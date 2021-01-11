"""
Module for "seeing" the client.

"""

import logging as log
import pathlib
import pyautogui as pag
import startup
import vision
import misc
import behaviour
import input

def haystack_locate(image, haystack, grayscale=False, conf=0.95):
    """
    Finds the coordinates of a image image within a haystack image.

    Args:
        image (file): Filepath to the image image.
        haystack (file): Filepath to the haystack image.
        grayscale (bool): Whether to use grayscale matching to increase
                          speed, default is false.
        conf (float): Similarity required to match image to haystack,
                      expressed as a decimal <= 1, default is 0.95.

    """
    # Make sure file path is OS-agnostic.
    image = str(pathlib.Path(image))

    target_image = pag.locate(image, haystack, confidence=conf, grayscale=grayscale)
    if target_image is not None:
        log.debug('Found center of %s, %s', image, target_image)
        return target_image

    log.debug('Cannot find center of %s, conf=%s', image, conf)
    return False


class Vision:
    """
    Contains methods for locating images on the display. All coordinates
    are relative to the top left corner of the display.

    Args:
        ltwh (tuple): A 4-tuple containing the Left, Top, Width, and
                      Height of the region in which to look for the
                      image.
        image (file): The image to search within the (ltwh) coordinates
                       for. Must be a filepath.
        loctype (str): Whether to return the image's (ltwh) coordinates
                       or its (X, Y) center.
            regular = Returns the image's left, top, width, and height
                      as a 4-tuple.
            center = Returns the (X, Y) coordinates of the image's
                     center as a 2-tuple (relative to the display's
                     dimensions).
        conf (float): The confidence value required to match the image
                      successfully, expressed as a decimal <= 1. This is
                      used by PyAutoGUI, default is 0.95.
        loop_num (int): The number of times wait_for_image() will search
                        the given coordinates for the image, default is
                        10.
        loop_sleep_range (tuple): A 2-tuple containing the minimum and
                                  maximum number of miliseconds to wait
                                  between image-search loops. Used by
                                  the wait_for_image() method, default
                                  is (0, 100).
        grayscale (bool): Converts the haystack to grayscale before
                          searching within it. Speeds up searching by
                          about 30%, default is false.

    """

    # def __init__(self, ltwh, image, loctype='regular', conf=0.95,
    #              loop_num=20, loop_sleep_range=(0, 100), grayscale=False):
    def __init__(self, ltwh, image, loctype='regular', conf=0.80, 
        loop_num=20, loop_sleep_range=(0, 100), grayscale=True):
        self.grayscale = grayscale
        self.ltwh = ltwh
        self.image = image
        self.loctype = loctype
        self.conf = conf
        self.loop_num = loop_num
        self.loop_sleep_range = loop_sleep_range

    def mlocate(self):
        """
        Searches the (ltwh) coordinates for the image.

        Returns:
            If the image is found, and loctype is regular, returns the
            image's left/top/width/height parameters as a 4-tuple. If
            the image is found and loctype is center, returns coordinates
            of the image's center as a 2-tuple. If the image is not
            found, returns False.

        """
        # Make sure file path is OS-agnostic.
        image = str(pathlib.Path(self.image))

        if self.loctype == 'regular':
            target_image = pag.locateOnScreen(image, confidence=self.conf,
                                              grayscale=self.grayscale,
                                              region=self.ltwh)
            if target_image is not None:
                log.debug('Found regular image %s, %s', image, target_image)
                log.info('Found regular image %s, %s', image, target_image)
                return target_image

            log.debug('Cannot find regular image %s, conf=%s', image, self.conf)
            return False

        elif self.loctype == 'center':
            target_image = pag.locateCenterOnScreen(image, confidence=self.conf,
                                                    grayscale=self.grayscale,
                                                    region=self.ltwh)
            if target_image is not None:
                log.debug('Found center of image %s, %s', image, target_image)
                log.info('Found center of image %s, %s', image, target_image)
                return target_image

            log.debug('Cannot find center of image %s, conf=%s', image, self.conf)
            return False

        raise RuntimeError('Incorrect mlocate function parameters!')

    def wait_for_image(self, get_tuple=False):
        """
        Repeatedly searches within the (ltwh) coordinate space
        for the image.

        Args:
            get_tuple (bool): Whether to return a tuple containing the
                              image's coordinates.

        Returns:
            If get_tuple is false, returns True if image was found.

            If get_tuple is true and loctype is 'regular', returns a
            4-tuple containing the (left, top, width, height) coordinates
            of the image. If loctype is 'center', returns a tuple
            containing the (X, Y) center of the image.

            Returns False if image was not found.

        """
        # log.debug('Looking for ' + str(image))

        # Need to add 1 to loop_num because if range() starts at 0, the
        #   first loop will be the "0th" loop, which is confusing.
        for tries in range((self.loop_num + 1)):

            target_image = Vision.mlocate(self)

            if target_image is False:
                log.debug('Cannot find %s, tried %s times.', self.image, tries)
                loop_sleep_min, loop_sleep_max = self.loop_sleep_range
                misc.sleep_rand(loop_sleep_min, loop_sleep_max)

            else:
                log.debug('Found %s after trying %s times.', self.image, tries)
                if get_tuple is True:
                    return target_image
                return True

        log.debug('Timed out looking for %s', self.image)
        return False

    def click_image(self, sleep_range=(50, 200, 50, 200),
                    move_duration_range=(50, 1500),
                    button='left', move_away=False):
        """
        Moves the mouse to the provided image image and clicks on
        it.

        Args:
            sleep_range (tuple): Passed to the Mouse class in input.py,
                                 see its docstring for more info.
            move_duration_range (tuple): Passed to the Mouse class in
                                         input.py, see its docstring for
                                         more info.
            button (str): The mouse button to use when clicking on the
                          image, default is left.
            move_away (bool): Whether to move the mouse out of the way
                              after clicking on the image. Useful when
                              mlocate() needs to determine the status
                              of a button that the mouse just clicked.

        Returns:
            Returns True if method found the image and clicked on it,
            returns False otherwise.

        """
        log.debug('Looking for %s to click on.', self.image)

        target_image = self.wait_for_image(get_tuple=True)

        if isinstance(target_image, tuple) is True:
            # Randomize the location the pointer will move to using the dimensions of image image.
            input.Mouse(ltwh=target_image,
            # input.Mouse(ltwh=target_image,
                        sleep_range=sleep_range,
                        move_duration_range=move_duration_range,
                        button=button).click_coord()

            log.debug('Clicking on %s', self.image)

            if move_away is True:
                input.Mouse(ltwh=(25, 25, 100, 100), move_duration_range=(50, 200)).moverel()
            return True

        else:
            return False


