from pickle import GLOBAL
import time
from Fantasma import *

import pygame
from pygame import mixer
from pygame.examples.testsprite import Static

from Mapa import *
n=0
fantasmasLiberados = 0
# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((MAPA_ANCHO, MAPA_ALTO))

# Background
background = pygame.image.load('PNGs/background.png')
background_inicio = pygame.image.load('PNGs/background_inicio.png')
background_wwcd = pygame.image.load('PNGs/wwcd2.png')

#vida y muerte
vidas = 3
fuente_vidas = pygame.font.Font(None, 36) #no se usa, es solo para representar vidas como texto
corazon_img = pygame.image.load('PNGs/corazon.png')
gameOver_img = pygame.image.load('PNGs/gameOver2.png')

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

#cargar imagen Blinky (rojo)
blinky_left = pygame.image.load('PNGs/BlinkyLeft.png')
blinky_right = pygame.image.load('PNGs/BlinkyRight.png')

#cargar imagen Pinky (rosa)
pinky_left = pygame.image.load('PNGs/PinkyLeft.png')
pinky_right = pygame.image.load('PNGs/PinkyRight.png')

#cargar imagen Inky (cyan)
inky_left = pygame.image.load('PNGs/InkyLeft.png')
inky_right = pygame.image.load('PNGs/InkyRight.png')

#cargar imagen Clyde (naranja)
clyde_left = pygame.image.load('PNGs/ClydeLeft.png')
clyde_right = pygame.image.load('PNGs/ClydeRight.png')

# Posicion inicial de Pac-Man en el mapa (coordenadas de la celda)
pacman_x = 14  # Columna de la matriz
pacman_y = 13  # Fila de la matriz
# Velocidad de movimiento (en celdas)
velocidad = 1
# Dirección: 1Left 2Right 3Up 4Down
direccion = 2

# Diccionario para almacenar las posiciones de las celdas que no sean 'pared'. Para no tener que recorrer toda la matiz en cada vuelta del while
# Inicializar dos diccionarios
diccionario_celdas_puntos= {}        #se modifica con cada movimiento de pacman, elimina por donde va comiendo pacman
diccionario_celdas_items = {}        #No se modifica. Para tener presente las celdas en las que se puede mover y pueden haber items
diccionario_celdas_pared = {}        #No se modifica. Para dibujar el mapa


#Supuestamente seria para A*(No tocar)
def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo)
        nodo = nodo.anterior  # Retrocede a la celda anterior
    return camino[::-1]  # Devuelve el camino en orden desde el inicio al objetivo

#No tocar(Aunque ahorita no hace nada)
def a_asterisco(inicio,objetivo):
    sin_procesar = []
    procesados = []

    # Agrega el nodo inicial
    inicio.g = 0
    inicio.h = inicio.calcular_distancia(objetivo)
    sin_procesar.append(inicio)

    while sin_procesar:
        # Ordena la lista abierta por f y selecciona el nodo con menor f
        sin_procesar.sort(key=lambda celda: celda.calcular_f())
        actual = sin_procesar.pop(0)  # Toma el nodo con menor f

        # Si hemos llegado al objetivo, podemos reconstruir el camino
        if actual == objetivo:
            return reconstruir_camino(actual)

        procesados.append(actual)

        # Para cada vecino
        for vecino in [actual.arriba, actual.abajo, actual.izquierda, actual.derecha]:
            if vecino and vecino.valor != 'pared' and vecino not in procesados:
                # Calcular g para el vecino
                g_temp = actual.g + 1  # Suponiendo que el costo de moverse a un vecino es 1

                if g_temp < vecino.g:
                    # Si el nuevo g es mejor, actualiza
                    vecino.g = g_temp
                    vecino.h = vecino.calcular_distancia(objetivo)
                    vecino.anterior = actual  # Guarda la celda anterior
                    if vecino not in sin_procesar:
                        sin_procesar.append(vecino)

    return None  # No se encontró camino


