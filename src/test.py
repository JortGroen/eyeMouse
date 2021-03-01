#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:33:26 2021

@author: djoghurt
"""
import pygame
import sys
import random
import pyautogui

screenSize = pyautogui.size()

def game_init():
    #screen = pygame.display.set_mode(screenSize)
    screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (255,0,0), (50,50), 20)
    pygame.display.flip()
    return screen
    
def create_dot(screen):
    x = random.randint(1, screenSize.width)
    y = random.randint(1, screenSize.height)
    pygame.draw.circle(screen, (255,0,0), (x,y), 20)
    return screen

def game_update(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space")
                screen.fill((255,255,255))
                screen = create_dot(screen)
                pygame.display.flip()
                
            elif event.key == pygame.K_q:
                print("quit")
                return False
    return True

def main():
    screen = game_init()
    while True:
        if not game_update(screen):
            return



pygame.init()
main()
pygame.quit()