def orient(ltwh=(0, 0, startup.DISPLAY_WIDTH, startup.DISPLAY_HEIGHT),
           launch_client=False):
    """
    Looks for an icon to orient the client. If it's found, use its
    location within the game client to determine the coordinates of the
    game client relative to the display's coordinates.

    This function is also used to determine if the client is logged out.
    This is generally one of the first functions that is run upon script
    startup.

    Args:
        ltwh (tuple): A 4-tuple containing the left, top, width, and
                      height of the coordinate space to search within,
                      relative to the display's coordinates. By default
                      uses the entire display.

    Raises:
       Raises an exception if the client cannot be found, or if the
       function can't determine if the client is logged in or logged
       out.

    Returns:
         If client is logged in, returns a 2-tuple containing a string
         with the text "logged_in" and a 2-tuple of the center (X, Y)
         coordinates of the orient image.

         If client is logged out, returns a 2-tuple containing a string
         with the text "logged_out" and a 2-tuple of the center (X, Y)
         coordinates of the orient-logged-out image.

    """
    logged_in = Vision(ltwh=ltwh, image='images/minimap/orient.png',
                       loctype='center', loop_num=1, conf=0.8) \
        .wait_for_image(get_tuple=True)
    if isinstance(logged_in, tuple) is True:
        return 'logged_in', logged_in

    # If the client is not logged in, check if it's logged out.
    logged_out = Vision(ltwh=ltwh, image='images/login-menu/orient-logged-out.png',
                        loctype='center', loop_num=1, conf=0.8) \
        .wait_for_image(get_tuple=True)
    if isinstance(logged_out, tuple) is True:
        return 'logged_out', logged_out

    if launch_client is True:
        # TODO
        start_client()
        # Try 10 times to find the login screen after launching the client.
        for _ in range(10):
            misc.sleep_rand(8000, 15000)
            orient(ltwh=ltwh, launch_client=False)
        log.critical('Could not find client! %s', launch_client)
        raise Exception('Could not find client!')

    else:
        raise Exception('Could not find client!')


