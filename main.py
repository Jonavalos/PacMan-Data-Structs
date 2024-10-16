from pickle import GLOBAL

import pygame
from pygame import mixer
from pygame.examples.testsprite import Static

from Mapa import *  # Aquí tienes tu mapa cargado
n=0
# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((MAPA_ANCHO, MAPA_ALTO))

# Background
background = pygame.image.load('PNGs/background.png')
background_inicio = pygame.image.load('PNGs/background_inicio.png')
background_wwcd = pygame.image.load('PNGs/wwcd2.png')


# Obtener las dimensiones de las imagenes para centrarlas

image_rect = background_inicio.get_rect()
# Calcular la posición para centrar la imagen
inicio_x = (MAPA_ANCHO - image_rect.width) // 2  # Posición X
inicio_y = (MAPA_ALTO - image_rect.height) // 2  # Posición Y

image_rect2 = background_wwcd.get_rect()
# Calcular la posición para centrar la imagen
wwcd_x = (MAPA_ANCHO - image_rect2.width) // 2  # Posición X
wwcd_y = (MAPA_ALTO - image_rect2.height) // 2  # Posición Y

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

# Posicion inicial de Pac-Man en el mapa (coordenadas de la celda)
pacman_x = 1  # Columna de la matriz
pacman_y = 1  # Fila de la matriz
# Velocidad de movimiento (en celdas)
velocidad = 1
# Dirección: 1Left 2Right 3Up 4Down
direccion = 2

# Diccionario para almacenar las posiciones de las celdas que no sean 'pared'. Para no tener que recorrer toda la matiz en cada vuelta del while
#me parece que deberia ir dentro del inicializar_mapa pero no se si es posible que otros metodos accedan al diccionario, ver luego.
# Inicializar dos diccionarios
diccionario_celdas_puntos= {}        #se modifica con cada movimiento de pacman, elimina por donde va comiendo pacman
diccionario_celdas_items = {}        #No se modifica. Para tener presente las celdas en las que se puede mover y pueden haber items


def inicializar_mapa(mapa):

    for y, fila in enumerate(mapa): #para no tener que recorrer toda la matriz verificando si hay puntos. Se eliminan conforme va comiendo pacman
        for x, celda in enumerate(fila):
            if celda.valor == 'punto':
                diccionario_celdas_puntos[(x, y)] = 'punto'
                diccionario_celdas_items[(x, y)] = 'punto'
            elif celda.valor == 'fruta':
                diccionario_celdas_items[(x, y)] = 'fruta'




