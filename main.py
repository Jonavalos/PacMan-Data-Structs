
"""
 El movimiento de pacman, colisiones, objetos en el mapa fueron basados en un juego
 creado previamente por los integrantes (Space Invaders).
 Los algoritmos de búsqueda y fórmulas fueron hechos con ayuda de inteligencia artificial.
 Las imágenes y sonidos fueron extraídos de internet o creados con inteligencia artificial.




Integrantes:
Jonathan Avalos Montero
Josué Pineda Quesada
Fernando Santamaría Leiva


 """




import os
from pickle import GLOBAL
import time
from Fantasma import *
import random

import pygame
import pickle
from pygame import mixer
from pygame.examples.testsprite import Static

from Mapa import *
n=0
tiempo_liberar = None #para volver a chase

#FRUTAS & Multiplicador
tiempo_multiplicador = None
multiplicador = False
tiempo_spawn_fruta = None

def escoger_par_aleatorio2(diccionario): #GPT
    # Convierte las claves del diccionario en una lista de pares
    pares = list(diccionario.keys())
    # Escoge un par aleatorio
    return random.choice(pares)

def escoger_par_aleatorio(pares): #pasa vector_pares
    return random.choice(pares)

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((MAPA_ANCHO, MAPA_ALTO))

# Imagenes
background = pygame.image.load('PNGs/background.png')
background_inicio = pygame.image.load('PNGs/background_inicio.png')
background_wwcd = pygame.image.load('PNGs/wwcd2.png')
tigre_feliz = pygame.image.load('PNGs/tigreFeliz.png')

#Variables para controlar el estado del juego
is_paused = False
puntos=0
nivel = 1
velocidad_juego=200
vidas = 3
fuente_vidas_puntos = pygame.font.Font(None, 30) #representa puntos o vida como texto
corazon_img = pygame.image.load('PNGs/corazon.png')
gameOver_img = pygame.image.load('PNGs/gameOver2.png')
nivel_completado = False
fantasmasLiberados = 0
continuar_partida = False
Blinky_celda_actual_X = 0
Blinky_celda_actual_Y = 0
Pinky_celda_actual_X = 0
Pinky_celda_actual_Y = 0
Inky_celda_actual_X = 0
Inky_celda_actual_Y = 0
Clyde_celda_actual_X = 0
Clyde_celda_actual_Y = 0
estado_juego = {"Score: ": puntos, "nivel: ": nivel, "vidas: ": vidas}
save_file = "savegame.pkl"

# Cargar el archivo del juego si es que llegara a haber 1 partida guardada
if os.path.exists(save_file): #GPT
    with open(save_file, 'rb') as file:
        estado_juego = pickle.load(file)

#guardar el estado del juego
def guardar_partida(): #GPT
    print("Guardando partida")
    estado_juego = {
        "diccionario_celdas_puntos": diccionario_celdas_puntos,
        "diccionario_celdas_puntos2": diccionario_celdas_puntos2,
        "diccionario_celdas_items": diccionario_celdas_items,
        "diccionario_celdas_pared": diccionario_celdas_pared,
        "puntos": puntos,
        "vidas": vidas,
        "pacman_x": pacman_x,
        "pacman_y": pacman_y,
        "Blinky_celda_actual_X": fantasmas[0].celda_actual.id[1],
        "Blinky_celda_actual_Y": fantasmas[0].celda_actual.id[0],
        "Blinky_modo": fantasmas[0].modo,
        "Pinky_celda_actual_X": fantasmas[1].celda_actual.id[1],
        "Pinky_celda_actual_Y": fantasmas[1].celda_actual.id[0],
        "Pinky_modo": fantasmas[1].modo,
        "Inky_celda_actual_X": fantasmas[2].celda_actual.id[1],
        "Inky_celda_actual_Y": fantasmas[2].celda_actual.id[0],
        "Inky_modo": fantasmas[2].modo,
        "Clyde_celda_actual_X": fantasmas[3].celda_actual.id[1],
        "Clyde_celda_actual_Y": fantasmas[3].celda_actual.id[0],
        "Clyde_modo": fantasmas[3].modo
    }
    with open(save_file, 'wb') as file:
        pickle.dump(estado_juego, file)
    print("Partida guardada.")