# ----------------------------------------------------------------------
# Setup the necessary tuples for the Vision class and orient the client.
# ----------------------------------------------------------------------

display = (0, 0, startup.DISPLAY_WIDTH, startup.DISPLAY_HEIGHT)
(client_status, anchor) = orient(ltwh=display)
(client_left, client_top) = anchor

if client_status == 'logged_in':
    client_left -= 735
    client_top -= 21
elif client_status == 'logged_out':
    client_left -= 183
    client_top -= 59

# Each of these tuples contains coordinates for the "region" parameter
#   of PyAutoGUI's Locate() functions. These tuples are used by methods
#   in the Vision class to look for images within the specified set of
#   coordinates, rather than within the entire display's coordinates,
#   which is much faster.
client = (client_left, client_top,
          startup.CLIENT_WIDTH, startup.CLIENT_HEIGHT)

# The player's inventory.
inv_left = client_left + 548
inv_top = client_top + 205
inv = (inv_left, inv_top,
       startup.INV_WIDTH, startup.INV_HEIGHT)

# Bottom half of the player's inventory.
inv_bottom_left = inv_left
inv_bottom_top = inv_top + startup.INV_HALF_HEIGHT
inv_bottom = (inv_bottom_left, inv_bottom_top,
              startup.INV_WIDTH, startup.INV_HALF_HEIGHT)

# Right half of the player's inventory.
inv_right_half_left = (inv_left + startup.INV_HALF_WIDTH) - 5
inv_right_half_top = inv_top
inv_right_half = (inv_right_half_left, inv_right_half_top,
                  startup.INV_HALF_WIDTH, startup.INV_HEIGHT)

# Left half of the player's inventory.
inv_left_half_left = inv_left
inv_left_half_top = inv_top
inv_left_half = (inv_left_half_left, inv_left_half_top,
                 startup.INV_HALF_WIDTH, startup.INV_HEIGHT)

# Gameplay screen.
game_screen_left = client_left + 4
game_screen_top = client_top + 4
game_screen = (game_screen_left, game_screen_top,
               startup.GAME_SCREEN_WIDTH, startup.GAME_SCREEN_HEIGHT)

# The player's inventory, plus the top and bottom "side stone" tabs that
#   open all the different menus.
side_stones_left = client_left + 516
side_stones_top = client_top + 166
side_stones = (side_stones_left, side_stones_top,
               startup.SIDE_STONES_WIDTH, startup.SIDE_STONES_HEIGHT)

# Chat menu.
chat_menu_left = client_left + 7
chat_menu_top = client_top + 345
chat_menu = (chat_menu_left, chat_menu_top,
             startup.CHAT_MENU_WIDTH, startup.CHAT_MENU_HEIGHT)

# The most recent chat message.
chat_menu_recent_left = chat_menu_left - 3
chat_menu_recent_top = chat_menu_top + 98
chat_menu_recent = (chat_menu_recent_left, chat_menu_recent_top,
                    startup.CHAT_MENU_RECENT_WIDTH, startup.CHAT_MENU_RECENT_HEIGHT)

# The text input fields on the login menu.
login_field_left = client_left + 273
login_field_top = client_top + 242
login_field = (login_field_left, login_field_top,
               startup.LOGIN_FIELD_WIDTH, startup.LOGIN_FIELD_HEIGHT)

pass_field_left = client_left + 275
pass_field_top = client_top + 258
pass_field = (pass_field_left, pass_field_top,
              startup.LOGIN_FIELD_WIDTH, startup.LOGIN_FIELD_HEIGHT)

# The entire minimap.
minimap_left = client_left + 571
minimap_top = client_top + 11
minimap = (minimap_left, minimap_top,
           startup.MINIMAP_WIDTH, startup.MINIMAP_HEIGHT)

# The current minimap "slice" for locating the player on the world map.
minimap_slice_left = client_left + 590
minimap_slice_top = client_top + 51
minimap_slice = (minimap_slice_left, minimap_slice_top,
                 startup.MINIMAP_SLICE_WIDTH, startup.MINIMAP_SLICE_HEIGHT)
