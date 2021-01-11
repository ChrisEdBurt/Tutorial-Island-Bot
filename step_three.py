"""
Step three file.

"""

import os
import vision
import logging as log
import pyautogui as pag

# Step Three Gielnor Guide -------------------------------------------------------------------------------------------------

def third_step():
    speak_to_gielnor_guide()
    click_experienced_player()
    click_spanner_icon()
    speak_to_gielnor_guide()
    click_door()

def speak_to_gielnor_guide():
    # locate and click experienced player response
    gielnor_guide = [os.path.join('./images/game-screen/tutorial-island/step-three/gielnor-guide/',f) for f in os.listdir('./images/game-screen/tutorial-island/step-three/gielnor-guide/') if f.endswith('.png')]
    #print(gielnor_guide)

    for i in gielnor_guide:
        log.info('gielbor_guide ' + i)
        gielnor_guide1 = vision.Vision(ltwh=vision.client,
        image = i,    
        loop_num=1).click_image()

    pag.press('space', presses=5)

def click_experienced_player():
    # locate and click experienced player response
    experienced_player = vision.Vision(ltwh=vision.client,
    image='./images/game-screen/tutorial-island/step-three/dialoge_responses/experienced.png',
    loop_num=1).click_image()

def click_spanner_icon():
    # locate and click closed spanner(settings) icon
    experienced_player = vision.Vision(ltwh=vision.client,
    image='./images/side-stones/closed/settings.png',
    loop_num=1).click_image()

def click_door():
    # locate and click door
    door = [os.path.join('./images/game-screen/tutorial-island/step-three/',f) for f in os.listdir('./images/game-screen/tutorial-island/step-three/') if f.endswith('.png')]
    #print(door)
    for i in door:
        log.info('door ' + i)
        door = vision.Vision(ltwh=vision.client,
        image = i,    
        loop_num=1).click_image()