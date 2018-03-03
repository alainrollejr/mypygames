# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 00:18:13 2018

@author: aro
"""

import pygame

import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)
clock = pygame.time.Clock()

''' vanaf hier wordt het interessant
'''
display_width = 800 # breedte
display_height = 600  # hoogte
beeldjes_per_seconde = 40

scherm = pygame.display.set_mode((display_width,display_height))


pygame.display.set_caption('boze Wesley game')



''' posities
'''
wesley_x = 0
wesley_y = 0


wesley = pygame.image.load('images/wesley_w283_h290_px.png')
wesley_b = wesley.get_width() # breedte in pixels
wesley_h = wesley.get_height() # hoogte in pixels

print(wesley_b)
print(wesley_h)


''' game loop
'''
stop = False
while not stop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        print(event)
        
    scherm.fill(green)
    scherm.blit(wesley,(wesley_x,wesley_y))
    
    
    wesley_x = wesley_x + 1
    print('wesley_x=' + str(wesley_x))
    
    ''' scherm vernieuwen
    '''
    pygame.display.update()
    clock.tick(beeldjes_per_seconde)
    
pygame.quit()
quit()