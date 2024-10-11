import pygame
from Mapa import *  # Aquí tienes tu mapa cargado

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((MAPA_ANCHO, MAPA_ALTO))

# Background
background = pygame.image.load('PNGs/background.png')

# Caption and icon
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load('PNGs/game.png')
pygame.display.set_icon(icon)

# Cargar la imagen de Pac-Man
pacman_img = pygame.image.load('PNGs/pacman.png')
pacman_Right_img = pygame.image.load('PNGs/pacmanRight.png')    #1
pacman_Left_img = pygame.image.load('PNGs/pacmanLeft.png')      #2
pacman_Up_img = pygame.image.load('PNGs/pacmanUp.png')          #3
pacman_Down_img = pygame.image.load('PNGs/pacmanDown.png')      #4

# Posición inicial de Pac-Man en el mapa (coordenadas de la celda)
pacman_x = 1  # Columna de la matriz
pacman_y = 1  # Fila de la matriz
# Velocidad de movimiento (en celdas)
velocidad = 1
#direccion: 1Left 2Right 3Up 4Down
direccion = 2

# Función para dibujar el mapa en pantalla
def dibujar_mapa(mapa):
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            color = (23, 56, 110) if celda.valor == 'pared' else (255, 255, 255)  # Azul para pared, blanco para otros
            pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

# Función para dibujar a Pac-Man en la celda correspondiente
def dibujar_pacman(pacman_x, pacman_y, n):
    # Convertir las coordenadas de la celda a coordenadas en píxeles
    pos_x = pacman_x * ANCHO_CELDA
    pos_y = pacman_y * ALTO_CELDA
    if (n == 1):
        screen.blit(pacman_Left_img, (pos_x, pos_y))
    if (n == 2):
        screen.blit(pacman_Right_img, (pos_x, pos_y))
    if (n == 3):
        screen.blit(pacman_Up_img, (pos_x, pos_y))
    if (n == 4):
        screen.blit(pacman_Down_img, (pos_x, pos_y))

# Game loop
running = True
while running:
    screen.fill((0, 124, 140))  # RGB
    screen.blit(background, (0, 0))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:  # pressing key up, down, left, right (movement)
            if event.key == pygame.K_LEFT and pacman_x > 0 and mapa[pacman_y][pacman_x - 1].valor != 'pared':  # Izquierda
                pacman_x -= velocidad
                direccion=1
            if event.key == pygame.K_RIGHT and pacman_x < len(mapa[0]) - 1 and mapa[pacman_y][
                pacman_x + 1].valor != 'pared':  # Derecha
                pacman_x += velocidad
                direccion=2
            if event.key == pygame.K_UP and pacman_y > 0 and mapa[pacman_y - 1][pacman_x].valor != 'pared':  # Arriba
                pacman_y -= velocidad
                direccion=3
            if event.key == pygame.K_DOWN and pacman_y < len(mapa) - 1 and mapa[pacman_y + 1][pacman_x].valor != 'pared':  # Abajo
                pacman_y += velocidad
                direccion=4




    # Función para dibujar el mapa en pantalla
    def dibujar_mapa(mapa):
        for y, fila in enumerate(mapa):
            for x, celda in enumerate(fila):
                color = (23, 56, 110) if celda.valor == 'pared' else (
                255, 255, 255)  # Azul para pared, blanco para otros
                pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

    # Mover Pac-Man con las teclas de flechas



    # Dibujar el mapa y a Pac-Man
    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)

    # Actualizar la pantalla
    pygame.display.flip()