def inicializar_mapa(mapa):
    fila_max = len(mapa) - 1
    col_max = len(mapa[0]) - 1

    for y, fila in enumerate(
            mapa):  # para no tener que recorrer toda la matriz verificando si hay puntos. Se eliminan conforme va comiendo pacman
        for x, celda in enumerate(fila):
            celda.id = (y, x)
            if celda.valor != 'pared':
                if y != fila_max and mapa[y + 1][x].valor != 'pared':
                    celda.abajo = mapa[y + 1][x]
                if y != 0 and mapa[y - 1][x].valor != 'pared':
                    celda.arriba = mapa[y - 1][x]
                if x != col_max and mapa[y][x + 1].valor != 'pared':
                    celda.derecha = mapa[y][x + 1]
                if x != 0 and mapa[y][x - 1].valor != 'pared':
                    celda.izquierda = mapa[y][x - 1]

            if celda.valor == 'punto':
                diccionario_celdas_puntos[(x, y)] = 'punto'
                diccionario_celdas_items[(x, y)] = 'punto'
            elif celda.valor == 'fruta':
                diccionario_celdas_items[(x, y)] = 'fruta'
            elif celda.valor == 'pildora':
                diccionario_celdas_items[(x, y)] = 'pildora'
                diccionario_celdas_puntos[(x, y)] = 'pildora'
            elif celda.valor == 'pared':
                diccionario_celdas_pared[(x, y)] = 'pared'

    #for y, fila in enumerate(mapa): #para no tener que recorrer toda la matriz verificando si hay puntos. Se eliminan conforme va comiendo pacman
        #for x, celda in enumerate(fila):
            #if celda.valor == 'punto':
                #diccionario_celdas_puntos[(x, y)] = 'punto'
                #diccionario_celdas_items[(x, y)] = 'punto'
            #elif celda.valor == 'fruta':
                #diccionario_celdas_items[(x, y)] = 'fruta'
            #elif celda.valor == 'pared':
                #diccionario_celdas_pared[(x, y)] = 'pared'




# Dibujar el mapa en pantalla
def dibujar_mapa(mapa):

    for (x, y) in diccionario_celdas_pared.keys(): #    Dibujar paredes
        if mapa[y][x].valor == 'pared':
            color = (23, 56, 110)  # Azul para pared
        else:
            color = (0, 0, 0)
            if mapa[y][x].olor >= 1:
                color = (214, 90, 104)
            if 10 < mapa[y][x].olor < 20:
                color = (255, 46, 70)
            if mapa[y][x].olor >= 20:
                color = (255, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))


    for (x, y) in diccionario_celdas_items.keys(): #Dibujar rastro de olor (quitar en version final)
        mapa[y][x].decrementar_olor()

        # # Cambiar color basado en el valor del olor
        # if mapa[y][x].valor == 'pared':
        #     color = (23, 56, 110)  # Azul para pared
        # else:
        #     color = (0, 0, 0)
        #     if mapa[y][x].olor >= 1:
        #         color = (214, 90, 104)
        #     if 10 < mapa[y][x].olor < 20:
        #         color = (255, 46, 70)
        #     if mapa[y][x].olor >= 20:
        #         color = (255, 0, 0)
        # pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))


        # Comprobar si la celda es 'vacio' y no dibujar nada
        if mapa[y][x].valor == 'vacio':
            continue  # Saltar al siguiente ciclo si la celda es 'vacio'

        # Cambiar color basado en el valor del olor
        if mapa[y][x].valor == 'pared':
            color = (23, 56, 110)  # Azul para pared
            pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
        else:

            # Dibujar el punto si corresponde
            if mapa[y][x].valor == 'punto':
                punto_color = (255, 255, 255)  # Blanco para el punto
                punto_size = ANCHO_CELDA // 4  # Tamaño del punto (pedir opinion del tamaño)
                # Calcular la posicion centrada del cuadrito dentro de la celda
                punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2) - (punto_size // 2)
                punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2) - (punto_size // 2)
                # Dibujar el cuadrito blanco
                pygame.draw.rect(screen, punto_color, pygame.Rect(punto_x, punto_y, punto_size, punto_size))
            if mapa[y][x].valor == 'pildora':
                punto_color = (150, 173, 255)  # morado claro para el punto
                punto_radio = ANCHO_CELDA // 6  # radio del punto (pedir opinion del tamaño)

                # Calcular la posicion centrada del punto dentro de la celda
                punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2)  # Centro en X
                punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2)  # Centro en Y

                # Dibujar el círculo
                pygame.draw.circle(screen, punto_color, (punto_x, punto_y), punto_radio)


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

