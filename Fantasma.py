from symtable import Class
import time

from fontTools.misc.cython import returns

from Celda import *
from Mapa import *
import pygame

class Fantasma:
    def __init__(self,actual,esquina):
        self.modo = 'chase'        #scatter (van primero a las esquinas), chase (modo diablo), frightened (asustados)
        self.celda_actual = actual      #deberia ir primero scatter, y luego se activa el chase. Cambiar luego
        self.celda_anterior = None
        self.imagen=[None,None,None]
        self.imagen_Actual = None
        self.esquina = esquina
        self.camino = []


    def decidir_donde_viajar(self,destino):
        #nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        #self.celda_anterior = self.celda_actual
        #self.celda_actual = nueva_celda
        pass

    def imprimir(self,screen):
        pos_x = self.celda_actual.id[1] * ANCHO_CELDA
        pos_y = self.celda_actual.id[0] * ALTO_CELDA
        if self.celda_anterior != None:
            if self.celda_anterior.derecha == self.celda_actual and self.modo!='frightened':
                self.imagen_Actual=self.imagen[1]
            if self.celda_anterior.izquierda == self.celda_actual and self.modo!='frightened':
                self.imagen_Actual=self.imagen[0]
            if self.modo=='frightened':
                self.imagen_Actual=self.imagen[2]

        screen.blit(self.imagen_Actual, (pos_x, pos_y))


class Blinky(Fantasma):     #Esquina abajo derecha
    def __init__(self, actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/BlinkyLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/BlinkyRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen_Actual = self.imagen[0]

    def decidir_donde_viajar(self, destino):
        tamano = len(self.camino)
        if self.modo == 'chase':
            if tamano == 0:
                self.camino = self.celda_actual.a_star(self.celda_actual,destino)
                if self.camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    self.camino = []
                else:
                    self.camino.pop(0)
                    nueva_celda = self.camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
            else:
                nueva_celda = self.camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
        if self.modo == 'scatter':
            if tamano == 0:
                self.camino = self.celda_actual.a_star(self.celda_actual, self.esquina)
                if self.camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    self.camino = []
                else:
                    self.camino.pop(0)
                    nueva_celda = self.camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
            else:
                nueva_celda = self.camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda




def imprimir(self, screen):
        super().imprimir(screen)
    # def __init__(self,actual):
    #     super().__init__(actual)
    #     self.imagen[0]=pygame.image.load('PNGs/BlinkyLeft.png')     #Izquierda
    #     self.imagen[1]=pygame.image.load('PNGs/BlinkyRight.png')    #Derecha
    #     self.imagen[2]=pygame.image.load('PNGs/scaredGhost.png')    #Asustado
    #     self.imagen_Actual = self.imagen[0]
    #
    #
    # def decidir_donde_viajar(self,destino):
    #     # nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
    #     # self.celda_anterior = self.celda_actual
    #     # self.celda_actual = nueva_celda
    #     celda = self.celda_actual.a_star_limited(self.celda_actual, destino)
    #     if celda is not None:
    #         self.celda_actual=celda[1]
    #     else:
    #         self.celda_actual = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
    #
    # def imprimir(self,screen):
    #     super().imprimir(screen)


class Pinky(Fantasma): #(Rosa): Intenta predecir la dirección de Pacman y cortarle el paso  #Esquina abajo izquierda
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0]=pygame.image.load('PNGs/PinkyLeft.png')     #Izquierda
        self.imagen[1]=pygame.image.load('PNGs/PinkyRight.png')    #Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen_Actual = self.imagen[0]


    def decidir_donde_viajar(self,destino):
        if self.modo == 'chase':
            nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda



    def imprimir(self,screen):
        super().imprimir(screen)



class Inky(Fantasma):   #(Cian): Utiliza tanto la posición de Pacman como la de Blinky para calcular su objetivo, lo que lo hace más impredecible       #Esquina arriba izquierda
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/InkyLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/InkyRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen_Actual = self.imagen[0]

    def decidir_donde_viajar(self,destino):
        if self.modo == 'chase':
            nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda

    def imprimir(self,screen):
        super().imprimir(screen)


class Clyde(Fantasma):  # (Naranja): Se comporta de manera errática, a veces persiguiendo a Pacman y otras veces alejándose      Esquina arriba derecha
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/ClydeLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/ClydeRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen_Actual = self.imagen[0]
        self.modo = 'scatter'


    def decidir_donde_viajar(self,destino):
        tamano = len(self.camino)
        if self.modo == 'chase':
            if tamano == 0:
                self.camino = self.celda_actual.a_star(self.celda_actual, destino)
                if self.camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    self.camino = []
                    if self.celda_actual.calcular_distancia(destino) <= 8:
                        self.modo = 'scatter'
                        return
                else:
                    self.camino.pop(0)
                    nueva_celda = self.camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    if self.celda_actual.calcular_distancia(destino) <= 8:
                        self.modo = 'scatter'
                        self.camino = []
                        return
            else:
                nueva_celda = self.camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                if self.celda_actual.calcular_distancia(destino) <= 8:
                    self.modo = 'scatter'
                    self.camino = []
                    return

        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
            return
        if self.modo == 'scatter':
            if tamano == 0:
                self.camino = self.celda_actual.a_star(self.celda_actual, self.esquina)
                if self.camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    self.camino = []
                    if self.celda_actual == self.esquina:
                        self.modo = 'chase'
                        return
                else:
                    self.camino.pop(0)
                    nueva_celda = self.camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    if self.celda_actual == self.esquina:
                        self.modo = 'chase'
                        self.camino = []
                        return
            else:
                nueva_celda = self.camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                if self.celda_actual == self.esquina:
                    self.modo = 'chase'
                    self.camino = []
                    return


            # if self.modo =='scatter':
        #     nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina, self.celda_anterior)
        #     self.celda_anterior = self.celda_actual
        #     self.celda_actual = nueva_celda
        #     if self.celda_actual.id[0] == self.esquina.id[0] & self.celda_actual.id[1] == self.esquina.id[1]:
        #         self.modo = 'chase'
        # if destino.calcular_distancia(destino) > 8 or self.modo == 'chase':
        #     self.modo = 'chase'
        #     nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        #     self.celda_anterior = self.celda_actual
        #     self.celda_actual = nueva_celda



    def imprimir(self,screen):
        super().imprimir(screen)
