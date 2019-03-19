'''
Created on Mar 13, 2019

@author: antho
'''

import pygame as p

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
    
    def __init__(self, x, y, image): 
        self.x = x 
        self.y = y
        self.xInit = x
        self.yInit = y
        self.image = image
        self.widthInit = image.get_width()
        self.heightInit = image.get_height()
        self.on = False
        
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
        if self.on == False:
            self.image = p.transform.smoothscale(self.image, (int(self.widthInit*1.05), int(self.heightInit*1.05)))
            self.x = self.xInit-int(self.widthInit*.025)
            self.y = self.yInit-int(self.heightInit*.025)
            self.on = True
        elif self.on == True:
            self.image = p.transform.smoothscale(self.image, (self.widthInit, self.heightInit))
            self.x = self.xInit
            self.y = self.yInit
            self.on = False
    
    # Toggle the button on (if off)    
    def toggleOn(self):
        self.image = p.transform.smoothscale(self.image, (int(self.widthInit*1.05), int(self.heightInit*1.05)))
        self.x = self.xInit-int(self.widthInit*.025)
        self.y = self.yInit-int(self.heightInit*.025)
        self.on = True
      
    # Toggle the button off (if on)   
    def toggleOff(self):
        self.image = p.transform.smoothscale(self.image, (self.widthInit, self.heightInit))
        self.x = self.xInit
        self.y = self.yInit
        self.on = False   
        
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

'''
FUNCTIONS
'''

def setHovering(button):
    if button.check(p.mouse.get_pos()):
        button.toggleOn()
    else:
        button.toggleOff()
        
def drawText(screen, text, size, x, y, color):
    myfont = p.font.Font('Fonts/PixelSplitter-Bold.ttf', size)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(x,y))

def res(num, resolution_mult):
    return int(num*resolution_mult)

def getImage(path, width, height):
    return p.transform.scale(p.image.load(path), (width,height))

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


