def dibujar_fantasmas(fantasmas):
    for fantasma in fantasmas:
        fantasma.imprimir(screen)

def moverFantasmas(pacman_y, pacman_x,fantasmas):
    for fantasma in fantasmas:
        fantasma.decidir_donde_viajar(mapa[pacman_y][pacman_x])
        #TP
        if fantasma.celda_actual.id == (12, 0):
            fantasma.celda_actual = mapa[12][25]
        if fantasma.celda_actual.id == (12, 26):
            fantasma.celda_actual=mapa[12][1]


#--------cosas de muerte---------

def is_comido(p_y, p_x, fantasmas):
    for fantasma in fantasmas:
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo != 'frightened':
            print("Comido")
            return True
    return False

def dibujar_vidas(vid):
    for i in range(vid):
        screen.blit(corazon_img, (5 + i * 45, 5)) #para separar los corazones

def game_over():
    screen.fill((255, 255, 255))  # RGB
    screen.blit(gameOver_img, (wwcd_x, wwcd_y))
    pygame.display.flip()
    pygame.time.wait(2000)

def victoria():
    screen.fill((255, 255, 255))  # RGB
    screen.blit(background_wwcd, (inicio_x, inicio_y))
    pygame.display.flip()
    pygame.time.wait(2000)

# Reducir olor de todas las celdas conforme camina PACMAN
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

        if pos_actual in diccionario_celdas_items and mapa[pacman_y][pacman_x].valor == 'pildora':
            del diccionario_celdas_items[pos_actual]  # elimina pildoras del diccionario de items
            mapa[pacman_y][pacman_x].valor = 'vacio'
            asustar_fantasmas()

        mapa[pacman_y][pacman_x].valor = 'vacio'
        del diccionario_celdas_puntos[pos_actual]  # elimina solo del diccionario de puntos
        # sonido de chomp
        mixer.music.load('musica/pacman_chomp2.wav')
        mixer.music.play()



    return pacman_x, pacman_y




tiempo = None
fantasmas = [
        Blinky(mapa[10][13]),
        Pinky(mapa[10][13]),
        Inky(mapa[10][13]),
        Clyde(mapa[10][13],mapa[24][1])
    ]

def liberarFantasmas(fantasmas,fantasmasLiberados):
    fantasmas[fantasmasLiberados].celda_actual=mapa[8][13]

def reiniciarFantasmas(fantasmas):
    for fantasma in fantasmas:
        fantasma.celda_actual = mapa[10][13]
        fantasma.liberado = False
    return 0


def inicializar_juego():
    inicializar_mapa(mapa)
    mixer.music.load('musica/pacman_beginning.wav')
    mixer.music.play()
    screen.fill((255, 255, 255))  # RGB
    screen.blit(background_inicio, (inicio_x, inicio_y))
    pygame.display.flip()
    pygame.time.wait(4000)

def asustar_fantasmas():
    for fantasma in fantasmas:
        fantasma.modo = 'frightened'
    tiempo = time.time()
    return 0

def normalizarFantasmas():
    for fantasma in fantasmas:
        fantasma.modo = 'chase'
    return 0


