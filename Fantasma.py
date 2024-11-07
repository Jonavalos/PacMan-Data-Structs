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


    def decidir_donde_viajar(self,destino,direccion=0):
        #nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
        #self.celda_anterior = self.celda_actual
        #self.celda_actual = nueva_celda
        pass

    def imprimir(self,screen):
        pos_x = self.celda_actual.id[1] * ANCHO_CELDA
        pos_y = self.celda_actual.id[0] * ALTO_CELDA
        if self.celda_anterior is not None:
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


    def decidir_donde_viajar(self, destino,direccion=0):
        if self.modo == 'chase':
            camino = self.celda_actual.a_star(self.celda_actual,destino)
            if camino is None:
            # Si no hay camino, moverse al vecino más cercano sin recalcular
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return
            else:  # Mantener camino vacío hasta el próximo intento
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return

        # Modo asustado (moverse aleatoriamente)
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
            return

        # Modo scatter (ir a las esquinas)
        if self.modo == 'scatter':
                camino = self.celda_actual.a_star(self.celda_actual, self.esquina)
                if camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina,self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    return
                else:
                    camino.pop(0)
                    nueva_celda = camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                return


    def imprimir(self, screen):
            super().imprimir(screen)




class Pinky(Fantasma): #(Rosa): Intenta predecir la dirección de Pacman y cortarle el paso  #Esquina abajo izquierda
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0]=pygame.image.load('PNGs/PinkyLeft.png')     #Izquierda
        self.imagen[1]=pygame.image.load('PNGs/PinkyRight.png')    #Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen_Actual = self.imagen[0]


    def decidir_donde_viajar(self,destino,direccion=0):     # Dirección: 1Left 2Right 3Up 4Down
        if self.modo == 'chase':
            # Diccionario para seleccionar `des` basado en la dirección
            des = destino
            aux = destino
            i = 0
            while des is not None and i < 3:
                aux = des
                des = des.getVecino(direccion)
                i+=1
            des = aux

            if des == self.celda_actual:
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return

            # Calcular el camino usando A*
            camino = self.celda_actual.a_star_combinar_estrategias(self.celda_actual, des,self.celda_anterior,destino)

            if camino is None:
                # Si no hay camino, usa el vecino más cercano sin recalcular
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
            else:
                # Avanzar en el camino calculado
                camino.pop(0)  # Ignora la celda actual
                nueva_celda = camino.pop(0)   # Avanza a la siguiente si hay camino

            # Actualizar posiciones
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
            return

            # Modo asustado (moverse aleatoriamente)
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
            return

            # Modo scatter (ir a las esquinas)
        if self.modo == 'scatter':
            camino = self.celda_actual.a_star(self.celda_actual, self.esquina)
            if camino is None:
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
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

    def decidir_donde_viajar(self,destino,direccion=0):
        if self.modo == 'chase':
            if self.modo == 'chase':
                self.camino = self.celda_actual.a_star(self.celda_actual, destino)
                if self.camino is None:
                    # Si no hay camino, moverse al vecino más cercano sin recalcular
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    self.camino = []
                else:  # Mantener camino vacío hasta el próximo intento
                    self.camino.pop(0)
                    self.celda_actual = self.camino.pop(0)
            # nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
            # self.celda_anterior = self.celda_actual
            # self.celda_actual = nueva_celda
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

    def decidir_donde_viajar(self, destino,direccion=0):
        if self.modo == 'chase':
            camino = self.celda_actual.a_star(self.celda_actual,destino)
            if camino is None:
            # Si no hay camino, moverse al vecino más cercano sin recalcular
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    return
            else:  # Mantener camino vacío hasta el próximo intento
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                if self.celda_actual.calcular_distancia(destino) <= 8:
                    self.modo = 'scatter'
                    return

        # Modo asustado (moverse aleatoriamente)
        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda
            return

        # Modo scatter (ir a las esquinas)
        if self.modo == 'scatter':
                camino = self.celda_actual.a_star(self.celda_actual, self.esquina)
                if camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina,self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                else:
                    camino.pop(0)
                    nueva_celda = camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    # Si llegó a la esquina, cambia a modo 'chase'
                    if self.celda_actual == self.esquina:
                        self.modo = 'chase'









    def imprimir(self,screen):
        super().imprimir(screen)