#Funcion encargada de cargar el estado del juego
def cargar_partida(): #GPT
    global diccionario_celdas_puntos, diccionario_celdas_puntos2, diccionario_celdas_items, diccionario_celdas_pared, puntos, vidas, posicion_guardada_x, posicion_guardada_y
    global Blinky_celda_actual_X, Blinky_celda_actual_Y, Pinky_celda_actual_X,Pinky_celda_actual_Y,Inky_celda_actual_X,Inky_celda_actual_Y,Clyde_celda_actual_X,Clyde_celda_actual_Y
    if os.path.exists(save_file):
        try:
            with open(save_file, 'rb') as file:
                estado_juego = pickle.load(file)
                diccionario_celdas_puntos = estado_juego.get("diccionario_celdas_puntos", {})
                diccionario_celdas_puntos2 = estado_juego.get("diccionario_celdas_puntos2", {})
                diccionario_celdas_items = estado_juego.get("diccionario_celdas_items", {})
                diccionario_celdas_pared = estado_juego.get("diccionario_celdas_pared", {})
                puntos = estado_juego.get("puntos",0)
                vidas = estado_juego.get("vidas",5)
                posicion_guardada_x = estado_juego.get('pacman_x')
                posicion_guardada_y = estado_juego.get('pacman_y')
                Blinky_celda_actual_X = estado_juego.get("Blinky_celda_actual_X", 13)
                Blinky_celda_actual_Y = estado_juego.get("Blinky_celda_actual_Y", 10)
                fantasmas[0].modo = estado_juego.get("Blinky_modo")
                Pinky_celda_actual_X = estado_juego.get("Pinky_celda_actual_X", 1)
                Pinky_celda_actual_Y = estado_juego.get("Pinky_celda_actual_Y", 24)
                fantasmas[1].modo = estado_juego.get("Pinky_modo")
                Inky_celda_actual_X = estado_juego.get("Inky_celda_actual_X", 1)
                Inky_celda_actual_Y = estado_juego.get("Inky_celda_actual_Y", 1)
                fantasmas[2].modo = estado_juego.get("Inky_modo")
                Clyde_celda_actual_X = estado_juego.get("Clyde_celda_actual_X", 25)
                Clyde_celda_actual_Y = estado_juego.get("Clyde_celda_actual_Y", 1)
                fantasmas[3].modo = estado_juego.get("Clyde_modo")
                asustar = False
                i = 0
                v = []
                for fantasma in fantasmas:
                    if fantasma.modo == 'frightened':
                        asustar = True
                    if fantasma.modo == 'chase':
                        v.append(i)
                    i+=1
                if asustar:
                    global tiempo_liberar
                    tiempo_liberar = time.time()
                    asustar_fantasmas()

                for num in v:
                    fantasmas[num].modo = 'chase'

                for (x,y) in diccionario_celdas_puntos:
                    if diccionario_celdas_puntos[(x,y)] == 'fruta':
                        mapa[y][x].valor = 'fruta'

                if fantasmas:
                    fantasma_celda = mapa[Blinky_celda_actual_Y][Blinky_celda_actual_X]
                    fantasmas[0].celda_actual = fantasma_celda
                print("Partida cargada correctamente.")
        except Exception as e:
            print("Error al cargar la partida:", e)
    else:
        print("No existe la partida guardada.")


