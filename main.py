"""
Main bot file.

"""

import os
import sys
import logging as log
import pathlib
import pyautogui as pag
import pyclick as pyc
import random as rand
import time
import configparser
import logging as log

# Read the config file.
config = configparser.ConfigParser()
config.read('./config.ini')

log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s', level=str(config.get('main', 'log_level')))

# Constants ------------------------------------------------------------------------------------------------------------------
# Captures the width and height of various different elements within the game client. Units are in pixels.

# The entire OSRS game client (in fixed-size mode).
CLIENT_WIDTH = 765
CLIENT_HEIGHT = 503

# The player's inventory.
INV_WIDTH = 186
INV_HEIGHT = 262
INV_HALF_WIDTH = round((INV_WIDTH / 2) + 5)
INV_HALF_HEIGHT = round(INV_HEIGHT / 2)

# The player's inventory plus the top and bottom rows of side stones.
SIDE_STONES_WIDTH = 249
SIDE_STONES_HEIGHT = 366

# The "gameplay screen". This is the screen that displays the player character and the game world.
GAME_SCREEN_WIDTH = 512
GAME_SCREEN_HEIGHT = 334

# The bottom chat menu pane.
CHAT_MENU_WIDTH = 506
CHAT_MENU_HEIGHT = 129

# The most recent "line" in the chat menu's chat history.
CHAT_MENU_RECENT_WIDTH = 490
CHAT_MENU_RECENT_HEIGHT = 17

# The entire display.
DISPLAY_WIDTH = pag.size().width
DISPLAY_HEIGHT = pag.size().height

# The "Login" and "Password" fields on the main login screen.
LOGIN_FIELD_WIDTH = 258
LOGIN_FIELD_HEIGHT = 12

# The entire minimap.
MINIMAP_WIDTH = 146
MINIMAP_HEIGHT = 151

# The largest area of the minimap, centered on the player, that can be used to determine the player's location for the travel() function.
MINIMAP_SLICE_WIDTH = 110
MINIMAP_SLICE_HEIGHT = 73

# username_file = config.get('main', 'username_file')
# password_file = config.get('main', 'password_file')

# # Remove line breaks from password and usernam to make logging in more predictable.
# username = open(username_file, 'r').read()
# username = str(username.replace('\n', ''))

# password = open(password_file, 'r').read()
# password = str(password.replace('\n', ''))

# print(username)
# print(password)

# Misc ------------------------------------------------------------------------------------------------------------------
# Utility Methods


def rand_seconds(rmin=0, rmax=100):
    """
    Gets a random integer between two values. Input arguments are in
    miliseconds but output is in seconds. For example, if this function
    generates a random value of 391, it will return a value of 0.391.

    Args:
        rmin (int): The minimum number of miliseconds, default is 0.
        rmax (int): The maximum number of miliseconds, default is 100.

    Returns:
        Returns a float.

    """
    randval = rand.randint(rmin, rmax)
    randval = float(randval / 1000)
    # log.debug('Got random value of %s.', randval)
    return randval


def sleep_rand(rmin=0, rmax=100):
    """
    Does nothing for a random period of time. Input arguments are in
    miliseconds.

    Args:
        rmin (int): The minimum number of miliseconds to wait, default
                    is 0.
        rmax (int): The maximum number of miliseconds to wait, default
                    is 100.

    """
    sleeptime = rand_seconds(rmin=rmin, rmax=rmax)
    # log.debug('Sleeping for %s seconds.', sleeptime)
    time.sleep(sleeptime)
    return True


def session_duration(human_readable=False):
    """
    Determines how many seconds the current session has been running.
    This timer is reset when the bot logs in or when the bot restarts.

    Args:
        human_readable (bool): Whether to return the number of seconds
                               the bot has been running, or the amount
                               of time in a HH:MM:SS format, default is
                               false.

    Returns:
          Returns an int containing the number of seconds the bot has
          been running since its last logon.
    """
    current_time = time.time()
    # Get elapsed time by subtracting startup time from current time.
    elapsed_time_seconds = round(current_time - start_time)

    if human_readable is False:
        return elapsed_time_seconds
    else:
        elapsed_time_human_readable = datetime.timedelta(seconds=elapsed_time_seconds)
        return elapsed_time_human_readable


