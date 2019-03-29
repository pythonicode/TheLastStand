'''
Created on Mar 13, 2019

@author: antho
'''

import pygame as p
import time

class TextButton:
    
    '''
    Initialize the ToggleButton
    @param x: horizontal distance from the top left corner
    @param y: vertical distance from the top left corner
    @param text: text to be used for the button
    @param font: font name (as a string)
    @param size: text size to be used for the button
    @param color1: default button color
    @param color2: button color when toggled
    '''
    def __init__(self, x, y, text, font, size, color1, color2):
        self.myfont = p.font.Font('Fonts/' + font, size)
        self.textsurface = self.myfont.render(text, False, color1)
        self.x = x 
        self.y = y
        self.text = text
        self.c1 = color1
        self.c2 = color2
        self.on = False
        
    # Draw the Button
    def draw(self, screen):
        screen.blit(self.textsurface, (self.x, self.y))
        
    # Check if the button is pressed
    def check(self, pos):
        mouseX = pos[0]
        mouseY = pos[1]
        if mouseX > self.x and mouseX < (self.x+self.textsurface.get_width()) and mouseY > self.y and mouseY < (self.y+self.textsurface.get_height()):
            return True
        return False
    
    # Toggle the button
    def toggle(self):
        if self.on == False:
            self.textsurface = self.myfont.render(self.text, False, self.c2)
            self.on = True
        elif self.on == True:
            self.textsurface = self.myfont.render(self.text, False, self.c1)
            self.on = False
    
    # Toggle the button on (if off)    
    def toggleOn(self):
        self.textsurface = self.myfont.render(self.text, False, self.c2)
        self.on = True
      
    # Toggle the button off (if on)   
    def toggleOff(self):
        self.textsurface = self.myfont.render(self.text, False, self.c1)
        self.on = False

class ImageButton:
    
    def __init__(self, x, y, upImage, downImage): 
        self.x = x 
        self.y = y
        self.xInit = x
        self.yInit = y
        self.upImage= upImage
        self.downImage = downImage
        self.image = upImage
        self.up = True
        
    # Draw the Button
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    # Check if the button is pressed
    def check(self, pos):
        mouseX = pos[0]
        mouseY = pos[1]
        if mouseX > self.x and mouseX < (self.x+self.image.get_width()) and mouseY > self.y and mouseY < (self.y+self.image.get_height()):
            return True
        return False
    
    # Toggle the button
    def toggle(self):
        if self.up == False:
            self.image = self.upImage
            self.up = True
        elif self.up == True:
            self.image = self.downImage
            self.up = False
    
    # Toggle the button on (if off)    
    def toggleOn(self):
        self.image = self.downImage
        self.up = False
      
    # Toggle the button off (if on)   
    def toggleOff(self):
        self.image = self.upImage
        self.up = True   
        
class GameData:
    
    def __init__(self, path):
        with open(path) as f:
            lines = f.readlines()
            self.data = []
            for line in lines:
                if line != '\n':
                    self.data.append(int(line))
            f.close()
        if len(self.data) == 0:
            with open('Saves/DefaultSave.txt') as f:
                lines = f.readlines()
                for line in lines:
                    if line != '\n':
                        self.data.append(int(line))
            
    def save(self, data):
        with open('Saves/Save.txt', 'w') as f:
            stringArray = []
            for item in data:
                stringArray.append(str(item)+'\n')
            f.writelines(stringArray)
            f.close()


class Hero:
    
    def __init__(self, name, tier, level, x, y, idleImage, attackImage, location):
        
        self.name = name
        self.tier = tier
        self.level = level
        self.x = x
        self.y = y
        self.xInit = x
        self.yInit = y
        self.animationImage1 = idleImage
        self.animationImage2 = attackImage
        self.image = idleImage
        self.loc = location
        
        self.upgradeCost = int(200*(tier-1))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self, mSecs):
        if int(time.clock()*1000)%(mSecs*2) <= mSecs:
            self.image = self.animationImage1
            self.x = self.xInit
            self.y = self.yInit
        else:
            self.image = self.animationImage2
            if self.loc == 'right' or self.loc == 'r':
                self.x = self.xInit - self.animationImage2.get_width() + self.animationImage1.get_width()
            self.y = self.yInit
            
class Titan:
    
    def __init__(self, level, tier, x, y, image1, image2):
        
        self.level = level
        self.tier = tier
        self.x = x
        self.y = y
        self.xInit = x
        self.yInit = y
        
        self.animationImage1 = image1
        self.animationImage2 = image2
        self.image = self.animationImage1
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self, mSecs):
        if int(time.clock()*1000)%(mSecs*2) <= mSecs:
            self.image = self.animationImage1
            self.y = self.yInit
        else:
            self.image = self.animationImage2
            self.y = self.yInit + (self.animationImage1.get_height()-self.animationImage2.get_height())*2
        if int(time.clock()*1000)%(mSecs) >= mSecs//2 and int(time.clock()*1000)%(mSecs) <= mSecs//2 + 100:
            return time.clock()
        return 0
    
    def wobble(self, currentTime):
        if time.clock()-currentTime <= 0.025:
            self.x = self.xInit - 5
            return False
        elif time.clock()-currentTime <= 0.05:
            self.x = self.xInit + 5
            return False
        else:
            self.x = self.xInit
            return True
    
    def check(self, pos):
        mouseX = pos[0]
        mouseY = pos[1]
        if mouseX > self.x and mouseX < (self.x+self.image.get_width()) and mouseY > self.y and mouseY < (self.y+self.image.get_height()):
            return True
        return False




