class Celda:
    def __init__(self,x, valor):
        self.id = id           # Identificador de columna de la celda (para no perderme al hacer el mapa)
        self.valor = valor     # Tipo de celda ('pared', 'punto', 'fruta', 'vacio', etc.)
        self.olor = 0          # Valor del "olor" a Pac-Man
        self.izquierda = None
        self.derecha = None
        self.arriba = None
        self.abajo = None

        #Para A* aunque ahorita no se esta usando
        self.anterior = None
        self.g = float('inf')
        self.h = None


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

    def calcular_f(self):
        return self.g + self.h

    def retornar_vecino_con_menor_distancia(self, objetivo, anterior):
        menor_Celda = None
        menor_distancia = 1000

        for vecino in [self.arriba, self.abajo, self.izquierda, self.derecha]:
            if vecino and vecino is not anterior and vecino.valor != 'pared':
                distancia_actual = vecino.calcular_distancia(objetivo)
                if distancia_actual <= menor_distancia:
                    menor_Celda = vecino
                    menor_distancia = distancia_actual

        return menor_Celda