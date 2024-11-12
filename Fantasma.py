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
        self.imagen=[None,None,None,None]
        self.imagen_Actual = None
        self.esquina = esquina
        self.spawn = actual
        self.liberado = False

    def get_celda_actual(self):
        if self.modo == "eaten":    #Use traductor para poner eso jaja, supongamos que es "comido", si esta mal escrito me avisan o lo cambian jaja
            return self.spawn
        return self.celda_actual
    def decidir_donde_viajar(self,destino,direccion=0,mapa=None):
        pass

    def imprimir(self,screen):
        pos_x = self.celda_actual.id[1] * ANCHO_CELDA
        pos_y = self.celda_actual.id[0] * ALTO_CELDA
        if self.celda_anterior is not None:
            if self.celda_anterior.derecha == self.celda_actual and self.modo!='frightened' and self.modo != "eaten":
                self.imagen_Actual=self.imagen[1]
            if self.celda_anterior.izquierda == self.celda_actual and self.modo!='frightened' and self.modo != "eaten":
                self.imagen_Actual=self.imagen[0]
            if self.modo=='frightened':
                self.imagen_Actual=self.imagen[2]
            if self.modo == 'eaten':
                self.imagen_Actual=self.imagen[3]

        screen.blit(self.imagen_Actual, (pos_x, pos_y))