def is_colision(p_y, p_x, fantasmas):
    for fantasma in fantasmas:
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo!='frightened': #se lo comen
            #reiniciarFantasmas(fantasmas)
            print("se lo comieron")
            return 0
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo == 'frightened': #se los come
            fantasma.celda_actual = mapa[10][13]
            fantasma.liberado = False
            fantasma.modo = 'chase'  # CAMBIAR A scattered
            print("se lo comio")
            return 1
    return 3


inicializar_mapa(mapa)
inicializar_juego()

# **********************************Game loop*******************************
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
            if event.key == pygame.K_r:
                a = 1 #reiniciar con r (restart)
            if event.key == pygame.K_s:
                a = 1 #guardar con s (save)

    # Mover al PACMAN y actualizar el mapa
    pacman_x, pacman_y = mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad)
    if fantasmasLiberados < 4 and n % 30 == 0 and n != 0:
        liberarFantasmas(fantasmas,fantasmasLiberados)
        fantasmasLiberados += 1

    #-----------------VARIFICAR SI SE COMIERON AL PACMAN----------------
    if is_comido(pacman_y, pacman_x, fantasmas):
        pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
        reiniciarFantasmas(fantasmas)
        vidas -= 1
        if vidas <= 0:
            running = False
    else:
        is_colision(pacman_y, pacman_x, fantasmas)

    moverFantasmas(pacman_y, pacman_x, fantasmas)
    if is_comido(pacman_y, pacman_x, fantasmas):
        pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
        fantasmasLiberados=reiniciarFantasmas(fantasmas)
        vidas -= 1
        if vidas <= 0:
            running = False
    else:
        is_colision(pacman_y, pacman_x, fantasmas)



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
        pacman_x = 25   #Porque 25? Se esta saltando la celda 26, si se cambia da error, pero no entiendo porque(Creo que es para que no se encicle)
        if pos_tp in diccionario_celdas_puntos:
            # xy-> 25,12 y 26,12 vacio en tp
            mapa[pacman_y][pacman_x].valor = 'vacio'
            mapa[pacman_y][pacman_x+1].valor = 'vacio'
            del diccionario_celdas_puntos[pos_tp]
            del diccionario_celdas_puntos[pos_previa_tp]
    if pacman_x == 26 and pacman_y == 12:
        print("TP")
        pos_tp = (1, 12)
        pos_previa_tp = (0, 12)
        pacman_x = 1
        if pos_tp in diccionario_celdas_puntos:

            # xy-> 1,12 y 0,12 vacio en tp
            mapa[pacman_y][pacman_x].valor = 'vacio'
            mapa[pacman_y][pacman_x-1].valor = 'vacio'
            del diccionario_celdas_puntos[pos_tp]
            del diccionario_celdas_puntos[pos_previa_tp]

    # Dibujar el mapa y a PACMAN
    if tiempo is not None:
        tiempo_transcurrido = int(time.time() - tiempo)
        if tiempo_transcurrido >= 10:
            tiempo = None
            tiempo_transcurrido = None
            normalizarFantasmas()


    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)
    dibujar_fantasmas(fantasmas)
    dibujar_vidas(vidas)
    n+=1    #cantidad de iteraciones
    print(mapa[pacman_y][pacman_x].id, mapa[pacman_y-1][pacman_x-1].olor, mapa[pacman_y][pacman_x].olor, n, pacman_x, pacman_y)
    #creo que mapa[pacman_y-1][pacman_x-1].olor, es un poco ilogico porque al ser y-1 x-1, estaria en diagonal de Pacman
    if is_victoria(mapa):
        victoria()
        running = False

    if vidas==0:
        game_over()

    #texto_vidas = fuente_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
    #screen.blit(texto_vidas, (10, 10))  # arriba izq

    # Actualizar la pantalla
    pygame.display.flip()
    #controlar velocidad
    pygame.time.delay(200)
