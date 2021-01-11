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

#behaviour.login_basic()

# log.info('Open inventory screen if closed, otherwise nothing.')
# behaviour.open_side_stone('inventory')

log.info('gielbor_guide1')
gielnor_guide1 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide1.png',    
    loop_num=1).click_image()

log.info('gielbor_guide2')
gielnor_guide2 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide2.png',
    loop_num=1).click_image()

log.info('gielbor_guide3')
gielnor_guide3 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide3.png',
    loop_num=1).click_image()

log.info('gielbor_guide4')
gielnor_guide4 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide4.png',
    loop_num=1).click_image()

log.info('gielbor_guide5')
gielnor_guide5 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide5.png',
    loop_num=1).click_image()

log.info('gielbor_guide6')
gielnor_guide6 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide6.png',
    loop_num=1).click_image()

log.info('gielbor_guide7')
gielnor_guide7 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide7.png',
    loop_num=1).click_image()

log.info('gielbor_guide8')
gielnor_guide8 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide8.png',
    loop_num=1).click_image()

log.info('gielbor_guide9')
gielnor_guide9 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide9.png',
    loop_num=1).click_image()

log.info('gielbor_guide10')
gielnor_guide10 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide10.png',
    loop_num=1).click_image()

log.info('gielbor_guide11')
gielnor_guide11 = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/gielnor-guide/gielbor_guide11.png',
    loop_num=1).click_image()


# Test ----------------------------------------------------------------------------------------------------------------------