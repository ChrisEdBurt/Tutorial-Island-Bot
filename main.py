"""
Main bot file.

"""

import os
import sys
import pyautogui as pag
import pyclick as pyc
import random as rand
import time
import configparser

# Read the config file.
config = configparser.ConfigParser()
config.read('./config.ini')

# Constants ------------------------------------------------------------
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
    elapsed_time_seconds = round(current_time - startup.start_time)

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


TEST_LEFT = 0
TEST_TOP = 0 
TEST_WIDTH = 0 
TEST_HEIGHT = 0

# Test
# Move mouse to top left corner of the screen.
test_coordinates = (TEST_LEFT, TEST_TOP, TEST_WIDTH, TEST_HEIGHT)
Mouse(ltwh=test_coordinates).move_to()