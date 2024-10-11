import math
import pygame
import random
from Mapa import *
# Dimensiones de las celdas y de la pantalla
ANCHO_CELDA = 36
ALTO_CELDA = 36
MAPA_ANCHO = 1000
MAPA_ALTO = 700


# Initialize pygame
pygame.init()


# create screen
screen = pygame.display.set_mode((MAPA_ANCHO, MAPA_ALTO))

# background
background = pygame.image.load('PNGs/background.png')

# caption and icon
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load('PNGs/game.png')
pygame.display.set_icon(icon)


# game loop
running = True
while running:  # agarra todos los eventos ingame uno por uno en el for y checkea si le dio a quit

    screen.fill((0, 124, 140))  # RGB
    screen.blit(background, (0, 0))  # background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Función para dibujar el mapa en pantalla
    def dibujar_mapa(mapa):
        for y, fila in enumerate(mapa):
            for x, celda in enumerate(fila):
                color = (0, 0, 255) if celda.valor == 'pared' else (255, 255, 255)  # Azul para pared, blanco para otros
                pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))



    # Llamar la función dentro de un bucle de Pygame
    dibujar_mapa(mapa)
    pygame.display.flip()  # Actualizar la pantalla

print ("hello world!")