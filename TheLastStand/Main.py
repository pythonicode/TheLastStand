'''
Created on Mar 15, 2019

@author: antho
'''

from Global import *
from Classes import *

import pygame as p
import random
import math
import time


# Set up the Window
def setup():  
    global gameState, clock, screen, game
    global FULLSCREEN, RESOLUTION_SETTING, FPS_SETTING, WINDOW_WIDTH, WINDOW_HEIGHT, HELP, MONEY, TOKENS, STAGE, HERO_INDEX, HERO_LEVELS
    p.init()
    # RETRIEVING DATA FROM SAVE FILE
    game = GameData('Saves/Save.txt')
    data = game.data
    FULLSCREEN = toBoolean(data[0])
    RESOLUTION_SETTING = data[1]/900
    WINDOW_WIDTH = res(1600)
    WINDOW_HEIGHT = res(900)
    FPS_SETTING = data[2]
    HELP = toBoolean(data[3])
    MONEY = data[4]
    TOKENS = data[5]
    STAGE = data[6]
    HERO_INDEX = data[7]
    HERO_LEVELS = []
    for i in range(20):
        HERO_LEVELS.append(data[i+8])
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
    global FULLSCREEN, RESOLUTION_SETTING, FPS_SETTING, WINDOW_WIDTH, WINDOW_HEIGHT, HELP, PREV_STATE, MONEY, TOKENS, STAGE, HERO_INDEX, HERO_LEVELS
    # Misc Objects
    click = p.mixer.Sound('Sounds/click.wav')
    helpColor = (255,128,128)
    attackTime = time.clock()
    checkAliveTime = time.clock()
    # Main Menu Objects
    startButton = TextButton(res(1120), res(450), 'Play', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    settingsButton = TextButton(res(1070+(res(40)-40)), res(550), 'Settings', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    quitButton = TextButton(res(1120), res(650), 'Exit', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    # Settings Objects
    fullScreenOnButton = TextButton(res(700), res(200), 'On', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    fullScreenOffButton = TextButton(res(1200), res(200), 'Off', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    lowResolutionButton = TextButton(res(600), res(300), '1280x720', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    midResolutionButton = TextButton(res(900), res(300), '1600x900', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    highResolutionButton = TextButton(res(1200), res(300), '1920x1080', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    lowFPS = TextButton(res(675), res(400), '15', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    midFPS = TextButton(res(975), res(400), '30', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    highFPS = TextButton(res(1275), res(400), '60', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    helpOnButton = TextButton(res(700), res(500), 'On', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    helpOffButton = TextButton(res(1200), res(500), 'Off', 'PixelSplitter-Bold.ttf', 40, (0,0,0), (255,0,0))
    # Game Objects
    heroesButton = TextButton(res(60), res(250), 'Heroes', 'PixelSplitter-Bold.ttf', res(50), (0,0,0), (255,0,0))
    artifactsButton = TextButton(res(1280), res(250), 'Artifacts', 'PixelSplitter-Bold.ttf', res(50), (0,0,0), (255,0,0))
    skillsButton = TextButton(res(25), res(650), 'Abilities', 'PixelSplitter-Bold.ttf', res(50), (0,0,0), (255,0,0))
    prestigeButton = TextButton(res(1295), res(650), 'Prestige', 'PixelSplitter-Bold.ttf', res(50), (0,0,0), (255,0,0))
    # Titans
    titan1 = Titan(STAGE, 1, res(500), res(200), resImage(getImage('Images/tseriesbot1_a.png')), resImage(getImage('Images/tseriesbot1_b.png')))
    titans = [titan1]
    # Heroes
    pewdiepieHero = Hero('PewDiePie', 1, HERO_LEVELS[0], res(425), res(380), resImage(getImage('Images/pewdiepie.png')), resImage(getImage('Images/pewdiepie_attack.png')), 'left')
    mrbeastHero = Hero('Mr. Beast', 2, HERO_LEVELS[1], res(1130), res(280), resImage(getImage('Images/mrbeast.png')), resImage(getImage('Images/mrbeast_attack.png')), 'right')
    marziaHero = Hero('Marzia', 3, HERO_LEVELS[2], res(470), res(600), resImage(getImage('Images/marzia.png')), resImage(getImage('Images/marzia_attack.png')), 'left')
    jackHero = Hero('Jack Septic Eye', 4, HERO_LEVELS[3], res(1150), res(500), resImage(getImage('Images/jack.png')), resImage(getImage('Images/jack_attack.png')), 'right')
    markiplierHero = Hero('Markiplier', 5, HERO_LEVELS[4], res(400), res(500), resImage(getImage('Images/markiplier.png')), resImage(getImage('Images/markiplier_attack.png')), 'left')
    heroes = [pewdiepieHero, mrbeastHero, marziaHero, jackHero, markiplierHero]
    # Pause Menu
    mainMenuButton = TextButton(res(680), res(300), 'Main Menu', 'PixelSplitter-Bold.ttf', res(40), (255,255,255), (255,0,0))
    settingsButton2 = TextButton(res(694), res(400), 'Settings', 'PixelSplitter-Bold.ttf', res(40), (255,255,255), (255,0,0))
    quitButton2 = TextButton(res(745), res(500), 'Exit', 'PixelSplitter-Bold.ttf', res(40), (255,255,255), (255,0,0))
    # Back Button 
    backButton = ImageButton(res(50), res(750), resImage(getImage('Images/back_arrow.png')), resImage(getImage('Images/back_arrow_hover.png')))
    # Right Button
    rightButton = ImageButton(res(1240), res(400), resImage(getImage('Images/right_arrow.png')), resImage(getImage('Images/right_arrow_hover.png')))
    # Left Button
    leftButton = ImageButton(res(300), res(400), resImage(getImage('Images/left_arrow.png')), resImage(getImage('Images/left_arrow_hover.png')))
    # MAIN MENU
    while gameState == 'mainmenu':
        # Pre-Event Code
        screen.fill((255,255,255))
        drawText(screen, 'PewDiePie', res(128), res(790), res(100), (0,0,0))
        drawText(screen, 'The Last Stand', res(64), res(900), res(250), (0,0,0))
        startButton.draw(screen)
        settingsButton.draw(screen)
        quitButton.draw(screen)
        gameLogo = getImage('Images/pewdiepieicon.png', res(900), res(900))
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
                    gameState = 'game'
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
        drawText(screen, 'Fullscreen:', 40, res(200), res(200), (0,0,0))
        fullScreenOnButton.draw(screen)
        fullScreenOffButton.draw(screen)
        if FULLSCREEN == True:
            fullScreenOnButton.toggleOn()
            fullScreenOffButton.toggleOff()
        else:
            fullScreenOnButton.toggleOff()
            fullScreenOffButton.toggleOn()
        # Resolution Settings
        drawText(screen, 'Resolution:', 40, res(200), res(300), (0,0,0))
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
        drawText(screen, 'Max FPS:', 40, res(200), res(400), (0,0,0))
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
        drawText(screen, 'Help:', 40, res(200), res(500), (0,0,0))
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
    while gameState == 'game':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Menu Buttons
        heroesButton.draw(screen)
        artifactsButton.draw(screen)
        skillsButton.draw(screen)
        prestigeButton.draw(screen)
        # Game Screen
        p.draw.rect(screen, (0,0,0), p.Rect(res(340), 0, res(920), res(920)))
        p.draw.rect(screen, (255,255,255), p.Rect(res(350), 0, res(900), res(900)))
        # Titans
        titan1.draw(screen)
        titan1.update(1000)
        if titan1.update(1000) > 0:
            attackTime = titan1.update(1000)
        # Heroes
        for hero in heroes:
            hero.draw(screen)
            hero.update(500)
        if HELP:
            pass
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                if heroesButton.check(p.mouse.get_pos()):
                    heroesButton.toggleOn()
                else:
                    heroesButton.toggleOff()
                if artifactsButton.check(p.mouse.get_pos()):
                    artifactsButton.toggleOn()
                else:
                    artifactsButton.toggleOff()
                if skillsButton.check(p.mouse.get_pos()):
                    skillsButton.toggleOn()
                else:
                    skillsButton.toggleOff()
                if prestigeButton.check(p.mouse.get_pos()):
                    prestigeButton.toggleOn()
                else:
                    prestigeButton.toggleOff()
            if event.type == p.MOUSEBUTTONUP:
                if heroesButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'heroes'
                    main()
                if artifactsButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'artifacts'
                    main()
                if skillsButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'skills'
                    main()
                if prestigeButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'prestige'
                    main()
                if titan1.check(p.mouse.get_pos()):
                    titan1.takeDamage(1)
                    checkAliveTime = time.clock()
                    attackTime = time.clock()
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
                if event.key == p.K_SPACE:
                    attackTime = time.clock()
        titan1.wobble(attackTime)
        titan1.checkAlive(checkAliveTime)
        # Post-Event Code
        PREV_STATE = 'game'
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    while gameState == 'pausemenu':
        # Pre-Event Code
        p.draw.rect(screen, (0,0,0), p.Rect(res(600), res(100), res(400), res(700)))
        p.draw.rect(screen, (255,255,255), p.Rect(res(700), res(250), res(200), res(5)))
        drawText(screen, 'PAUSED', res(80), res(625), res(120), (255,255,255))
        mainMenuButton.draw(screen)
        settingsButton2.draw(screen)
        quitButton2.draw(screen)
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                if mainMenuButton.check(p.mouse.get_pos()):
                    mainMenuButton.toggleOn()
                else:
                    mainMenuButton.toggleOff()
                if settingsButton2.check(p.mouse.get_pos()):
                    settingsButton2.toggleOn()
                else:
                    settingsButton2.toggleOff()
                if quitButton2.check(p.mouse.get_pos()):
                    quitButton2.toggleOn()
                else:
                    quitButton2.toggleOff()
            if event.type == p.MOUSEBUTTONUP:
                if mainMenuButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'mainmenu'
                    main()
                if settingsButton2.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'settings'
                    main()
                if quitButton2.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'quit'
                    main()
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    click.play()
                    gameState = PREV_STATE
                    main()
        # Post-Event Code
        
        # Update the display
        p.display.flip()
        clock.tick(FPS_SETTING)
    while gameState == 'heroes':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Help
        if HELP:
            pass
        # Heroes
        currentHero = heroes[HERO_INDEX]
        currentHeroText = getText(currentHero.name, 75, (0,0,0))
        screen.blit(currentHeroText, (res(800) - currentHeroText.get_width()//2, 100))
        screen.blit(p.transform.scale(currentHero.image, (currentHero.image.get_width()*4, currentHero.image.get_height()*4)), (res(800)-(currentHero.image.get_width()*2),(res(450)-(currentHero.image.get_height()*2))))
        # Other UI Images
        moneyImage = resImage(getImage('Images/money.png'))
        moneyText = getText(str(MONEY), res(70), (0,0,0))
        moneySurface = p.Surface((moneyImage.get_width()+moneyText.get_width()+20, moneyText.get_height()+10), p.SRCALPHA)
        moneySurface.blit(moneyImage, (0,(moneyText.get_height()-moneyImage.get_height())//2))
        moneySurface.blit(moneyText, (moneyImage.get_width()+20, 0))
        screen.blit(moneySurface, (res(1600) - moneySurface.get_width() - res(100), res(50)))
        # Buttons
        backButton.draw(screen)
        rightButton.draw(screen)
        leftButton.draw(screen)
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.MOUSEMOTION:
                if backButton.check(p.mouse.get_pos()):
                    backButton.toggleOn()
                else:
                    backButton.toggleOff()
                if rightButton.check(p.mouse.get_pos()):
                    rightButton.toggleOn()
                else:
                    rightButton.toggleOff()
                if leftButton.check(p.mouse.get_pos()):
                    leftButton.toggleOn()
                else:
                    leftButton.toggleOff()
            if event.type == p.MOUSEBUTTONUP:
                if backButton.check(p.mouse.get_pos()):
                    click.play()
                    gameState = 'game'
                    main()
                if rightButton.check(p.mouse.get_pos()):
                    click.play()
                    if HERO_INDEX + 1 < len(heroes):
                        HERO_INDEX += 1
                    else:
                        HERO_INDEX = 0
                if leftButton.check(p.mouse.get_pos()):
                    if HERO_INDEX > 0:
                        HERO_INDEX -= 1
                    else:
                        HERO_INDEX = len(heroes) - 1
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
        # Post-Event Code
        PREV_STATE = 'heroes'
        # Update the display
        clock.tick(FPS_SETTING)
        p.display.flip()
    while gameState == 'artifacts':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
        # Post-Event Code
        PREV_STATE = 'artifacts'
        # Update the display
        clock.tick(FPS_SETTING)
        p.display.flip()
    while gameState == 'skills':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
        # Post-Event Code
        PREV_STATE = 'skills'
        # Update the display
        clock.tick(FPS_SETTING)
        p.display.flip()
    while gameState == 'prestige':
        # Pre-Event Code
        screen.fill((255,255,255))
        # Events
        for event in p.event.get():
            # Quit Event
            if event.type == p.QUIT:
                gameState = 'quit'
            if event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    gameState = 'pausemenu'
                    main()
        # Post-Event Code
        PREV_STATE = 'prestige'
        # Update the display
        clock.tick(FPS_SETTING)
        p.display.flip()

'''
FUNCTIONS
'''

def setHovering(button):
    if button.check(p.mouse.get_pos()):
        button.toggleOn()
    else:
        button.toggleOff()
        
def drawText(screen, text, size, x, y, color):
    myfont = p.font.Font('Fonts/' + FONT_NAME, size)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(x,y))
    return textsurface

def getText(text, size, color):
    myfont = p.font.Font('Fonts/' + FONT_NAME, size)
    textsurface = myfont.render(text, False, color)
    return textsurface

def res(num):
    return int(num*RESOLUTION_SETTING)

def resImage(image):
    return p.transform.scale(image, (int(image.get_width()*RESOLUTION_SETTING), int(image.get_height()*RESOLUTION_SETTING)))

def getImage(path, *args):
    if len(args) == 2:
        return p.transform.scale(p.image.load(path).convert_alpha(), (args[0],args[1]))
    else:
        return p.image.load(path).convert_alpha()

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = p.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

def toNum(myBoolean):
    if myBoolean:
        return 1
    else:
        return 0

def toBoolean(myNum):
    if myNum == 1:
        return True
    else:
        return False
    
def prettyNum(num):
    if num < 1000:
        return str(num)
    elif num < 1000000000000000:
        if len(num)//3 == 0:
            return str(num[0])+'.'+str(num[1])+str(num[2])+'K'

def getData():
    data = [toNum(FULLSCREEN), int(RESOLUTION_SETTING*900), FPS_SETTING, toNum(HELP), MONEY, TOKENS, STAGE, HERO_INDEX]
    for lv in HERO_LEVELS:
        data.append(lv)
    return data


setup()
main()