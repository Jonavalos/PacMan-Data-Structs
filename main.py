import pygame
from pygame import mixer
from Mapa import *  # Aquí tienes tu mapa cargado
n=0
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
# Dirección: 1Left 2Right 3Up 4Down
direccion = 2

# Función para dibujar el mapa en pantalla
def dibujar_mapa(mapa):
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            # Cambiar color basado en el valor del olor
            if celda.valor == 'pared':
                color = (23, 56, 110)  # Azul para pared
            else:
                color = (0,0,0)
                if celda.olor >= 1:
                    color = (214, 90, 104)
                if 10 < celda.olor < 20:
                    color = (255, 46, 70)
                if celda.olor >= 20:
                    color = (255, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

# Función para dibujar a Pac-Man en la celda correspondiente
def dibujar_pacman(pacman_x, pacman_y, direccion):
    # Convertir las coordenadas de la celda a coordenadas en píxeles
    pos_x = pacman_x * ANCHO_CELDA
    pos_y = pacman_y * ALTO_CELDA
    if direccion == 1:
        screen.blit(pacman_Left_img, (pos_x, pos_y))
    if direccion == 2:
        screen.blit(pacman_Right_img, (pos_x, pos_y))
    if direccion == 3:
        screen.blit(pacman_Up_img, (pos_x, pos_y))
    if direccion == 4:
        screen.blit(pacman_Down_img, (pos_x, pos_y))

# Función para reducir el olor de todas las celdas
def reducir_olor(mapa):
    for fila in mapa:
        for celda in fila:
            celda.decrementar_olor()  # Llama una función para reducir el olor en cada iteración
# Función para mover a Pac-Man
def mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad):
    if direccion == 1 and pacman_x > 0 and mapa[pacman_y][pacman_x - 1].valor != 'pared':  # Izquierda
        pacman_x -= velocidad
    if direccion == 2 and pacman_x < len(mapa[0]) - 1 and mapa[pacman_y][pacman_x + 1].valor != 'pared':  # Derecha
        pacman_x += velocidad
    if direccion == 3 and pacman_y > 0 and mapa[pacman_y - 1][pacman_x].valor != 'pared':  # Arriba
        pacman_y -= velocidad
    if direccion == 4 and pacman_y < len(mapa) - 1 and mapa[pacman_y + 1][pacman_x].valor != 'pared':  # Abajo
        pacman_y += velocidad
    return pacman_x, pacman_y

mixer.music.load('musica/pacman_beginning.wav')
mixer.music.play()

# Game loop
running = True
while running:
    screen.fill((0, 124, 140))  # RGB
    screen.blit(background, (0, 0))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # pressing key up, down, left, right (movement)
            if event.key == pygame.K_LEFT:
                direccion = 1
            if event.key == pygame.K_RIGHT:
                direccion = 2
            if event.key == pygame.K_UP:
                direccion = 3
            if event.key == pygame.K_DOWN:
                direccion = 4

    # Mover a Pac-Man automáticamente en la dirección actual
    pacman_x, pacman_y = mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad)

    # Incrementar el olor de la celda actual de Pac-Man
    mapa[pacman_y][pacman_x].incrementar_olor()

    # Reducir el olor de todas las celdas en cada iteración
    reducir_olor(mapa)

    #teleport
    if pacman_x == 0 and pacman_y == 12:
        print("TP")
        pacman_x = 25
    if pacman_x == 26 and pacman_y == 12:
        print("TP")
        pacman_x = 1

    # Dibujar el mapa y a Pac-Man
    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)
    n+=1
    print(mapa[pacman_y][pacman_x].id, mapa[pacman_y-1][pacman_x-1].olor, mapa[pacman_y][pacman_x].olor, n, pacman_x, pacman_y)

    # Actualizar la pantalla
    pygame.display.flip()
    #controlar velocidad
    pygame.time.delay(200)