#Funcion para mostrar el menu al iniciar el juego
def mostrar_menu_opciones():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)
    opciones = ["Cargar Partida", "Inicializar Mapa"]

    for i, texto in enumerate(opciones):
        color = (255, 255, 255)
        texto_render = font.render(texto, True, color)
        screen.blit(texto_render, (MAPA_ANCHO // 2 - 100, MAPA_ALTO // 2 + i * 50))
    pygame.display.flip()

# Funcion para mostrar el menu en pausa
def mostrar_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)
    opciones = ["Continuar", "Guardar partida", "Salir"]
    for i, texto in enumerate(opciones):
        color = (255, 255, 255)
        texto_render = font.render(texto, True, color)
        screen.blit(texto_render, (MAPA_ANCHO // 2 - 100, MAPA_ALTO // 2 + i * 50))
    pygame.display.flip()


# Funcion para manejar el menu en pausa del juego
def manejar_menu(): #GPT
    global is_paused
    mostrar_menu()
    seleccion = 0
    font = pygame.font.Font("fonts\Silkscreen-Bold.ttf", 40)
    fondo_pausa = pygame.image.load('PNGs/Pausa.png')
    opciones = ["Continuar", "Guardar partida", "Salir"]

    factor = 0.8
    fondo_width = int(fondo_pausa.get_width() * factor)
    fondo_height = int(fondo_pausa.get_height() * factor)
    fondo_pausa = pygame.transform.scale(fondo_pausa, (fondo_width, fondo_height))
    fondo_x = (MAPA_ANCHO - fondo_width) // 2
    fondo_y = (MAPA_ALTO - fondo_height) // 2

    while is_paused:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_SPACE:
                    if seleccion == 0:  # Continuar
                        is_paused = False
                    elif seleccion == 1:  # Guardar partida
                        guardar_partida()
                        print("Partida guardada.")
                    elif seleccion == 2:  # Salir
                        pygame.quit()
                        exit()
            screen.blit(fondo_pausa, (fondo_x, fondo_y))
            posicion_y_inicial = MAPA_ALTO // 2 - 300
            for i, texto in enumerate(opciones):
                color = (255, 0, 0) if i == seleccion else (255, 255, 255)
                texto_render = font.render(texto, True, color)
                text_rect = texto_render.get_rect(center=(MAPA_ANCHO // 2, posicion_y_inicial + i * 60))
                screen.blit(texto_render, text_rect)
            pygame.display.flip()

#Funcion para manejar el menu del inicio del juego
def manejar_menu_inicio(): #GPT
    global continuar_partida
    seleccion = 0
    font = pygame.font.Font("fonts\Silkscreen-Bold.ttf", 45)
    opciones = ["Continuar Partida", "Nueva Partida"]
    fondo = pygame.image.load('PNGs/Pacman_Y_Tigre.png')
    factor = 0.8
    fondo_width = int(fondo.get_width() * factor)
    fondo_height = int(fondo.get_height() * factor)
    fondo = pygame.transform.scale(fondo, (fondo_width, fondo_height))
    fondo_x = (MAPA_ANCHO - fondo_width) // 2
    fondo_y = (MAPA_ALTO - fondo_height) // 2

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_SPACE:
                    if seleccion == 0:
                        continuar_partida = True
                        inicializar_mapa(mapa, cargar_desde_archivo=True)
                        inicializar_posicion_pacman()
                        cargar_fantasmas()
                        print("Partida cargada.")
                        return
                    elif seleccion == 1:
                        inicializar_mapa(mapa)
                        print("Mapa inicializado.")
                        return
        screen.blit(fondo, (fondo_x, fondo_y))
        posicion_y_inicial = MAPA_ALTO // 2 - 280
        for i, texto in enumerate(opciones):
            color = (255, 0, 0) if i == seleccion else (255, 255, 255)
            texto_render = font.render(texto, True, color)
            text_rect = texto_render.get_rect(center=(MAPA_ANCHO // 2, posicion_y_inicial + i * 60))
            screen.blit(texto_render, text_rect)

        pygame.display.flip()

# Obtener las dimensiones de las imagenes para centrarlas

image_rect = background_inicio.get_rect()#GPT
# Calcular la posición para centrar la imagen
inicio_x = (MAPA_ANCHO - image_rect.width) // 2  # Posición X
inicio_y = (MAPA_ALTO - image_rect.height) // 2  # Posición Y

image_rect2 = background_wwcd.get_rect()#GPT

# Calcular la posición para centrar la imagen
wwcd_x = (MAPA_ANCHO - image_rect2.width) // 2  # Posición X
wwcd_y = (MAPA_ALTO - image_rect2.height) // 2  # Posición Y

image_rect3 = background_wwcd.get_rect()#GPT

# Calcular la posición para centrar la imagen
tf_x = (MAPA_ANCHO - image_rect3.width) // 2  # Posición X
tf_y = (MAPA_ALTO - image_rect3.height) // 2  # Posición Y

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

#cargar imagen de frutas
apple_img = pygame.image.load('PNGs/apple.png')
cherry3D_img = pygame.image.load('PNGs/cherry3D.png')

# Posicion de Pac-Man en el mapa (coordenadas de la celda)
def inicializar_posicion_pacman():
    global pacman_x, pacman_y, continuar_partida, posicion_guardada_x, posicion_guardada_y
    if continuar_partida:
        pacman_x = posicion_guardada_x
        pacman_y = posicion_guardada_y
    else:
        pacman_x = 14  # Columna de la matriz
        pacman_y = 13  # Fila de la matriz

inicializar_posicion_pacman()

# Velocidad de movimiento (en celdas)
velocidad = 1
# Dirección: 1Left 2Right 3Up 4Down
direccion = 2

# Diccionario para almacenar las posiciones de las celdas que no sean 'pared'. Para no tener que recorrer toda la matiz en cada vuelta del while
# Inicializar dos diccionarios
diccionario_celdas_puntos= {}        #se modifica con cada movimiento de pacman, elimina por donde va comiendo pacman
diccionario_celdas_puntos2= {}        #NO se modifica con cada movimiento de pacman, elimina por donde va comiendo pacman
diccionario_celdas_items = {}        # Para tener presente las celdas en las que se puede mover y pueden haber items
diccionario_celdas_pared = {}        #NO se modifica Para dibujar el mapa

import heapq


def inicializar_mapa(mapa, cargar_desde_archivo = False):

    fila_max = len(mapa) - 1
    col_max = len(mapa[0]) - 1

    if cargar_desde_archivo:
        cargar_partida()
    else:
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
                    diccionario_celdas_puntos2[(x, y)] = 'punto'
                    diccionario_celdas_items[(x, y)] = 'punto'
                elif celda.valor == 'fruta':
                    diccionario_celdas_items[(x, y)] = 'fruta'
                    diccionario_celdas_puntos[(x, y)] = 'fruta'
                    diccionario_celdas_puntos2[(x, y)] = 'pildora'
                elif celda.valor == 'pildora':
                    diccionario_celdas_items[(x, y)] = 'pildora'
                    diccionario_celdas_puntos[(x, y)] = 'pildora'
                    diccionario_celdas_puntos2[(x, y)] = 'pildora'
                elif celda.valor == 'pared':
                    diccionario_celdas_pared[(x, y)] = 'pared'

def reset_mapa():
    global diccionario_celdas_items
    diccionario_celdas_items=diccionario_celdas_puntos2.copy()
    for (x, y) in diccionario_celdas_puntos2:
        if diccionario_celdas_puntos2[(x,y)] == 'pildora':
            diccionario_celdas_puntos[(x, y)] = 'pildora'
            diccionario_celdas_items[(x, y)] = 'pildora'
            mapa[y][x].valor = 'pildora'
        else:
            if diccionario_celdas_puntos2[(x,y)] == 'punto':
                diccionario_celdas_puntos[(x, y)] = 'punto'
                mapa[y][x].valor = 'punto'


# Dibujar el mapa en pantalla
def dibujar_mapa(mapa):

    for (x, y) in diccionario_celdas_pared.keys(): #    Dibujar paredes
        if mapa[y][x].valor == 'pared':
            color = (23, 56, 110)  # Azul para pared
        else:
            color = (0, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))

    for (x, y) in diccionario_celdas_puntos.keys():
        # Comprobar si la celda es 'vacio' y no dibujar nada
        if mapa[y][x].valor == 'vacio':
            continue  # Saltar al siguiente ciclo si la celda es 'vacio'


        if mapa[y][x].valor == 'pared':
            color = (23, 56, 110)  # Azul para pared
            pygame.draw.rect(screen, color, pygame.Rect(x * ANCHO_CELDA, y * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA))
        else:

            # Dibujar el punto si corresponde
            if mapa[y][x].valor == 'punto':
                punto_color = (255, 255, 255)  # Blanco para el punto
                punto_size = ANCHO_CELDA // 4
                # Calcular la posicion centrada del cuadrito dentro de la celda #GPT
                punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2) - (punto_size // 2)
                punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2) - (punto_size // 2)
                # Dibujar el cuadrito blanco
                pygame.draw.rect(screen, punto_color, pygame.Rect(punto_x, punto_y, punto_size, punto_size))
            if mapa[y][x].valor == 'pildora':
                punto_color = (150, 173, 255)  # morado claro para el punto
                punto_radio = ANCHO_CELDA // 3  # radio del punto, creo

                # Calcular la posicion centrada del punto dentro de la celda #GPT
                punto_x = (x * ANCHO_CELDA) + (ANCHO_CELDA // 2)  # Centro en X
                punto_y = (y * ALTO_CELDA) + (ALTO_CELDA // 2)  # Centro en Y

                # Dibujar el círculo
                pygame.draw.circle(screen, punto_color, (punto_x, punto_y), punto_radio)
            if mapa[y][x].valor == 'fruta':
                # Calcular la posicion centrada del punto dentro de la celda #GPT
                punto_x = (x * ANCHO_CELDA)
                punto_y = (y * ALTO_CELDA)
                # Dibujar la fruta
                screen.blit(cherry3D_img, (punto_x, punto_y))

def is_victoria(mapa): #Verifica si ya no quedan puntos (si ya ganó)
    if not diccionario_celdas_puntos:
        return True
    return False

# Dibujar a PACMAN en la celda correspondiente (GPT)
def dibujar_pacman(pacman_x, pacman_y, direccion):
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
        fantasma.decidir_donde_viajar(mapa[pacman_y][pacman_x],direccion,mapa,fantasmas[0])
        #Teleport
        if fantasma.celda_actual.id == (12, 0):
            fantasma.celda_actual = mapa[12][25]
        if fantasma.celda_actual.id == (12, 26):
            fantasma.celda_actual=mapa[12][1]


#--------cosas de muerte---------

def is_comido(p_y, p_x, fantasmas):
    for fantasma in fantasmas:
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo != 'frightened' and fantasma.modo !=  "eaten":
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
    mixer.music.load('musica/stage_clear.wav')
    mixer.music.play()
    pygame.display.flip()
    pygame.time.wait(6000)

def subir_nivel():
    screen.fill((255, 255, 255))  # RGB
    screen.blit(tigre_feliz, (tf_x, tf_y))
    pygame.display.flip()
    pygame.time.wait(1000)
    reset_mapa()

def aumentar_puntos():
    global puntos
    puntos+=1

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

    # Cuando pasa PACMAN, actualiza valor, elimina del diccionario y hace sonido de CHOMP (suena horrible pero es lo que hay)
    pos_actual = (pacman_x, pacman_y)
    if pos_actual in diccionario_celdas_puntos:

        if pos_actual in diccionario_celdas_items and mapa[pacman_y][pacman_x].valor == 'pildora':
            del diccionario_celdas_items[pos_actual]  # elimina pildoras del diccionario de items
            diccionario_celdas_puntos2[pos_actual] = 'pildora'
            mapa[pacman_y][pacman_x].valor = 'vacio'
            asustar_fantasmas()
            global tiempo_liberar
            tiempo_liberar = time.time()
            global tiempo_spawn_fruta
            tiempo_spawn_fruta = time.time()

        if pos_actual in diccionario_celdas_items and mapa[pacman_y][pacman_x].valor == 'fruta':
            del diccionario_celdas_items[pos_actual]  # elimina fruta del diccionario de items
            diccionario_celdas_puntos2[pos_actual] = 'punto'
            mapa[pacman_y][pacman_x].valor = 'vacio'
            multiplicador_on()
            global tiempo_multiplicador
            tiempo_multiplicador = time.time()

        mapa[pacman_y][pacman_x].valor = 'vacio'
        aumentar_puntos()
        if multiplicador:
            aumentar_puntos()

        del diccionario_celdas_puntos[pos_actual]  # elimina solo del diccionario de puntos
        # sonido de chomp
        mixer.music.load('musica/pacman_chomp2.wav')
        mixer.music.play()


    return pacman_x, pacman_y


fantasmas = [
        Blinky(mapa[10][13],mapa[24][25]),
        Pinky(mapa[10][13],mapa[24][1]),
        Inky(mapa[10][13],mapa[1][1]),
        Clyde(mapa[10][13],mapa[1][25])
    ]

def cargar_fantasmas():
    if Blinky_celda_actual_X != 0 and Blinky_celda_actual_Y != 0:
        fantasmas[0].celda_actual = mapa[Blinky_celda_actual_Y][Blinky_celda_actual_X]
    if Pinky_celda_actual_X != 0 and Pinky_celda_actual_Y != 0:
        fantasmas[1].celda_actual = mapa[Pinky_celda_actual_Y][Pinky_celda_actual_X]
    if Inky_celda_actual_X != 0 and Inky_celda_actual_Y != 0:
        fantasmas[2].celda_actual = mapa[Inky_celda_actual_Y][Inky_celda_actual_X]
    if Clyde_celda_actual_X != 0 and Clyde_celda_actual_Y != 0:
        fantasmas[3].celda_actual = mapa[Clyde_celda_actual_Y][Clyde_celda_actual_X]

def liberarFantasmas(fantasmas):
    for fantasma in fantasmas:
        if not fantasma.liberado:
            fantasma.celda_actual=mapa[8][13]
            fantasma.liberado = True
            return



def reiniciarFantasmas(fantasmas):
    for fantasma in fantasmas:
        fantasma.celda_actual = mapa[10][13]
        fantasma.liberado = False
    return 0


def inicializar_juego():

    mixer.music.load('musica/pacman_beginning.wav')
    mixer.music.play()
    screen.fill((255, 255, 255))  # RGB
    screen.blit(background_inicio, (inicio_x, inicio_y))
    pygame.display.flip()
    pygame.time.wait(4000)

    manejar_menu_inicio()

def asustar_fantasmas():
    for fantasma in fantasmas:
        if fantasma.modo != "eaten":
            fantasma.modo = 'frightened'
    return 0

def chase_fantasmas():
    for fantasma in fantasmas:
        fantasma.modo = 'chase'
    return 0

def multiplicador_off():
    global multiplicador
    multiplicador = False
    print('MULTIPLICADOR OFF')

def multiplicador_on():
    global multiplicador
    multiplicador = True
    print('MULTIPLICADOR ON')


def spawn_fruta_random():
    (x,y) = escoger_par_aleatorio2(diccionario_celdas_puntos) #ponerlo con el de puntos actuales o modificar abajo
    if diccionario_celdas_puntos.items():
        diccionario_celdas_puntos[(x,y)] = 'fruta'
        diccionario_celdas_puntos2[(x,y)] = 'fruta'
        diccionario_celdas_items[(x,y)] = 'fruta'
        mapa[y][x].valor = 'fruta'
        print('SPAWN FRUTA')
        print(y,x)


def is_colision(p_y, p_x, fantasmas):
    for fantasma in fantasmas:
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo!='frightened' and fantasma.modo != "eaten": #se lo comen
            reiniciarFantasmas(fantasmas)
            print("se lo comieron")
            return 0
        if fantasma.celda_actual.id == (p_y, p_x) and fantasma.modo == 'frightened': #se los come
            fantasma.modo = "eaten"
            print("se lo comio")
            aumentar_puntos()
            if multiplicador:
                aumentar_puntos()
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
            if event.key == pygame.K_SPACE:
                is_paused = not is_paused  #  toggle is_paused con espacio
                manejar_menu()

    if not is_paused: #la logica del juego no se ejecuta mientras este en pausa, solo la parte grafica. entonces parece que esta pausado

        # Mover al PACMAN y actualizar el mapa
        pacman_x, pacman_y = mover_pacman(mapa, pacman_x, pacman_y, direccion, velocidad)
        if n % 30 == 0 and n != 0:  #Aqui en vez de n podria ser una variable que cambie dependiendo del nivel
           liberarFantasmas(fantasmas)


        #-----------------VERIFICAR SI SE COMIERON AL PACMAN----------------
        if is_comido(pacman_y, pacman_x, fantasmas):
            pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
            fantasmasLiberados=reiniciarFantasmas(fantasmas)
            vidas -= 1
            if vidas <= 0:
                running = False
        else:
            if is_colision(pacman_y, pacman_x, fantasmas) == 1: #se come a alguno
                fantasmasLiberados -= 1
                tiempo_liberar = time.time()

        moverFantasmas(pacman_y, pacman_x, fantasmas)
        if is_comido(pacman_y, pacman_x, fantasmas):
            pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
            fantasmasLiberados=reiniciarFantasmas(fantasmas)
            vidas -= 1
            if vidas <= 0:
                running = False
        else:
            if is_colision(pacman_y, pacman_x, fantasmas)==1: #se come a alguno
                fantasmasLiberados-=1
                tiempo_liberar = time.time()


        #TELEPORT (ENDER PEARLLL)
        if pacman_x == 0 and pacman_y == 12:
            print("TP")
            pos_tp = (25, 12)
            pos_previa_tp = (26, 12)
            pacman_x = 25
            if pos_tp in diccionario_celdas_puntos:
                # xy-> 25,12 y 26,12 vacio en tp
                mapa[pacman_y][pacman_x].valor = 'vacio'
                mapa[pacman_y][pacman_x+1].valor = 'vacio'
                puntos += 2
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
                puntos += 2
                del diccionario_celdas_puntos[pos_tp]
                del diccionario_celdas_puntos[pos_previa_tp]

        # Dibujar el mapa y a PACMAN

        if tiempo_liberar is not None: #GPT
            tiempo_transcurrido = int(time.time() - tiempo_liberar)
            if tiempo_transcurrido >= 10:
                tiempo_liberar = None
                tiempo_transcurrido = None
                chase_fantasmas()

        if tiempo_multiplicador is not None: #GPT
            tiempo_transcurrido2 = int(time.time() - tiempo_multiplicador)
            if tiempo_transcurrido2 >= 7:
                tiempo_multiplicador = None
                tiempo_transcurrido2 = None
                multiplicador_off()

        if tiempo_spawn_fruta is not None: #GPT
            tiempo_transcurrido3 = int(time.time() - tiempo_spawn_fruta)
            if tiempo_transcurrido3 >= 7:
                tiempo_spawn_fruta = None
                tiempo_transcurrido3 = None
                spawn_fruta_random()


    dibujar_mapa(mapa)
    dibujar_pacman(pacman_x, pacman_y, direccion)
    dibujar_fantasmas(fantasmas)
    dibujar_vidas(vidas)
    n+=1
    if is_victoria(mapa):
        if not nivel_completado:  # Solo sube de nivel si no se ha completado
            if nivel == 1:
                nivel += 1
                print ('nivel')
                print (nivel)
                diccionario_celdas_puntos = diccionario_celdas_items.copy()
                reiniciarFantasmas(fantasmas)
                pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
                subir_nivel()
                time_delay = 160

                nivel_completado = True

            elif nivel == 2:
                nivel += 1
                print(nivel)
                print('nivel')
                diccionario_celdas_puntos = diccionario_celdas_items.copy()
                reiniciarFantasmas(fantasmas)
                pacman_x, pacman_y = mover_pacman(mapa, 14, 13, direccion, velocidad)
                subir_nivel()
                time_delay = 120

                nivel_completado = True

            elif nivel == 3:
                print(nivel)
                print('nivel')
                victoria()
                running = False

        else:
            # si nivel ya fue completado, no hace nada hasta el siguiente nivel
            print(nivel)
            pass

        # Restablece nivel_completado cuando inicies un nuevo nivel
    if not is_victoria(mapa):
        nivel_completado = False  # Para permitir avanzar en el siguiente nivel

    if vidas == 0:
        game_over()

    texto_puntos = fuente_vidas_puntos.render(f'Puntos: {puntos}', True, (255, 255, 255))
    screen.blit(texto_puntos, (660, 8))  # arriba izq

    # actualizar la pantalla
    pygame.display.flip()
    #coontrolar velocidad
    pygame.time.delay(200)