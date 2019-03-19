'''
Created on Mar 12, 2019

@author: antho
'''

import random
import pygame as p
import math

from Classes import *
            
# Set up the window
def setup():  
    global running, clock, screen  
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((500, 500))
    running = True
    
def main():
    global running, clock, screen
    startButton = ToggleButton(100,100, 'Start', 'PixelSplitter-Bold.ttf', 30, (0,0,0), (255,0,0))
    save_file = GameData('/Saves/Save.txt')
    print(save_file.data)
    while running == True:
        bg = p.Rect(0,0,500,500)
        p.draw.rect(screen, (255,255,255), bg)
        startButton.draw(screen)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.MOUSEMOTION:
                if startButton.check(p.mouse.get_pos()):
                    startButton.toggleOn()
                else:
                    startButton.toggleOff()
        p.display.flip()
        clock.tick(60)
        
setup()
main()