def wait_rand(chance, second_chance=10, wait_min=10000, wait_max=60000):
    """
    Roll for a chance to do nothing for the specified period of time.

    Args:
        chance (int): The number that must be rolled for the wait to be
                      called. For example, if chance is 25, then there
                      is a 1 in 25 chance for the roll to pass.
        second_chance (int): The number that must be rolled for an
                             additional wait to be called if the first
                             roll passes, default is 10. By default,
                             this means that 10% of waits that pass the
                             first roll wait for an additional period of
                             time.
        wait_min (int): The minimum number of miliseconds to wait if the
                        roll passes, default is 10000.
        wait_max (int): The maximum number of miliseconds to wait if the
                        roll passes, default is 60000.
    """
    wait_roll = rand.randint(1, chance)
    if wait_roll == chance:
        log.info('Random wait called.')
        sleeptime = rand_seconds(wait_min, wait_max)
        log.info('Sleeping for %s seconds...', round(sleeptime))
        time.sleep(sleeptime)

        # Perform an additional wait roll so that (1/second_chance)
        #   waits are extra long.
        wait_roll = rand.randint(1, second_chance)
        if wait_roll == 10:
            log.info('Additional random wait called.')
            sleeptime = rand_seconds(wait_min, wait_max)
            log.info('Sleeping for %s seconds...', round(sleeptime))
            time.sleep(sleeptime)
    return True


# Misc-End ------------------------------------------------------------------------------------------------------------------


# Input ------------------------------------------------------------------------------------------------------------------


# initialize HumanClicker object
hc = pyc.HumanClicker()


class Mouse:
    """
    Class to move and click the mouse cursor.

    Args:
        ltwh (tuple): A 4-tuple containing the left, top, width, and
                      height coordinates. The width and height values
                      are used for randomizing the location of the mouse
                      cursor.
        sleep_range (tuple): A 4-tuple containing the minimum and maximum
                             number of miliseconds to wait before
                             performing the action, and the minimum and
                             maximum number of miliseconds to wait after
                             performing the action, default is
                             (0, 500, 0, 500).
        action_duration_range (tuple): A 2-tuple containing the
                                       minimum and maximum number of
                                       miliseconds during which the
                                       action will be performed, such as
                                       holding down the mouse button,
                                       default is (1, 100).
        move_duration_range (tuple): A 2-tuple containing the
                                     minimum and maximum number of
                                     miliseconds to take to move the
                                     mouse cursor to its destination,
                                     default is (50, 1500).
        button (str): The mouse button to click with, default is left.
    """


    def __init__(self,
                 ltwh,  # "left, top, width, height"
                 sleep_range=(0, 500, 0, 500),
                 move_duration_range=(50, 1500),
                 action_duration_range=(1, 100),
                 button='left'):

        self.ltwh = ltwh
        self.sleep_range = sleep_range
        self.move_duration_range = move_duration_range
        self.action_duration_range = action_duration_range
        self.button = button

    def click_coord(self, move_away=False):
        """
        Clicks within the provided coordinates. If width and height are
        both 0, then this function will click in the exact same location
        every time.

        Args:
            move_away (bool): Whether to move the mouse cursor a short
                              distance away from the coordinates that
                              were just clicked on, default is False.

        """
        self.move_to()
        self.click()
        if move_away is True:
            self.ltwh = (15, 15, 100, 100)
            self.move_duration_range = (0, 500)
            self.moverel()
        return True


    def move_to(self):
        """
        Moves the mouse pointer to the specified coordinates. Coordinates
        are based on the display's dimensions. Units are in pixels. Uses
        Bezier curves to make mouse movement appear more human-like.

        """
        left, top, width, height = self.ltwh

        # hc.move uses a (x1, x2, y1, y2) coordinate format instead of a
        #   (left, top, width, height) format.
        # x2 and y2 are obtained by adding width to left and height to top.
        x_coord = rand.randint(left, (left + width))
        y_coord = rand.randint(top, (top + height))

        hc.move((x_coord, y_coord), self.move_duration())
        return True


    def moverel(self):
        """
        Moves the mouse in a random direction, relative to its current
        position. Uses left/width to determinie the minimum and maximum
        X distance to move and top/height to determine the minimum and
        maximum Y distance to move.

        Whichever of the two left/width values is lower will be used as
        the minimum X distance and whichever of the two values is higher
        will be used as the maximum X distance. Same for top/height.

        """
        left, top, width, height = self.ltwh
        (x_position, y_position) = pag.position()

        # Get min and max values based on the provided ltwh coordinates.
        x_min = min(left, width)
        x_max = max(left, width)
        y_min = min(top, height)
        y_max = max(top, height)

        # Get a random distance to move based on min and max values.
        x_distance = rand.randint(x_min, x_max)
        y_distance = rand.randint(y_min, y_max)

        y_destination = y_position + y_distance
        x_destination = x_position + x_distance

        # Roll for a chance to reverse the direction the mouse moves in.
        if (rand.randint(1, 2)) == 2:
            x_destination = x_position - x_distance
        if (rand.randint(1, 2)) == 2:
            y_destination = y_position - y_distance

        hc.move((x_destination, y_destination), self.move_duration())
        return True


    def move_duration(self):
        """
        Randomizes the amount of time the mouse cursor takes to move to
        a new location.

        Returns:
            Returns a float containing a number in seconds.

        """
        move_durmin, move_durmax = self.move_duration_range
        move_duration_var = rand_seconds(rmin=move_durmin, rmax=move_durmax)
        return move_duration_var


    def click(self, hold=False):
        """
        Clicks the left or right mouse button, waiting both before and
        after for a randomized period of time.

        Args:
            hold (bool): Whether to hold down the mouse button rather
                         than just clicking it.
                         Uses self.action_duration_range to determine
                         the minimum and maximum duration to hold down
                         the mouse button.

        """
        # Random sleep before click.
        sleep_rand(rmin=self.sleep_range[0], rmax=self.sleep_range[1])

        if hold is True:
            duration = rand_seconds(rmin=self.action_duration_range[0],
                                         rmax=self.action_duration_range[1])
            pag.click(button=self.button, duration=duration)
        else:
            pag.click(button=self.button)

        # Random sleep after click.
        sleep_rand(rmin=self.sleep_range[2], rmax=self.sleep_range[3])
        return True


