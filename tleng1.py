import pygame
import os
pygame.font.init()
pygame.mixer.init()

from assets.scripts.colors import *

def errorChecking(var,typpe,name):
    #type in python
    if type(var) != typpe:
        raise Exception(f'The {name} variable is not {typpe}, change your var {name} to much type {typpe}.')
    #more or less than    

#initializing the game game engine
class Area():
    def __init__(self, Window, x=0, y=0, width=10, height=10, color=BLACK):
        self.rect = pygame.Rect(x-width/2,y-height/2,width,height)
        self.coreX = x
        self.coreY = y
        self.coreWidth = width
        self.coreHeight = height
        self.fill_color = color
        self.window = Window
    
    def n_color(self,ncolor):
        self.fill_color = ncolor

    def fill(self):
        pygame.draw.rect(self.window, self.fill_color, self.rect)

    def outline(self, thic=1, frame_color=BLACK):
        pygame.draw.rect(self.window, frame_color, pygame.Rect(self.rect.x - thic, self.rect.y - thic, self.rect.width + thic*2 , self.rect.height + thic*2), thic)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)
        
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Label(Area):
    def set_text(self, text, tsize=12, tcolor=BLACK, tbold=False):
        self.image = pygame.font.SysFont('verdana', tsize, tbold).render(text, True, tcolor)

    def drawtext(self, shift_x=0, shift_y=0,fillbfr=True):
        if fillbfr == True:
            self.fill()
        self.window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class Picture(Area):
    def __init__(self, mw, filename, x=0, y=0, width=10, height=10, animDict=None):
        Area.__init__(self,Window=mw, x=x, y=y, width=width, height=height, color=WHITE)
        self.image = pygame.image.load(filename)
        self.rotation = 0
        self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (width,height)), self.rotation)

        #for hitbox
        self.imageX = x-self.image.get_width()/2
        self.imageY = y-self.image.get_height()/2

        #declaring the variables for the animation function
        self.AnimData = 3
        self.animDict = {}
        self.animDictNewList = []
        self.animDictNameList = []

        #enabling the use of the animations
        if animDict != None:
            if type(animDict) == dict:
                self.animDict = animDict
                self.animDictNameList = animDict.keys()
                #looping through the whole dictianary to change them into pygame images
                for i in self.animDictNameList:
                    for j in range(len(animDict[i])):
                        self.new_image = pygame.image.load(animDict[i][j]).convert()
                        self.new_image = pygame.transform.rotate(pygame.transform.scale(self.new_image, (self.rect.width,self.rect.height)), self.rotation)
                        self.animDictNewList += [self.new_image]

                    self.animDict.update({i: self.animDictNewList})
                    self.animDictNewList = []
                    
            else:
                raise Exception(f"AnimDict isn't a dictionary, it's a {type(animDict)}.")   


    def display(self, picture=None, x=None, y=None):
        #if the user did not input anything its going to render in the pre-determined locations, if the user input anything it's going to render there.
        self.window.blit(pygame.image.load(picture) if picture != None else self.image, 
                    (self.rect.x if x == None else x
                    , self.rect.y if y == None else y))


    def hitbox(self, hitboxWidth, hitboxHeight):
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitboxWidth, hitboxHeight
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2
    
             
    def display_anim(self,animName,frames=12):
        # self.mw.blit(pygame.image.load(self.anim[self.AnimData]),(self.rect.x,self.rect.y))
        self.window.blit(self.animDict[animName][int(self.AnimData)],(self.imageX,self.imageY))
        #print(self.anim[int(self.AnimData)], len(self.anim), self.AnimData, frames, (self.rect.width,self.rect.height))   <----- debugging line

        
        self.AnimData += frames/FPS
        if self.AnimData >= len(self.animDict[animName]):
            self.AnimData = 0
    

    def transform_img(self,width,height,rotation,name = 'all'):
        #checking what the coder wants to change in the animations, either just one "slide" or everything or some but not all of the animations
        if name == 'all':
            for names in self.animDictNameList:
                for pic in range(len(self.animDict[names])):
                    self.animDict[names][pic] = pygame.transform.rotate(pygame.transform.scale( self.animDict[names][pic], (width, height)), rotation)

        elif type(name) == list:
            print("sorry i can't do that now")
            raise Exception('The programmer is too lazy to complete this task')

        elif type(name) == str and name == 'selfImage':
                pygame.transform.rotate(pygame.transform.scale( self.image, (width,height)), rotation)

        elif type(name) == str and len(self.animDict[name]) != 0:
            for pic in range(len(self.animDict[name])):
                self.animDict[name][pic] = pygame.transform.rotate(pygame.transform.scale( self.animDict[name][pic], (width, height)), rotation)
            pygame.transform.rotate(pygame.transform.scale( self.image, (width,height)), rotation)

        self.rect.width = width
        self.rect.height = height
        self.rotation = rotation
