'''
Created on Mar 13, 2019

@author: antho
'''

import pygame as p
import time
import math
import threading
import sys

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
    
    def __init__(self, name, tier, level, x, y, idleImage, attackImage, lockedImage, location):
        
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
        self.lockedImage = lockedImage
        
        self.upgradeCost = int(math.pow(50, self.tier-1)*math.pow(2,math.pow(self.level,0.5))*(self.level+1))
        self.dps = int(math.pow(10, (self.tier+2*(self.level//1000)-1))*math.pow(2,math.pow(self.level,0.3))*math.pow(self.level,math.pow(self.tier,0.1)+0.3))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self, mSecs):
        if int(time.perf_counter()*1000)%(mSecs*2) <= mSecs:
            self.image = self.animationImage1
            self.x = self.xInit
            self.y = self.yInit
        else:
            self.image = self.animationImage2
            if self.loc == 'right' or self.loc == 'r':
                self.x = self.xInit - self.animationImage2.get_width() + self.animationImage1.get_width()
            self.y = self.yInit
    
    def getUpgradeCost(self, lv):
        return int(math.pow(50, self.tier-1)*math.pow(2,math.pow(lv,0.5))*(lv+1))
    
    def getTotalUpgradeCost(self, amount):
        totalUpgradeCost = 0
        for i in range(amount):
            totalUpgradeCost += self.getUpgradeCost(self.level+i)
        return totalUpgradeCost
    
    def getDPS(self):
        return int(math.pow(10, (self.tier+2*(self.level//1000)-1))*math.pow(2,math.pow(self.level,0.3))*math.pow(self.level,math.pow(self.tier,0.1)+0.3))
            
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
        
        self.alive = True
        self.toDraw = True
        self.alpha = 255
        self.health = int((math.pow(self.tier, 2)*math.pow(2, math.pow(self.level,.35))*self.level+math.pow(self.level,2)+7)*self.level)
        self.value = int(self.tier*math.pow(5, self.tier-1)*math.pow(2, math.pow(self.level, 0.3))*(self.level/2)+(self.level-2))
        
    def draw(self, screen):
        if self.toDraw:
            blit_alpha(screen, self.image, (self.x, self.y), self.alpha)
    
    def update(self, mSecs):
        if self.alive:
            if int(time.perf_counter()*1000)%(mSecs*2) <= mSecs:
                self.image = self.animationImage1
                self.y = self.yInit
            else:
                self.image = self.animationImage2
                self.y = self.yInit + (self.animationImage1.get_height()-self.animationImage2.get_height())*2
            if int(time.perf_counter()*1000)%(mSecs) >= mSecs//2 and int(time.perf_counter()*1000)%(mSecs) <= mSecs//2 + 100:
                return time.perf_counter()
        return 0
    
    def checkAlive(self, FPS):
        if not self.alive:
            if self.alpha > 0:
                self.alpha -= 10*(60//FPS)
            else:
                self.toDraw = False
                return True
        
    def wobble(self, currentTime, mult):
        if self.alive:
            if time.perf_counter()-currentTime <= 0.025:
                self.x = self.xInit - mult
                return False
            elif time.perf_counter()-currentTime <= 0.05:
                self.x = self.xInit + mult
                return False
            else:
                self.x = self.xInit
                return True
            
    def takeDamage(self, damage):
        if self.health > damage:
            self.health -= damage
            self.alive = True
        else:
            self.health -= damage
            self.alive = False
    
    def check(self, pos):
        mouseX = pos[0]
        mouseY = pos[1]
        if mouseX > self.x and mouseX < (self.x+self.image.get_width()) and mouseY > self.y and mouseY < (self.y+self.image.get_height()):
            return True
        return False
    
    def getHealth(self):
        return int((math.pow(self.tier, 2)*math.pow(2, math.pow(self.level,.35))*self.level+math.pow(self.level,2)+7)*self.level)
    
    def getValue(self):
        return int(self.tier*math.pow(5, self.tier-1)*math.pow(2, math.pow(self.level, 0.3))*(self.level/2)+(self.level-1))

class Artifact:
    
    def __init__(self, name, level, artifactType, normalImage, hoverImage, lockedImage):
        
        self.name = name
        self.level = level
        self.artifactType = artifactType
        self.normalImage = normalImage
        self.hoverImage = hoverImage
        self.lockedImage = lockedImage
        self.image = normalImage
        
        self.maxLevel = sys.maxsize
        self.damageMult = 50*self.level
        self.effectMult = 10*self.level
        self.upgradeCost = int(math.pow(self.level,2)*math.pow(1.1, math.pow(self.level,.5)))
        self.desc = ''
        
        self.isMaxed = (self.level >= self.maxLevel)
        
        if self.artifactType == 'subs':
            self.upgradeCost = int(math.pow(self.level,2)*math.pow(1.5, self.level))
            self.desc = 'Subscribers'
        if self.artifactType == 'click':
            self.effectMult = int(math.pow(self.effectMult, 1.2))
            self.desc = 'Click Damage'
        if self.artifactType == 'numbots':
            self.maxLevel = 5
            self.damageMult = int(50*math.pow(self.level,2))
            self.effectMult = int(100 - 10*self.level)
            cost = '399'
            for i in range(self.level):
                cost += '9'
            self.upgradeCost = int(cost)
            self.desc = 'Bots Per Level'
        if self.artifactType == 'herochc':
            self.effectMult = int((1 - math.pow(1.1, -self.level))*100)
            self.desc = 'Hero Crit Chance'
        if self.artifactType == 'herochd':
            self.desc = 'Hero Crit Damage'
        if self.artifactType == 'artifact':
            self.desc = 'Artifact Damage'
        if self.artifactType == 'money':
            self.desc = 'Monetization'
        if self.artifactType == 'splash':
            self.maxLevel = 50
            self.effectMult = 2*self.level
            self.desc = 'Splash Damage'
        if self.artifactType == 'hero':
            self.desc = 'Hero Damage'
            
    def getDamageMult(self, level):
        temp = Artifact(self.name, level, self.artifactType, self.normalImage, self.hoverImage, self.lockedImage)
        return temp.damageMult
    
    def getEffectMult(self, level):
        temp = Artifact(self.name, level, self.artifactType, self.normalImage, self.hoverImage, self.lockedImage)
        return temp.effectMult
    
    def getUpgradeCost(self, level):
        temp = Artifact(self.name, level, self.artifactType, self.normalImage, self.hoverImage, self.lockedImage)
        return temp.upgradeCost
    
    def getTotalUpgradeCost(self, amount):
        totalUpgradeCost = 0
        for i in range(amount):
            totalUpgradeCost += self.getUpgradeCost(self.level+i)
        return totalUpgradeCost
    
    def draw(self, screen, x, y):
        screen.blit(self.image, (x,y))
        
    def check(self, pos):
        mouseX = pos[0]
        mouseY = pos[1]
        if mouseX > self.x and mouseX < (self.x+self.image.get_width()) and mouseY > self.y and mouseY < (self.y+self.image.get_height()):
            return True
        return False

        
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = p.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