# Input-End ------------------------------------------------------------------------------------------------------------------


# Vision ------------------------------------------------------------------------------------------------------------------


class Vision:
    """
    Contains methods for locating images on the display. All coordinates
    are relative to the top left corner of the display.

    Args:
        ltwh (tuple): A 4-tuple containing the Left, Top, Width, and
                      Height of the region in which to look for the
                      needle.
        needle (file): The image to search within the (ltwh) coordinates
                       for. Must be a filepath.
        loctype (str): Whether to return the needle's (ltwh) coordinates
                       or its (X, Y) center.
            regular = Returns the needle's left, top, width, and height
                      as a 4-tuple.
            center = Returns the (X, Y) coordinates of the needle's
                     center as a 2-tuple (relative to the display's
                     dimensions).
        conf (float): The confidence value required to match the needle
                      successfully, expressed as a decimal <= 1. This is
                      used by PyAutoGUI, default is 0.95.
        loop_num (int): The number of times wait_for_image() will search
                        the given coordinates for the needle, default is
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

    def __init__(self, ltwh, needle, loctype='regular', conf=0.95,
                 loop_num=10, loop_sleep_range=(0, 100), grayscale=False):
        self.grayscale = grayscale
        self.ltwh = ltwh
        self.needle = needle
        self.loctype = loctype
        self.conf = conf
        self.loop_num = loop_num
        self.loop_sleep_range = loop_sleep_range

    def mlocate(self):
        """
        Searches the (ltwh) coordinates for the needle image.

        Returns:
            If the needle is found, and loctype is regular, returns the
            needle's left/top/width/height parameters as a 4-tuple. If
            the needle is found and loctype is center, returns coordinates
            of the needle's center as a 2-tuple. If the needle is not
            found, returns False.
        """
        # Make sure file path is OS-agnostic.
        needle = str(pathlib.Path(self.needle))

        if self.loctype == 'regular':
            target_image = pag.locateOnScreen(needle, confidence=self.conf,
                                              grayscale=self.grayscale,
                                              region=self.ltwh)
            if target_image is not None:
                log.debug('Found regular image %s, %s', needle, target_image)
                return target_image

            log.debug('Cannot find regular image %s, conf=%s', needle, self.conf)
            return False

        elif self.loctype == 'center':
            target_image = pag.locateCenterOnScreen(needle, confidence=self.conf,
                                                    grayscale=self.grayscale,
                                                    region=self.ltwh)
            if target_image is not None:
                log.debug('Found center of image %s, %s', needle, target_image)
                return target_image

            log.debug('Cannot find center of image %s, conf=%s', needle, self.conf)
            return False

        raise RuntimeError('Incorrect mlocate function parameters!')


    def wait_for_image(self, get_tuple=False):
        """
        Repeatedly searches within the (ltwh) coordinate space
        for the needle.

        Args:
            get_tuple (bool): Whether to return a tuple containing the
            needle's coordinates.

        Returns:
            If get_tuple is false, returns True if needle was found.

            If get_tuple is true and loctype is 'regular', returns a
            4-tuple containing the (left, top, width, height) coordinates
            of the needle. If loctype is 'center', returns a tuple
            containing the (X, Y) center of the needle.

            Returns False if needle was not found.
        """
        # log.debug('Looking for ' + str(needle))

        # Need to add 1 to loop_num because if range() starts at 0, the
        #   first loop will be the "0th" loop, which is confusing.
        for tries in range((self.loop_num + 1)):

            target_image = Vision.mlocate(self)

            if target_image is False:
                log.debug('Cannot find %s, tried %s times.', self.needle, tries)
                loop_sleep_min, loop_sleep_max = self.loop_sleep_range
                sleep_rand(loop_sleep_min, loop_sleep_max)

            else:
                log.debug('Found %s after trying %s times.', self.needle, tries)
                if get_tuple is True:
                    return target_image
                return True

        log.debug('Timed out looking for %s', self.needle)
        return False


    def click_image(self, sleep_range=(50, 200, 50, 200),
                    move_duration_range=(50, 1500),
                    button='left', move_away=False):
        """
        Moves the mouse to the provided needle image and clicks on
        it.

        Args:
            sleep_range (tuple): Passed to the Mouse class in input.py,
            see its docstring for more info.
            move_duration_range (tuple): Passed to the Mouse class in
            input.py, see its docstring for
            more info.
            button (str): The mouse button to use when clicking on the
            needle, default is left.
            move_away (bool): Whether to move the mouse out of the way
            after clicking on the needle. Useful when
            mlocate() needs to determine the status
            of a button that the mouse just clicked.

        Returns:
            Returns True if method found the needle and clicked on it,
            returns False otherwise.
        """
        log.debug('Looking for %s to click on.', self.needle)

        target_image = self.wait_for_image(get_tuple=True)

        if isinstance(target_image, tuple) is True:
            # Randomize the location the pointer will move to using the
            #   dimensions of needle image.
            #input.Mouse(ltwh=target_image,
            Mouse(ltwh=target_image,
            # input.Mouse(ltwh=target_image,
                        sleep_range=sleep_range,
                        move_duration_range=move_duration_range,
                        button=button).click_coord()

            log.debug('Clicking on %s', self.needle)

            if move_away is True:
                #input.Mouse(ltwh=(25, 25, 100, 100), move_duration_range=(50, 200)).moverel()
                Mouse(ltwh=(25, 25, 100, 100), move_duration_range=(50, 200)).moverel()
            return True

        else:
            return False


# Look for client
# def orient(ltwh=(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT),
#            launch_client=False):
#     """
#     Looks for an icon to orient the client. If it's found, use its
#     location within the game client to determine the coordinates of the
#     game client relative to the display's coordinates.

