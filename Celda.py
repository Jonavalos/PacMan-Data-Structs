class Celda:
    def __init__(self, id, valor):
        self.id = id           # Identificador único de la celda
        self.valor = valor     # Tipo de celda ('pared', 'pared', 'pacman', etc.)
        self.olor = 0          # Valor del "olor" a Pac-Man

    def incrementar_olor(self):
        """Establece el valor de olor al máximo cuando Pac-Man pasa por la celda."""
        if self.valor != 'pared':  # Solo incrementa si no es una pared
            self.olor = 1000

    def decrementar_olor(self):
        """Decrementa el valor de olor hasta llegar a cero."""
        if self.olor > 0:
            self.olor -= 1

    def __repr__(self):
        return f"Celda(id={self.id}, valor={self.valor}, olor={self.olor})"