# Función para dibujar el mapa en pantalla
def dibujar_mapa(mapa):
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):

            # Cambiar color basado en el valor del olor
            if celda.valor == 'pared':
                color = (23, 56, 110)  # Azul para pared
            else:
                color = (0, 0, 0)
                if celda.olor >= 1:
                    color = (214, 90, 104)
                if 10 < celda.olor < 20:
                    color = (255, 46, 70)
                if celda.olor >= 20:
                    color = (255, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))


            # Comprobar si la celda es 'vacio' y no dibujar nada
            if celda.valor == 'vacio':
                continue  # Saltar al siguiente ciclo si la celda es 'vacio'

            # Cambiar color basado en el valor del olor
            if celda.valor == 'pared':
                color = (23, 56, 110)  # Azul para pared
                pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
            else:
                color = (0, 0, 0)
                if celda.olor >= 1:
                    color = (214, 90, 104)
                if 10 < celda.olor < 20:
                    color = (255, 46, 70)
                if celda.olor >= 20:
                    color = (255, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

                # Dibujar el punto si corresponde
                if celda.valor == 'punto':
                    punto_color = (255, 255, 255)  # Blanco para el punto
                    punto_size = ANCHO_CELDA // 4  # Tamaño del punto
                    # Calcular la posicion centrada del cuadrito dentro de la celda
                    punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2) - (punto_size // 2)
                    punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2) - (punto_size // 2)
                    # Dibujar el cuadrito
                    pygame.draw.rect(screen, punto_color, pygame.Rect(punto_x, punto_y, punto_size, punto_size))


def is_victoria(mapa): #Verifica si ya no quedan puntos (si ya ganó). Se va a optimizar mas adelante, por ahora dejar asi.
    # Verificar si quedan celdas con puntos
    if not diccionario_celdas_puntos:
        return True
    return False

# Dibujar a PACMAN en la celda correspondiente (GPT)
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
    for (x,y) in diccionario_celdas_items.keys():
        mapa[y][x].decrementar_olor()


# Mover a PACMAN y actualizar el valor de la celda
def mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad):
    if direccion == 1 and pacman_x > 0 and mapa[pacman_y][pacman_x - 1].valor != 'pared':  # Izquierda
        pacman_x -= velocidad
    if direccion == 2 and pacman_x < len(mapa[0]) - 1 and mapa[pacman_y][pacman_x + 1].valor != 'pared':  # Derecha
        pacman_x += velocidad
    if direccion == 3 and pacman_y > 0 and mapa[pacman_y - 1][pacman_x].valor != 'pared':  # Arriba
        pacman_y -= velocidad
    if direccion == 4 and pacman_y < len(mapa) - 1 and mapa[pacman_y + 1][pacman_x].valor != 'pared':  # Abajo
        pacman_y += velocidad

    # Cuando pasa PACMAN, actualiza valor, eliminca del diccionario y hace sonido de CHOMP (suena horrible pero es lo que hay)
    pos_actual = (pacman_x, pacman_y)
    if pos_actual in diccionario_celdas_puntos:
        mapa[pacman_y][pacman_x].valor = 'vacio'
        del diccionario_celdas_puntos[pos_actual]  # elimina solo del diccionario de puntos
        # sonido de chomp
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

    pos_actual = (pacman_x, pacman_y)
    if pos_actual in diccionario_celdas_puntos:
        mapa[pacman_y][pacman_x].valor = 'vacio'
        del diccionario_celdas_puntos[pos_actual]  # elimina solo del diccionario de puntos


    #TELEPORT (ENDER PEARLLL)
    if pacman_x == 0 and pacman_y == 12:
        print("TP")
        pos_tp = (25, 12)
        pos_previa_tp = (26, 12) #en realidad es la posicion siguiente, pero con respecto al pacman es la que le queda de espaldas
        if pos_tp in diccionario_celdas_puntos:
            pacman_x = 25
            # xy-> 25,12 y 26,12 vacio en tp
            mapa[pacman_y][pacman_x].valor = 'vacio'
            mapa[pacman_y][pacman_x+1].valor = 'vacio'
            del diccionario_celdas_puntos[pos_tp]
            del diccionario_celdas_puntos[pos_previa_tp]
    if pacman_x == 26 and pacman_y == 12:
        print("TP")
        pos_tp = (1, 12)
        pos_previa_tp = (0, 12)
        if pos_tp in diccionario_celdas_puntos:
            pacman_x = 1
            # xy-> 1,12 y 0,12 vacio en tp
            mapa[pacman_y][pacman_x].valor = 'vacio'
            mapa[pacman_y][pacman_x-1].valor = 'vacio'
            del diccionario_celdas_puntos[pos_tp]
            del diccionario_celdas_puntos[pos_previa_tp]

    # Dibujar el mapa y a PACMAN
    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)
    n+=1
    print(mapa[pacman_y][pacman_x].id, mapa[pacman_y-1][pacman_x-1].olor, mapa[pacman_y][pacman_x].olor, n, pacman_x, pacman_y)

    if is_victoria(mapa):
        screen.fill((255, 255, 255))  # RGB
        screen.blit(background_wwcd, (inicio_x, inicio_y))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False


    # Actualizar la pantalla
    pygame.display.flip()
    #controlar velocidad
    pygame.time.delay(200)