#     This function is also used to determine if the client is logged out.
#     This is generally one of the first functions that is run upon script
    

#     Args:
#         ltwh (tuple): A 4-tuple containing the left, top, width, and
#         height of the coordinate space to search within,
#         relative to the display's coordinates. By default
#         uses the entire display.

#     Raises:
#        Raises an exception if the client cannot be found, or if the
#        function can't determine if the client is logged in or logged
#        out.

#     Returns:
#          If client is logged in, returns a 2-tuple containing a string
#          with the text "logged_in" and a 2-tuple of the center (X, Y)
#          coordinates of the orient needle.

#          If client is logged out, returns a 2-tuple containing a string
#          with the text "logged_out" and a 2-tuple of the center (X, Y)
#          coordinates of the orient-logged-out needle.

#     """
#     logged_in = Vision(ltwh=ltwh, needle='images/minimap/orient.png',
#                        loctype='center', loop_num=1, conf=0.8) \
#         .wait_for_image(get_tuple=True)
#     if isinstance(logged_in, tuple) is True:
#         return 'logged_in', logged_in

#     # If the client is not logged in, check if it's logged out.
#     logged_out = Vision(ltwh=ltwh, needle='images/login-menu/orient-logged-out.png',
#                         loctype='center', loop_num=1, conf=0.8) \
#         .wait_for_image(get_tuple=True)
#     if isinstance(logged_out, tuple) is True:
#         return 'logged_out', logged_out

