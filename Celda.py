import heapq
import itertools
import random
class Celda:
    def __init__(self,x, valor):
        self.id = id           # X,Y
        self.valor = valor     # Tipo de celda ('pared', 'punto', 'fruta', 'vacio', etc.)
        self.olor = 0          # Valor del "olor" a Pac-Man
        self.izquierda = None
        self.derecha = None
        self.arriba = None
        self.abajo = None

        #Para A* aunque ahorita no se esta usando
        self.anterior = None
        self.g = float('inf')


    def incrementar_olor(self):
        #Establece el valor de olor al máximo cuando Pac-Man pasa por la celda.
        if self.valor != 'pared':  # Solo incrementa si no es una pared
            self.olor = 30

    def decrementar_olor(self):
        #Decrementa el valor de olor hasta llegar a cero.
        if self.olor > 0:
            self.olor -= 1

    def __repr__(self):
        return f"Celda(id={self.id}, valor={self.valor}, olor={self.olor})"

    def calcular_distancia(self, objetivo):    #Retorna la distancia hasta el nodo destino
        return abs(self.id[0] - objetivo.id[0]) + abs(self.id[1] - objetivo.id[1])

    def calcular_f(self,objetivo):
        return self.g + self.calcular_distancia(objetivo)

    def setAnterior(self,celda):
        self.anterior = celda
        self.g = celda.g+1

    def retornar_vecino_con_menor_distancia(self, objetivo, anterior):
        menor_Celda = None
        menor_distancia = 1000

        for vecino in [self.arriba, self.abajo, self.izquierda, self.derecha]:
            if vecino and vecino is not anterior and vecino.valor != 'pared':
                distancia_actual = vecino.calcular_distancia(objetivo)
                if distancia_actual < menor_distancia:
                    menor_Celda = vecino
                    menor_distancia = distancia_actual

        return menor_Celda

    def __eq__(self, other):
        if isinstance(other, Celda):
            return self.id == other.id
        return False

    # def a_star(self,inicio, objetivo):
    #     sin_procesar = []
    #     procesados = set()  # Usamos set para búsquedas más rápidas
    #
    #     inicio.g = 0
    #     # Guardamos tuplas de (f_valor, celda) en la cola de prioridad
    #     heapq.heappush(sin_procesar, (inicio.calcular_f(objetivo), inicio))
    #
    #     # Mantener un conjunto de celdas en sin_procesar para búsqueda rápida
    #     celdas_en_sin_procesar = {inicio}
    #
    #     while sin_procesar:
    #         _, actual = heapq.heappop(sin_procesar)
    #         celdas_en_sin_procesar.remove(actual)
    #
    #         if actual == objetivo:
    #             return self.reconstruir_camino(actual)
    #
    #         procesados.add(actual)
    #
    #         for vecino in [actual.arriba, actual.abajo, actual.izquierda, actual.derecha]:
    #             if vecino and vecino.valor != 'pared' and vecino not in procesados:
    #                 nuevo_g = actual.g + 1
    #
    #                 if vecino not in celdas_en_sin_procesar:
    #                     vecino.setAnterior(actual)
    #                     f_valor = vecino.calcular_f(objetivo)
    #                     heapq.heappush(sin_procesar, (f_valor, vecino))
    #                     celdas_en_sin_procesar.add(vecino)
    #                 elif nuevo_g < vecino.g:
    #                     # Si encontramos un mejor camino
    #                     vecino.setAnterior(actual)
    #                     # Agregar nueva versión con f actualizado
    #                     f_valor = vecino.calcular_f(objetivo)
    #                     heapq.heappush(sin_procesar, (f_valor, vecino))
    #
    #     return None

    # def a_star(self, inicio, objetivo):
    #     # Estructura de datos para mantener los nodos por procesar
    #     sin_procesar = []
    #     heapq.heappush(sin_procesar, (0, inicio))
    #
    #     # Diccionarios para llevar la cuenta de costos
    #     costo_g = {inicio: 0}
    #     padres = {inicio: None}
    #
    #     while sin_procesar:
    #         # Obtener el nodo con el costo f más bajo
    #         _, actual = heapq.heappop(sin_procesar)
    #
    #         # Verificar si se ha alcanzado el objetivo
    #         if actual == objetivo:
    #             return self.reconstruir_ruta(padres, actual)
    #
    #         for vecino in actual.vecinos:
    #             # Calcular el costo g del vecino
    #             nuevo_costo_g = costo_g[actual] + 1  # Suponiendo un costo uniforme de 1 para cada movimiento
    #
    #             # Solo considerar el nuevo vecino si es más barato o no está en la lista
    #             if vecino not in costo_g or nuevo_costo_g < costo_g[vecino]:
    #                 costo_g[vecino] = nuevo_costo_g
    #                 f_valor = nuevo_costo_g + vecino.calcular_heuristica(objetivo)
    #                 padres[vecino] = actual
    #
    #                 # Agregar a la lista de nodos a procesar
    #                 heapq.heappush(sin_procesar, (f_valor, vecino))
    #
    #                 # Limitar el tamaño de sin_procesar a 10
    #                 if len(sin_procesar) > 10:
    #                     sin_procesar = sorted(sin_procesar)[:10]  # Mantener solo los 10 mejores
    #
    #     return []  # Si no se encuentra una ruta
    def getVecino(self, num):
        vecino = {
            1: self.izquierda,
            2: self.derecha,
            3: self.arriba,
            4: self.abajo
        }
        return vecino[num]


    def a_star(self, inicio, objetivo):
        sin_procesar = []
        procesados = []

        # Agrega el nodo inicial
        inicio.g = 0
        inicio.h = inicio.calcular_distancia(objetivo)
        sin_procesar.append(inicio)

        # Diccionario para llevar la cuenta de los padres
        padres = {inicio: None}

        while sin_procesar:
            # Ordenar y obtener el nodo con el costo f más bajo
            sin_procesar.sort(key=lambda celda: celda.calcular_f(objetivo))
            actual = sin_procesar.pop(0)

            # Si se alcanza el objetivo, retornar inmediatamente
            if actual == objetivo:
                return self.reconstruir_ruta(padres, actual)  # Pasar padres aquí

            # Agregar el nodo actual a los procesados
            procesados.append(actual)

            # Iterar sobre los vecinos
            for vecino in [actual.arriba, actual.abajo, actual.izquierda, actual.derecha]:
                if vecino is not None and vecino.valor != 'pared' and vecino not in procesados and vecino not in sin_procesar:
                    # Calcular los costos y configurar el padre
                    vecino.g = actual.g + 1  # Suponiendo un costo uniforme
                    vecino.h = vecino.calcular_distancia(objetivo)
                    padres[vecino] = actual  # Establecer el padre
                    sin_procesar.append(vecino)  # Agregar el vecino a la lista de nodos a procesar

        return None  # Si no se encuentra un camino de 10 celdas

    def a_star_sin_devolverse(self, inicio, objetivo, nodo_anterior):
        sin_procesar = []
        procesados = []

        # Agregar el nodo inicial
        inicio.g = 0
        inicio.h = inicio.calcular_distancia(objetivo)
        sin_procesar.append(inicio)

        # Diccionario para llevar la cuenta de los padres
        padres = {inicio: None}

        primer_iteracion = True  # Variable para controlar la primera iteración

        while sin_procesar:
            # Ordenar y obtener el nodo con el costo f más bajo
            sin_procesar.sort(key=lambda celda: celda.calcular_f(objetivo))
            actual = sin_procesar.pop(0)

            # Si se alcanza el objetivo, retornar inmediatamente
            if actual == objetivo:
                return self.reconstruir_ruta(padres, actual)  # Pasar padres aquí

            # Agregar el nodo actual a los procesados
            procesados.append(actual)

            # Iterar sobre los vecinos
            for vecino in [actual.arriba, actual.abajo, actual.izquierda, actual.derecha]:
                if vecino is not None and vecino.valor != 'pared' and vecino not in procesados:
                    # Verificamos si es la primera iteración y si el vecino es el nodo anterior
                    if primer_iteracion and vecino == nodo_anterior:  # Si el vecino es el nodo anterior, lo saltamos
                        continue

                    # Calcular los costos y configurar el padre
                    nuevo_g = actual.g + 1  # Suponiendo un costo uniforme

                    # Verificar si el vecino ya está en la lista `sin_procesar`
                    if vecino in sin_procesar:
                        # Si el vecino está en la lista y el nuevo costo g es mejor, actualizamos
                        if nuevo_g < vecino.g:
                            vecino.g = nuevo_g
                            # Recalcular `f` y reorganizar la lista de nodos
                            vecino.h = vecino.calcular_distancia(objetivo)
                            padres[vecino] = actual
                    else:
                        # Si el vecino no está en la lista, lo agregamos
                        vecino.g = nuevo_g
                        vecino.h = vecino.calcular_distancia(objetivo)
                        padres[vecino] = actual
                        sin_procesar.append(vecino)

            # Después de la primera iteración, desactivamos la restricción
            primer_iteracion = False

        return None

    # Si no se encuentra un camino de 10 celdas

    def reconstruir_ruta(self, padres, nodo_actual):
        ruta = []
        while nodo_actual is not None:
            ruta.append(nodo_actual)
            nodo_actual = padres.get(nodo_actual)  # Obtener el padre del nodo actual
        return ruta[::-1]  # Retornar la ruta en orden correcto

    def __hash__(self):
        # Retorna un hash basado en los atributos que definen la igualdad
        return hash(self.id)

    def obtener_vecino_aleatorio(self, anterior):
        vecinos = [self.arriba, self.abajo, self.izquierda, self.derecha]
        # Filtrar las celdas no nulas
        vecinos_validos = [vecino for vecino in vecinos if vecino is not None]

        # Eliminar el vecino anterior de la lista de vecinos válidos, si está presente
        if anterior in vecinos_validos:
            vecinos_validos.remove(anterior)

        if not vecinos_validos:
            return None  # No hay vecinos válidos

        # Retornar un vecino válido al azar
        return random.choice(vecinos_validos)


