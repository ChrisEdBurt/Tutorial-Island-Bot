"""
Main bot file.

"""

import sys
import startup
import vision
import misc
import behaviour
import input
import skills
import logging as log

import os
import time
from PIL import Image

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

# login using credentials, type full username followed by the password.
# behaviour.login_full()

behaviour.login_basic()

# time.sleep(15)

logged_in = vision.Vision(ltwh=vision.display,
                                   image='./images/minimap/orient.png',
                                   loop_num=50, loop_sleep_range=(1000, 2000)).wait_for_image()

# log.info('Open inventory screen if closed, otherwise nothing.')
# behaviour.open_side_stone('inventory')

gielnor_guide = [os.path.join('./images/game-screen/tutorial-island/gielnor-guide/',f) for f in os.listdir('./images/game-screen/tutorial-island/gielnor-guide/') if f.endswith('.png')]
print(gielnor_guide)

for i in gielnor_guide:
    log.info('gielbor_guide ' + i)
    gielnor_guide1 = vision.Vision(ltwh=vision.client,
    image = i,    
    loop_num=1).click_image()

# Test ----------------------------------------------------------------------------------------------------------------------