#     # if launch_client is True:
#     #     # TODO
#     #     start_client()
#     #     # Try 10 times to find the login screen after launching the client.
#     #     for _ in range(10):
#     #         sleep_rand(8000, 15000)
#     #         orient(ltwh=ltwh, launch_client=False)
#     #     log.critical('Could not find client! %s', launch_client)
#     #     raise Exception('Could not find client!')

#     else:
#         raise Exception('Could not find client!')

# ----------------------------------------------------------------------
# Setup the necessary tuples for the Vision class and orient the client.
# ----------------------------------------------------------------------

# display = (0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
# (client_status, anchor) = orient(ltwh=display)
# (client_left, client_top) = anchor

# if client_status == 'logged_in':
#     client_left -= 735
#     client_top -= 21

client_left = 0
client_top = 0

# Each of these tuples contains coordinates for the "region" parameter
#   of PyAutoGUI's Locate() functions. These tuples are used by methods
#   in the Vision class to look for images within the specified set of
#   coordinates, rather than within the entire display's coordinates,
#   which is much faster.
client = (client_left, client_top,
          CLIENT_WIDTH, CLIENT_HEIGHT)

# The player's inventory.
inv_left = client_left + 548
inv_top = client_top + 205
inv = (inv_left, inv_top,
       INV_WIDTH, INV_HEIGHT)

# Bottom half of the player's inventory.
inv_bottom_left = inv_left
inv_bottom_top = inv_top + INV_HALF_HEIGHT
inv_bottom = (inv_bottom_left, inv_bottom_top,
              INV_WIDTH, INV_HALF_HEIGHT)

# Right half of the player's inventory.
inv_right_half_left = (inv_left + INV_HALF_WIDTH) - 5
inv_right_half_top = inv_top
inv_right_half = (inv_right_half_left, inv_right_half_top,
                  INV_HALF_WIDTH, INV_HEIGHT)

# Left half of the player's inventory.
inv_left_half_left = inv_left
inv_left_half_top = inv_top
inv_left_half = (inv_left_half_left, inv_left_half_top,
                 INV_HALF_WIDTH, INV_HEIGHT)

