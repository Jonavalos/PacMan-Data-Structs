from symtable import Class

from Celda import *
from Mapa import *
import pygame

class Fantasma: #Blinky
    def __init__(self,actual):
        self.modo = None        #Aqui iria si va a ir a atacar o huir
        self.celda_actual = actual
        self.celda_anterior = None
        self.imagen=[None,None]
        self.imagen_Actual = None

    def decidir_donde_viajar(self,destino):
        #nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        #self.celda_anterior = self.celda_actual
        #self.celda_actual = nueva_celda
        pass

    def imprimir(self,screen):
        pos_x = self.celda_actual.id[1] * ANCHO_CELDA
        pos_y = self.celda_actual.id[0] * ALTO_CELDA
        if self.celda_anterior != None:
            if self.celda_anterior.derecha == self.celda_actual:
                self.imagen_Actual=self.imagen[1]
            if self.celda_anterior.izquierda == self.celda_actual:
                self.imagen_Actual=self.imagen[0]

        screen.blit(self.imagen_Actual, (pos_x, pos_y))


class Blinky(Fantasma):
    def __init__(self,actual):
        super().__init__(actual)
        self.imagen[0]=pygame.image.load('PNGs/BlinkyLeft.png')     #Izquierda
        self.imagen[1]=pygame.image.load('PNGs/BlinkyRight.png')    #Derecha
        self.imagen_Actual = self.imagen[0]


    def decidir_donde_viajar(self,destino):
        nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        self.celda_anterior = self.celda_actual
        self.celda_actual = nueva_celda

    def imprimir(self,screen):
        super().imprimir(screen)


class Pinky(Fantasma): #(Rosa): Intenta predecir la dirección de Pacman y cortarle el paso
    def __init__(self,actual):
        super().__init__(actual)
        self.imagen[0]=pygame.image.load('PNGs/PinkyLeft.png')     #Izquierda
        self.imagen[1]=pygame.image.load('PNGs/PinkyRight.png')    #Derecha
        self.imagen_Actual = self.imagen[0]


    def decidir_donde_viajar(self,destino):
        nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        self.celda_anterior = self.celda_actual
        self.celda_actual = nueva_celda

    def imprimir(self,screen):
        super().imprimir(screen)



class Inky(Fantasma):   #(Cian): Utiliza tanto la posición de Pacman como la de Blinky para calcular su objetivo, lo que lo hace más impredecible
    def __init__(self,actual):
        super().__init__(actual)
        self.imagen[0] = pygame.image.load('PNGs/InkyLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/InkyRight.png')  # Derecha
        self.imagen_Actual = self.imagen[0]

    def decidir_donde_viajar(self,destino):
        nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        self.celda_anterior = self.celda_actual
        self.celda_actual = nueva_celda

    def imprimir(self,screen):
        super().imprimir(screen)


class Clyde(Fantasma):  # (Naranja): Se comporta de manera errática, a veces persiguiendo aPacman y otras veces alejándose
    def __init__(self,actual):
        super().__init__(actual)
        self.imagen[0] = pygame.image.load('PNGs/ClydeLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/ClydeRight.png')  # Derecha
        self.imagen_Actual = self.imagen[0]

    def decidir_donde_viajar(self,destino):
        nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        self.celda_anterior = self.celda_actual
        self.celda_actual = nueva_celda

    def imprimir(self,screen):
        super().imprimir(screen)
