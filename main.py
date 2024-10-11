import math

import pygame
import random

# Initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((1000, 750))

# background
background = pygame.image.load('background.png')

# caption and icon
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load('game.png')
pygame.display.set_icon(icon)



# game loop
running = True
while running:  # agarra todos los eventos ingame uno por uno en el for y checkea si le dio a quit

    screen.fill((0, 124, 140))  # RGB
    screen.blit(background, (0, 0))  # background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False















print ("hello world!")