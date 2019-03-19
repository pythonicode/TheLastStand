'''
Created on Mar 15, 2019

@author: antho
'''

from Global import *
from Classes import *

import pygame as p
import random
import math
from pygame.threads.Py25Queue import Full
from pygame.constants import K_ESCAPE

# Set up the Window
def setup():  
    global gameState, clock, screen, game
    global FULLSCREEN, RESOLUTION_SETTING, FPS_SETTING, WINDOW_WIDTH, WINDOW_HEIGHT, HELP  
    p.init()
    # RETRIEVING DATA FROM SAVE FILE
    game = GameData('Saves/Save.txt')
    data = game.data
    FULLSCREEN = toBoolean(data[0])
    RESOLUTION_SETTING = data[1]/900
    WINDOW_WIDTH = res(1600,RESOLUTION_SETTING)
    WINDOW_HEIGHT = res(900,RESOLUTION_SETTING)
    FPS_SETTING = data[2]
    HELP = toBoolean(data[3])
    clock = p.time.Clock()
    # Display mode (sets width and height for the window)
    if FULLSCREEN:
        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), p.FULLSCREEN)
    else:
        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Start the Mixer and Start playing Music
    p.mixer.init()
    p.mixer.music.load("Sounds/music.mp3") 
    p.mixer.music.play(-1,0.0)
    # Initial gameState
    gameState = 'mainmenu'

