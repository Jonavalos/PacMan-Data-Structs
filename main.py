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
background_inicio = pygame.image.load('PNGs/background_inicio.png')

#Pantalla de inicio
# Obtener las dimensiones de la imagen
image_rect = background_inicio.get_rect()
# Calcular la posición para centrar la imagen
inicio_x = (MAPA_ANCHO - image_rect.width) // 2  # Posición X
inicio_y = (MAPA_ALTO - image_rect.height) // 2  # Posición Y

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

def inicializar_mapa(mapa):
    for fila in mapa:
        for celda in fila:
            if celda.valor != 'pared':  # Si no es pared
                celda.valor = 'punto'   # Iniciar con 'punto'
    #y, x. El spawn de los fantasmas va sin puntos
    mapa[9][13].valor = 'vacio'
    mapa[10][12].valor = 'vacio'
    mapa[10][13].valor = 'vacio'
    mapa[10][14].valor = 'vacio'
    mapa[11][12].valor = 'vacio'
    mapa[11][13].valor = 'vacio'
    mapa[11][14].valor = 'vacio'


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

            if celda.valor == 'punto':
                punto_color = (255, 255, 255)  # Blanco para el punto
                punto_size = ANCHO_CELDA // 4  # Tamaño del punto
                # Calcular la posición centrada del cuadrito dentro de la celda
                punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2) - (punto_size // 2)
                punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2) - (punto_size // 2)
                # Dibujar el cuadrito
                pygame.draw.rect(screen, punto_color, pygame.Rect(punto_x, punto_y, punto_size, punto_size))


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


# Función para mover a Pac-Man y actualizar el valor de la celda
def mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad):
    if direccion == 1 and pacman_x > 0 and mapa[pacman_y][pacman_x - 1].valor != 'pared':  # Izquierda
        pacman_x -= velocidad
    if direccion == 2 and pacman_x < len(mapa[0]) - 1 and mapa[pacman_y][pacman_x + 1].valor != 'pared':  # Derecha
        pacman_x += velocidad
    if direccion == 3 and pacman_y > 0 and mapa[pacman_y - 1][pacman_x].valor != 'pared':  # Arriba
        pacman_y -= velocidad
    if direccion == 4 and pacman_y < len(mapa) - 1 and mapa[pacman_y + 1][pacman_x].valor != 'pared':  # Abajo
        pacman_y += velocidad

    # Cambiar el valor de la celda a 'vacio' si Pac-Man pasa por una celda con 'punto'
    if mapa[pacman_y][pacman_x].valor == 'punto':
        mapa[pacman_y][pacman_x].valor = 'vacio'
        #sonido de chomp
        mixer.music.load('musica/pacman_chomp2.wav')
        mixer.music.play()

    return pacman_x, pacman_y


# Inicializar el mapa con 'punto' en celdas no pared
inicializar_mapa(mapa)


mixer.music.load('musica/pacman_beginning.wav')
mixer.music.play()
screen.fill((255, 255, 255))  # RGB
screen.blit(background_inicio, (inicio_x, inicio_y))
pygame.display.flip()
pygame.time.wait(4000)
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

    # Mover Pac-Man y actualizar el mapa
    pacman_x, pacman_y = mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad)

    # Incrementar el olor de la celda actual de Pac-Man
    mapa[pacman_y][pacman_x].incrementar_olor()

    # Reducir el olor de todas las celdas en cada iteración
    reducir_olor(mapa)

    #teleport
    if pacman_x == 0 and pacman_y == 12:
        print("TP")
        pacman_x = 25
        # 25,12 y 26,12 vacio en tp
        mapa[pacman_y][pacman_x].valor = 'vacio'
        mapa[pacman_y][pacman_x+1].valor = 'vacio'

    if pacman_x == 26 and pacman_y == 12:
        print("TP")
        pacman_x = 1
        mapa[pacman_y][pacman_x].valor = 'vacio'
        mapa[pacman_y][pacman_x-1].valor = 'vacio'

    # Dibujar el mapa y a Pac-Man
    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)
    n+=1
    print(mapa[pacman_y][pacman_x].id, mapa[pacman_y-1][pacman_x-1].olor, mapa[pacman_y][pacman_x].olor, n, pacman_x, pacman_y)

    # Actualizar la pantalla
    pygame.display.flip()
    #controlar velocidad
    pygame.time.delay(200)