class Blinky(Fantasma):     #Esquina abajo derecha
    def __init__(self, actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/BlinkyLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/BlinkyRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen[3] = pygame.image.load('PNGs/Ojos2.png')         #Comido
        self.imagen_Actual = self.imagen[0]
        self.modo = 'scatter'


    def decidir_donde_viajar(self, destino,direccion=0,mapa=None,blinky=None): #GPT
        if self.modo == 'chase':
            camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual,destino,self.celda_anterior)
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
                camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual, self.esquina,self.celda_anterior)
                if camino is None:
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina,self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda

                else:
                    camino.pop(0)
                    nueva_celda = camino.pop(0)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    if self.celda_actual == self.esquina:
                        self.modo = 'chase'

        if self.modo == "eaten":
            celda = mapa[self.spawn.id[0] - 2][self.spawn.id[1]]
            if self.celda_actual == celda:
                nueva_celda = self.spawn
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                self.modo = "scatter"
                self.liberado = False
                return
            camino = self.celda_actual.a_star(self.celda_actual, celda)
            if camino is None:
                # Si no hay camino se mueve a la casilla mas cerca de pacman
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(celda, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda



    def imprimir(self, screen):
            super().imprimir(screen)

    def get_celda_actual(self):
        return super().get_celda_actual()



class Pinky(Fantasma): #(Rosa): Intenta predecir la dirección de Pacman y cortarle el paso  #Esquina abajo izquierda
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0]=pygame.image.load('PNGs/PinkyLeft.png')     #Izquierda
        self.imagen[1]=pygame.image.load('PNGs/PinkyRight.png')    #Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen[3] = pygame.image.load('PNGs/Ojos2.png')
        self.imagen_Actual = self.imagen[0]
        self.modo = 'scatter'


    def decidir_donde_viajar(self,destino,direccion=0,mapa=None,blinky=None):  #GPT   # Dirección: 1Left 2Right 3Up 4Down
        if self.modo == 'chase':
            # Diccionario para seleccionar `des` basado en la dirección
            des = destino
            aux = destino
            i = 0
            while des is not None and i < 2:
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
            camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual, self.esquina,self.celda_anterior)
            if camino is None:
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(self.esquina, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                if self.celda_actual == self.esquina:
                    self.modo = 'chase'

             # Comido
        if self.modo == "eaten":
            celda = mapa[self.spawn.id[0] - 2][self.spawn.id[1]]
            if self.celda_actual == celda:
                nueva_celda = self.spawn
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                self.modo = "scatter"
                self.liberado = False
                return
            camino = self.celda_actual.a_star(self.celda_actual, celda)
            if camino is None:
                # Si no hay camino se mueve a la casilla mas cerca de pacman
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(celda, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda


    def imprimir(self,screen):
        super().imprimir(screen)
    def get_celda_actual(self):
        return super().get_celda_actual()


class Inky(Fantasma):   #(Cian): Utiliza tanto la posición de Pacman como la de Blinky para calcular su objetivo, lo que lo hace más impredecible       #Esquina arriba izquierda
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/InkyLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/InkyRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen[3] = pygame.image.load('PNGs/Ojos2.png')         #Comido
        self.imagen_Actual = self.imagen[0]
        self.modo = 'scatter'

    def decidir_donde_viajar(self,destino,direccion=0,mapa=None,blinky = None): #GPT
        if self.modo == 'chase':
            fila_max = len(mapa) - 2
            col_max = len(mapa[0]) - 2
            vec = self.calculo_de_celda(destino,direccion,blinky)
            vec = (self.limitar(vec[0],2,fila_max),self.limitar(vec[1],2,col_max))
            celda = mapa[vec[0]][vec[1]]

            if celda.valor == 'pared':
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(celda, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return

            if celda == self.celda_actual:
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return

            camino = self.celda_actual.a_star_combinar_estrategias(self.celda_actual, celda, self.celda_anterior,destino)
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

        if self.modo == 'frightened':
            nueva_celda = self.celda_actual.obtener_vecino_aleatorio(self.celda_anterior)
            self.celda_anterior = self.celda_actual
            self.celda_actual = nueva_celda

        if self.modo == 'scatter':
                camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual, self.esquina,self.celda_anterior)
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

            # Comido
        if self.modo == "eaten":
            celda = mapa[self.spawn.id[0] - 2][self.spawn.id[1]]
            if self.celda_actual == celda:
                nueva_celda = self.spawn
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                self.modo = "scatter"
                self.liberado = False
                return
            camino = self.celda_actual.a_star(self.celda_actual, celda)
            if camino is None:
                # Si no hay camino se mueve a la casilla mas cerca de pacman
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(celda, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda








    def imprimir(self,screen):
        super().imprimir(screen)

    def limitar(self,valor, minimo, maximo):
        return max(minimo, min(valor, maximo))

    def get_celda_actual(self):
        return super().get_celda_actual()

    def calculo_de_celda(self,destino,direccion=0,blinky = None):
        des = destino
        aux = destino
        i = 0
        while des is not None and i < 2:
            aux = des
            des = des.getVecino(direccion)
            i += 1
        des = aux
        vec = (des.id[0]-blinky.celda_actual.id[0],des.id[1]-blinky.celda_actual.id[1])
        vec2= (blinky.get_celda_actual().id[0] + vec[0]*2,blinky.get_celda_actual().id[1]+vec[1]*2)
        return vec2




class Clyde(Fantasma):  # (Naranja): Se comporta de manera errática, a veces persiguiendo a Pacman y otras veces alejándose      Esquina arriba derecha
    def __init__(self,actual,esquina):
        super().__init__(actual,esquina)
        self.imagen[0] = pygame.image.load('PNGs/ClydeLeft.png')  # Izquierda
        self.imagen[1] = pygame.image.load('PNGs/ClydeRight.png')  # Derecha
        self.imagen[2] = pygame.image.load('PNGs/scaredGhost.png')  # Asustado
        self.imagen[3] = pygame.image.load('PNGs/Ojos2.png')
        self.imagen_Actual = self.imagen[0]
        self.modo = 'scatter'

    def decidir_donde_viajar(self, destino,direccion=0,mapa=None,blinky=None): #GPT
        if self.modo == 'chase':
            camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual,destino,self.celda_anterior)
            if camino is None:
            # Si no hay camino se mueve a la casilla mas cerca de pacman
                    nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(destino, self.celda_anterior)
                    self.celda_anterior = self.celda_actual
                    self.celda_actual = nueva_celda
                    return
            else:
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
            camino = self.celda_actual.a_star_sin_devolverse(self.celda_actual, self.esquina,self.celda_anterior)
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
                    # Si llegó a la esquina, cambia a modo 'chase'
                if self.celda_actual == self.esquina:
                    self.modo = 'chase'
                return

        #Comido
        if self.modo == "eaten":
            celda = mapa[self.spawn.id[0] - 2][self.spawn.id[1]]
            if self.celda_actual == celda:
                nueva_celda = self.spawn
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                self.modo = "scatter"
                self.liberado = False
                return
            camino = self.celda_actual.a_star(self.celda_actual, celda)
            if camino is None:
                # Si no hay camino se mueve a la casilla mas cerca de pacman
                nueva_celda = self.celda_actual.retornar_vecino_con_menor_distancia(celda, self.celda_anterior)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda
                return
            else:
                camino.pop(0)
                nueva_celda = camino.pop(0)
                self.celda_anterior = self.celda_actual
                self.celda_actual = nueva_celda



    def get_celda_actual(self):
        return super().get_celda_actual()

    def imprimir(self,screen):
        super().imprimir(screen)
