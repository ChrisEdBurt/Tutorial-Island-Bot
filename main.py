"""
Main bot file.

"""

import os
import time
import sys

import startup
import vision
import misc
import behaviour
import input
import skills
import logging as log

import step_one
import step_two
import step_three
import step_four
import step_five
import step_six
import step_seven
import step_eight
import step_nine
import step_ten
import step_eleven

# Test ----------------------------------------------------------------------------------------------------------------------

# login using credentials, type full username followed by the password. Dont wait for after login screen to appear.
#behaviour.login_full()
behaviour.login_basic()

logged_in = vision.Vision(ltwh=vision.display,
image='./images/minimap/orient.png',
loop_num=50, loop_sleep_range=(1000, 2000)).wait_for_image()

step_three.third_step()

# Test ----------------------------------------------------------------------------------------------------------------------