# Main function that runs the game
def main():
    global gameState, clock, screen, game
    global FULLSCREEN, RESOLUTION_SETTING, FPS_SETTING, WINDOW_WIDTH, WINDOW_HEIGHT, HELP, PREV_STATE
    # Misc Objects
    click = p.mixer.Sound('Sounds/click.wav')
    # Main Menu Objects
    startButton = TextButton(res(1120,RESOLUTION_SETTING), res(450,RESOLUTION_SETTING), 'Play', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    settingsButton = TextButton(res(1070+(res(40, RESOLUTION_SETTING)-40),RESOLUTION_SETTING), res(550,RESOLUTION_SETTING), 'Settings', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    quitButton = TextButton(res(1120,RESOLUTION_SETTING), res(650,RESOLUTION_SETTING), 'Exit', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    # Settings Objects
    fullScreenOnButton = TextButton(res(700,RESOLUTION_SETTING), res(200,RESOLUTION_SETTING), 'On', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    fullScreenOffButton = TextButton(res(1200,RESOLUTION_SETTING), res(200,RESOLUTION_SETTING), 'Off', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    lowResolutionButton = TextButton(res(600,RESOLUTION_SETTING), res(300,RESOLUTION_SETTING), '1280x720', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    midResolutionButton = TextButton(res(900,RESOLUTION_SETTING), res(300,RESOLUTION_SETTING), '1600x900', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    highResolutionButton = TextButton(res(1200,RESOLUTION_SETTING), res(300,RESOLUTION_SETTING), '1920x1080', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    lowFPS = TextButton(res(675,RESOLUTION_SETTING), res(400,RESOLUTION_SETTING), '15', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    midFPS = TextButton(res(975,RESOLUTION_SETTING), res(400,RESOLUTION_SETTING), '30', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    highFPS = TextButton(res(1275,RESOLUTION_SETTING), res(400,RESOLUTION_SETTING), '60', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    helpOnButton = TextButton(res(700,RESOLUTION_SETTING), res(500,RESOLUTION_SETTING), 'On', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    helpOffButton = TextButton(res(1200,RESOLUTION_SETTING), res(500,RESOLUTION_SETTING), 'Off', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    backButton = TextButton(res(750, RESOLUTION_SETTING), res(750,RESOLUTION_SETTING), 'Back', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    # Game Menu Objects
    upgradesButton = TextButton(res(700,RESOLUTION_SETTING), res(200,RESOLUTION_SETTING), 'Upgrades', 'PixelSplitter-Bold.ttf', res(50,RESOLUTION_SETTING), (0,0,0), (255,0,0))
    artifactsButton = TextButton(res(700,RESOLUTION_SETTING), res(400,RESOLUTION_SETTING), 'Artifacts', 'PixelSplitter-Bold.ttf', res(50,RESOLUTION_SETTING), (0,0,0), (255,0,0))
    skillsButton = TextButton(res(1100,RESOLUTION_SETTING), res(200,RESOLUTION_SETTING), 'Skills', 'PixelSplitter-Bold.ttf', res(50,RESOLUTION_SETTING), (0,0,0), (255,0,0))
    # Pause Menu
    mainMenuButton = TextButton(res(680,RESOLUTION_SETTING), res(300,RESOLUTION_SETTING), 'Main Menu', 'PixelSplitter-Bold.ttf', res(40,RESOLUTION_SETTING), (255,255,255), (255,0,0))
    # MAIN MENU
    while gameState == 'mainmenu':
        # Pre-Event Code
        screen.fill((255,255,255))
        drawText(screen, 'PewDiePie', res(128,RESOLUTION_SETTING), res(790,RESOLUTION_SETTING), res(100,RESOLUTION_SETTING), (0,0,0))
        drawText(screen, 'The Last Stand', res(64,RESOLUTION_SETTING), res(900,RESOLUTION_SETTING), res(250,RESOLUTION_SETTING), (0,0,0))
        startButton.draw(screen)
        settingsButton.draw(screen)
        quitButton.draw(screen)
        gameLogo = getImage('Images/pewdiepieicon.png', res(900, RESOLUTION_SETTING), res(900,RESOLUTION_SETTING))
        screen.blit(gameLogo, (0,0))
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                setHovering(startButton)
                setHovering(settingsButton)
                setHovering(quitButton)
            if event.type == p.MOUSEBUTTONUP:
                if startButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'gamemenu'
                    main()
                if settingsButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'settings'
                    main()
                if quitButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'quit'
                    main()
        # Post-Event Code
        PREV_STATE = 'mainmenu'
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    # SETTINGS MENU
    while gameState == 'settings':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Fullscreen Settings
        drawText(screen, 'Fullscreen:', 40, res(200,RESOLUTION_SETTING), res(200,RESOLUTION_SETTING), (0,0,0))
        fullScreenOnButton.draw(screen)
        fullScreenOffButton.draw(screen)
        if FULLSCREEN == True:
            fullScreenOnButton.toggleOn()
            fullScreenOffButton.toggleOff()
        else:
            fullScreenOnButton.toggleOff()
            fullScreenOffButton.toggleOn()
        # Resolution Settings
        drawText(screen, 'Resolution:', 40, res(200,RESOLUTION_SETTING), res(300,RESOLUTION_SETTING), (0,0,0))
        lowResolutionButton.draw(screen)
        midResolutionButton.draw(screen)
        highResolutionButton.draw(screen)
        if RESOLUTION_SETTING == 0.8:
            lowResolutionButton.toggleOn()
            midResolutionButton.toggleOff()
            highResolutionButton.toggleOff()
        elif RESOLUTION_SETTING == 1:
            lowResolutionButton.toggleOff()
            midResolutionButton.toggleOn()
            highResolutionButton.toggleOff()
        elif RESOLUTION_SETTING == 1.2:
            lowResolutionButton.toggleOff()
            midResolutionButton.toggleOff()
            highResolutionButton.toggleOn()
        # FPS Settings
        drawText(screen, 'Max FPS:', 40, res(200,RESOLUTION_SETTING), res(400,RESOLUTION_SETTING), (0,0,0))
        lowFPS.draw(screen)
        midFPS.draw(screen)
        highFPS.draw(screen)
        if FPS_SETTING == 15:
            lowFPS.toggleOn()
            midFPS.toggleOff()
            highFPS.toggleOff()
        elif FPS_SETTING == 30:
            lowFPS.toggleOff()
            midFPS.toggleOn()
            highFPS.toggleOff()
        elif FPS_SETTING== 60:
            lowFPS.toggleOff()
            midFPS.toggleOff()
            highFPS.toggleOn()
        # Help Settings
        drawText(screen, 'Help:', 40, res(200, RESOLUTION_SETTING), res(500, RESOLUTION_SETTING), (0,0,0))
        helpOnButton.draw(screen)
        helpOffButton.draw(screen)
        if HELP == True:
            helpOnButton.toggleOn()
            helpOffButton.toggleOff()
        else:
            helpOnButton.toggleOff()
            helpOffButton.toggleOn()
        # Back
        backButton.draw(screen)
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEBUTTONUP:
                # Click Event for Full Screen Buttons
                if fullScreenOnButton.check(p.mouse.get_pos()):
                    click.play()
                    FULLSCREEN = True
                    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), p.FULLSCREEN)
                elif fullScreenOffButton.check(p.mouse.get_pos()):
                    click.play()
                    FULLSCREEN = False
                    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                # Click Event for Resolution Buttons
                if lowResolutionButton.check(p.mouse.get_pos()):
                    click.play()
                    RESOLUTION_SETTING = 0.8
                    WINDOW_WIDTH = 1280
                    WINDOW_HEIGHT = 720
                    if FULLSCREEN == True:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), p.FULLSCREEN)
                    else:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    main()
                elif midResolutionButton.check(p.mouse.get_pos()):
                    click.play()
                    RESOLUTION_SETTING = 1
                    WINDOW_WIDTH = 1600
                    WINDOW_HEIGHT = 900
                    if FULLSCREEN == True:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), p.FULLSCREEN)
                    else:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    main()
                elif highResolutionButton.check(p.mouse.get_pos()):
                    click.play()
                    RESOLUTION_SETTING = 1.2
                    WINDOW_WIDTH = 1920
                    WINDOW_HEIGHT = 1080
                    if FULLSCREEN == True:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), p.FULLSCREEN)
                    else:
                        screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    main()
                # Click Event for FPS Buttons
                if lowFPS.check(p.mouse.get_pos()):
                    click.play()
                    FPS_SETTING = 15
                    main()
                elif midFPS.check(p.mouse.get_pos()):
                    click.play()
                    FPS_SETTING = 30
                    main()
                elif highFPS.check(p.mouse.get_pos()):
                    click.play()
                    FPS_SETTING = 60
                    main()
                # Back Button
                if backButton.check(p.mouse.get_pos()):
                    gameState = PREV_STATE
                    main()
                # Click Event for Help Buttons
                if helpOnButton.check(p.mouse.get_pos()):
                    click.play()
                    HELP = True
                    main()
                elif helpOffButton.check(p.mouse.get_pos()):
                    click.play()
                    HELP = False
                    main()
                # Save
                game.save(getData())
            if event.type == p.MOUSEMOTION:
                if backButton.check(p.mouse.get_pos()):
                    backButton.toggleOn()
                else:
                    backButton.toggleOff()
        # Post-Event Code
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    while gameState == 'gamemenu':
        # Pre-Event Code
        screen.fill((255,255,255))
        upgradesButton.draw(screen)
        artifactsButton.draw(screen)
        skillsButton.draw(screen)
        if HELP:
            drawText(screen, 'This is the game menu.', res(20,RESOLUTION_SETTING), res(950,RESOLUTION_SETTING), res(100,RESOLUTION_SETTING), (255,128,128))
            drawText(screen, 'You can navigate the various features of the game with these buttons.', res(20,RESOLUTION_SETTING), res(650,RESOLUTION_SETTING), res(125,RESOLUTION_SETTING), (255,128,128))
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                if upgradesButton.check(p.mouse.get_pos()):
                    upgradesButton.toggleOn()
                else:
                    upgradesButton.toggleOff()
            if event.type == p.MOUSEBUTTONUP:
                pass
            if event.type == p.KEYUP:
                if event.key == K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
        # Post-Event Code
        PREV_STATE = 'gamemenu'
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    while gameState == 'pausemenu':
        # Pre-Event Code
        p.draw.rect(screen, (0,0,0), p.Rect(res(600,RESOLUTION_SETTING), res(100,RESOLUTION_SETTING), res(400, RESOLUTION_SETTING), res(700, RESOLUTION_SETTING)))
        mainMenuButton.draw(screen)
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                if upgradesButton.check(p.mouse.get_pos()):
                    upgradesButton.toggleOn()
                else:
                    upgradesButton.toggleOff()
            if event.type == p.MOUSEBUTTONUP:
                pass
            if event.type == p.KEYUP:
                if event.key == K_ESCAPE:
                    gameState = PREV_STATE
                    main()
        # Post-Event Code
        
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    
def getData():
    global FULLSCREEN, RESOLUTION_SETTING, FPS_SETTING, WINDOW_WIDTH, WINDOW_HEIGHT, HELP
    return [toNum(FULLSCREEN), int(RESOLUTION_SETTING*900), FPS_SETTING, toNum(HELP)]


setup()
main()