# Gameplay screen.
game_screen_left = client_left + 4
game_screen_top = client_top + 4
game_screen = (game_screen_left, game_screen_top,
               GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

# The player's inventory, plus the top and bottom "side stone" tabs that open all the different menus.
side_stones_left = client_left + 516
side_stones_top = client_top + 166
side_stones = (side_stones_left, side_stones_top,
               SIDE_STONES_WIDTH, SIDE_STONES_HEIGHT)

# Chat menu.
chat_menu_left = client_left + 7
chat_menu_top = client_top + 345
chat_menu = (chat_menu_left, chat_menu_top,
             CHAT_MENU_WIDTH, CHAT_MENU_HEIGHT)

# The most recent chat message.
chat_menu_recent_left = chat_menu_left - 3
chat_menu_recent_top = chat_menu_top + 98
chat_menu_recent = (chat_menu_recent_left, chat_menu_recent_top,
                    CHAT_MENU_RECENT_WIDTH, CHAT_MENU_RECENT_HEIGHT)

# The text input fields on the login menu.
login_field_left = client_left + 273
login_field_top = client_top + 242
login_field = (login_field_left, login_field_top,
               LOGIN_FIELD_WIDTH, LOGIN_FIELD_HEIGHT)

pass_field_left = client_left + 275
pass_field_top = client_top + 258
pass_field = (pass_field_left, pass_field_top,
              LOGIN_FIELD_WIDTH, LOGIN_FIELD_HEIGHT)

# The entire minimap.
minimap_left = client_left + 571
minimap_top = client_top + 11
minimap = (minimap_left, minimap_top,
           MINIMAP_WIDTH, MINIMAP_HEIGHT)

# The current minimap "slice" for locating the player on the world map.
minimap_slice_left = client_left + 590
minimap_slice_top = client_top + 51
minimap_slice = (minimap_slice_left, minimap_slice_top,
                 MINIMAP_SLICE_WIDTH, MINIMAP_SLICE_HEIGHT)


# Vision-End ------------------------------------------------------------------------------------------------------------------


# Behaviour ------------------------------------------------------------------------------------------------------------------


def open_side_stone(side_stone):
    """
    Opens a side stone menu.

    Args:
        side_stone (str): The name of the side stone to open. Available
                          options are 'attacks', 'skills', 'quests',
                          'inventory', 'equipment', 'prayers', 'spellbook',
                          'clan', 'friends', 'account', 'logout',
                          'settings', emotes', and 'music'.

    Returns:
        Returns True if desired side stone was opened or is already open.

    Raises:
        Raises an exception if side stone could not be opened.

    """
    side_stone_open = ('./images/side-stones/open/' + side_stone + '.png')
    side_stone_closed = ('./images/side-stones/closed/' + side_stone + '.png')

    # Some side stones need a higher than default confidence to determine
    #   if they're open.
    # stone_open = vision.Vision(ltwh=vision.side_stones, needle=side_stone_open,
    #                         loop_num=1, conf=0.98).wait_for_image()
    stone_open = Vision(ltwh=side_stones, needle=side_stone_open,
                        loop_num=1, conf=0.98).wait_for_image()
    if stone_open is True:
        log.debug('Side stone already open.')
        return True
    else:
        log.debug('Opening side stone...')

    # Try a total of 5 times to open the desired side stone menu using
    #   the mouse.
    for tries in range(6):
        # Move mouse out of the way after clicking so the function can
        #   tell if the stone is open.
        # Vision(ltwh=Vision.side_stones, needle=side_stone_closed,
        Vision(ltwh=side_stones, needle=side_stone_closed,
                   loop_num=3, loop_sleep_range=(100, 300)). \
            click_image(sleep_range=(0, 200, 0, 200), move_away=True)

        #stone_open = Vision(ltwh=Vision.side_stones, needle=side_stone_open,
        stone_open = Vision(ltwh=side_stones, needle=side_stone_open,
                                loop_num=3, conf=0.98, loop_sleep_range=(100, 200)). \
            wait_for_image()

        if stone_open is True:
            log.info('Opened side stone after %s tries.', tries)
            return True
        # Make sure the bank window isn't open, which would block
        #   access to the side stones.
        # Vision(ltwh=Vision.game_screen, needle='./images/buttons/close.png',
        Vision(ltwh=game_screen, needle='./images/buttons/close.png',
                   loop_num=1).click_image()
    raise Exception('Could not open side stone!')


def check_skills():
    """
    Used to mimic human-like behavior. Checks the stats of a random
    skill.

    """
    open_side_stone('skills')
    input.Mouse(ltwh=Vision.inv).move_to()
    sleep_rand(1000, 7000)


def human_behavior_rand(chance):
    """
    Randomly chooses from a list of human behaviors if the roll passes.
    This is done to make the bot appear more human.

    Args:
        chance (int): The number that must be rolled for a random
                      behavior to be triggered. For example, if this
                      parameter is 25, then there is a 1 in 25 chance
                      for the roll to pass.

    """
    roll = rand.randint(1, chance)
    log.info('Human behavior rolled %s', roll)
    if roll == chance:
        log.info('Attempting to act human.')
        roll = rand.randint(1, 2)
        if roll == 1:
            check_skills()
        elif roll == 2:
            roll = rand.randint(1, 8)
            if roll == 1:
                open_side_stone('attacks')
            elif roll == 2:
                open_side_stone('quests')
            elif roll == 3:
                open_side_stone('equipment')
            elif roll == 4:
                open_side_stone('prayers')
            elif roll == 5:
                open_side_stone('spellbook')
            elif roll == 6:
                open_side_stone('music')
            elif roll == 7:
                open_side_stone('friends')
            elif roll == 8:
                open_side_stone('settings')
        return
    return


def drop_item(item, track=True, wait_chance=120, wait_min=5000, wait_max=20000):
    """
    Drops all instances of the provided item from the inventory.
    Shift+Click to drop item MUST be enabled.

    Args:
       item (file): Filepath to an image of the item to drop, as it
                    appears in the player's inventory.
       track (bool): Keep track of the number of items dropped in a
                     global variable, default is True.
       wait_chance (int): Chance to wait randomly while dropping item,
                          see wait_rand()'s docstring for more info,
                          default is 50.
       wait_min (int): Minimum number of miliseconds to wait if
                       a wait is triggered, default is 5000.
       wait_max (int): Maximum number of miliseconds to wait if
                       a wait is triggered, default is 20000.
    """
    # TODO: create four objects, one for each quadrant of the inventory
    #   and rotate dropping items randomly among each quadrant to make
    #   item-dropping more randomized.

    # Make sure the inventory tab is selected in the main menu.
    # log.debug('Making sure inventory is selected')
    log.info('Open inventory')
    open_side_stone('inventory')
    log.info('inventory opened')
    
    # item_remains = Vision.inv.wait_for_image(loop_num=1, needle=item)
    item_remains = inv.wait_for_image(loop_num=1, needle=item)
    if item_remains is False:
        log.info('Could not find %s', item)
        return False

    log.info('Dropping all instances of %s', item)
    for tries in range(40):

        pag.keyDown('shift')
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        item_on_right = \
            inv_right_half(needle=item).click_image(loop_num=1,
            # Vision.inv_right_half(needle=item).click_image(loop_num=1,
                                                        sleep_range=(10, 50, 50, 300),
                                                        move_duration_range=(50, 800))
        # TODO: this "track" parameter is for stats. implement stats!
        # if item_on_right is True and track is True:
        #     startup.items_gathered += 1

        item_on_left = \
            inv_left_half(needle=item).click_image(loop_num=1,
            #Vision.inv_left_half(needle=item).click_image(loop_num=1,
                                                       sleep_range=(10, 50, 50, 300),
                                                       move_duration_range=(50, 800))
        # if item_on_left is True and track is True:
        #     startup.items_gathered += 1

        # Search the entire inventory to check if the item is still
        #   there.
        #item_remains = Vision.inv.wait_for_image(loop_num=1, needle=item)
        item_remains = inv.wait_for_image(loop_num=1, needle=item)

        # Chance to briefly wait while dropping items.
        wait_rand(wait_chance, wait_min, wait_max)

        pag.keyUp('shift')
        if item_remains is False:
            return True

    log.error('Tried dropping item too many times!')
    return False


def enable_run():
    """
    If run is turned off but energy is full, turns running on.

    """
    # TODO: turn run on when over 75%
    for _ in range(5):
        # run_full_off = Vision(ltwh=Vision.client,
        run_full_off = Vision(ltwh=client,
                                  needle='./images/buttons/run-full-off.png',
                                  loop_num=1).click_image(move_away=True)
        if run_full_off is True:
            sleep_rand(300, 1000)
            #run_full_on = Vision(ltwh=Vision.client,
            run_full_on = Vision(ltwh=client,
                                     needle='./images/buttons/run-full-on.png',
                                     loop_num=1).wait_for_image()
            if run_full_on is True:
                return True
        else:
            return False
    log.error('Unable to turn on running!')


# def travel(param_list, haystack_map):
#     """
#     Clicks on the minimap until the plater has arrived at the desired
#     coordinates.

#     Here's an example of what the arguments might look like for this
#     function:
#         [((240, 399), 1, (4, 4), (5, 10))], haystack.png
#         (240, 399) = The X and Y coordinates of the waypoint on
#                      haystack.png.
#         1 = The X and Y variation in coordinates that will be used when
#             clicking on the minimap.
#         (4, 4) = The X and Y variation in coordinates the function will
#                  allow when checking if the player has reached the
#                  waypoint.
#         (5, 10) = The minimum and maximum number of seconds to wait for
#                   the player to walk/run to the location clicked on in
#                   the minimap.

#     Args:
#         param_list (list): A list of the coordinates to move the player
#                            to, among a few other parameters.
#                            Each item in the list containes three tuples
#                            and an integer in the following order:
#                            - A 2-tuple of the desired XY coordinates.
#                            - An integer of the coordinate tolerance for
#                              each minimap click.
#                            - A 2-tuple of the X and Y tolerance allowed
#                              for determining if the player has reached
#                              the waypoint.
#                            - A 2-tuple of the minimum and maximum number of
#                              seconds to sleep before re-checking position
#                              while going to that waypoint.
#         haystack_map (file): Filepath to the map to use to navigate.
#                              All waypoint coordinates are relative to
#                              this map.

#     Raises:
#         Logs out if any errors occur.

#     """
#     # Make sure file path is OS-agnostic.
#     haystack_map = str(pathlib.Path(haystack_map))
#     haystack = cv2.imread(haystack_map, cv2.IMREAD_GRAYSCALE)

#     # Disable failsafe for now.
#     pag.FAILSAFE = False

#     # Get the first waypoint.
#     for params in param_list:
#         # Break down the parameters for that waypoint.
#         waypoint, coord_tolerance, waypoint_tolerance, sleep_range = params
#         for _ in range(500):

#             # Find the minimap position within the haystack map.
#             coords = ocv_find_location(haystack)
#             (coords_map_left, coords_map_top, coords_map_width, coords_map_height) = coords

#             # Get center of minimap coordinates within haystack map.
#             coords_map_x = int(coords_map_left + (coords_map_width / 2))
#             coords_map_y = int(coords_map_top + (coords_map_height / 2))

#             # Get center of minimap coordinates within client.
#             # Absolute coordinates are used rather than using an image
#             #   search to speed things up.
#             coords_client_x = vision.client[0] + 642
#             coords_client_y = vision.client[1] + 85

#             # Figure out how far the waypoint is from the current location.
#             waypoint_distance_x = waypoint[0] - coords_map_x
#             waypoint_distance_y = waypoint[1] - coords_map_y
#             log.debug('dest_distance x is %s.', waypoint_distance_x)
#             log.debug('dest_distance y is %s.', waypoint_distance_y)

#             # Check if player has reached waypoint before making the click.
#             if (abs(waypoint_distance_x) <= waypoint_tolerance[0] and
#                     abs(waypoint_distance_y) <= waypoint_tolerance[1]):
#                 break

#             # Generate random click coordinate variation.
#             coord_rand = rand.randint(-coord_tolerance, coord_tolerance)
#             # If the waypoint's distance is larger than the size of the
#             #   minimap (about 50 pixels in either direction), reduce
#             #   the click distance to the edge of the minimap.
#             if waypoint_distance_x >= 50:
#                 click_pos_x = coords_client_x + 50 + coord_rand
#                 # Since the minimap is circular, if the Y-distance is low
#                 #   enough, we can make the click-position for the X-coordinate
#                 #   farther left/right to take advantage of the extra space.
#                 if waypoint_distance_y <= 10:
#                     click_pos_x += 13

#             # If the waypoint's X distance is "negative", we know we
#             #   need to subtract X coordinates.
#             elif abs(waypoint_distance_x) >= 50:
#                 click_pos_x = coords_client_x - 50 + coord_rand
#                 if abs(waypoint_distance_y) <= 10:
#                     click_pos_x -= 13
#             else:
#                 click_pos_x = coords_client_x + waypoint_distance_x + coord_rand

#             # Do the same thing, but for the Y coordinates.
#             coord_rand = rand.randint(-coord_tolerance, coord_tolerance)
#             if waypoint_distance_y >= 50:
#                 click_pos_y = coords_client_y + 50 + coord_rand
#                 if waypoint_distance_x <= 10:
#                     click_pos_y += 13
#             elif abs(waypoint_distance_y) >= 50:
#                 click_pos_y = coords_client_y - 50 + coord_rand
#                 if abs(waypoint_distance_x) <= 10:
#                     click_pos_y -= 13
#             else:
#                 click_pos_y = coords_client_y + waypoint_distance_y + coord_rand

#             click_pos_y = abs(click_pos_y)
#             click_pos_x = abs(click_pos_x)
#             # Holding down ctrl while clicking will cause character to
#             #   run.
#             pag.keyDown('ctrl')
#             input.Mouse(ltwh=(click_pos_x, click_pos_y, 0, 0),
#                         sleep_range=(50, 100, 100, 200),
#                         move_duration_range=(0, 300)).click_coord()
#             pag.keyUp('ctrl')
#             misc.sleep_rand((sleep_range[0] * 1000), (sleep_range[1] * 1000))

#             if (abs(waypoint_distance_x) <= waypoint_tolerance[0] and
#                     abs(waypoint_distance_y) <= waypoint_tolerance[1]):
#                 break
#     # logout()
#     # raise Exception('Could not reach destination!')
    return True


# Behaviour-End -------------------------------------------------------------------------------------------------------------


# Test ----------------------------------------------------------------------------------------------------------------------

log.info('Open inventory screen if closed, otherwise nothing.')
open_side_stone('inventory')


# Test-End ------------------------------------------------------------------------------------------------------------------