from Celda import *

# Dimensiones de las celdas y de la pantalla

MAPA_ANCHO = 1350
MAPA_ALTO = 700
ANCHO_CELDA = 30
ALTO_CELDA = 30

mapa = [     #1 borde,   13,14,15 columna (pared),  27 borde.  En primera y ultima todas son pared
    [Celda(1, 'pared'), Celda(2, 'pared'), Celda(3, 'pared'), Celda(4, 'pared'), Celda(5, 'pared'), Celda(6, 'pared'), Celda(7, 'pared'), Celda(8, 'pared'), Celda(9, 'pared'), Celda(10, 'pared'), Celda(11, 'pared'), Celda(12, 'pared'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'pared'), Celda(17, 'pared'), Celda(18, 'pared'), Celda(19, 'pared'), Celda(20, 'pared'), Celda(21, 'pared'), Celda(22, 'pared'), Celda(23, 'pared'), Celda(24, 'pared'), Celda(25, 'pared'), Celda(26, 'pared'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'punto'), Celda(4, 'punto'), Celda(5, 'punto'), Celda(6, 'punto'), Celda(7, 'punto'), Celda(8, 'punto'), Celda(9, 'punto'), Celda(10, 'punto'), Celda(11, 'punto'), Celda(12, 'punto'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'punto'), Celda(17, 'punto'), Celda(18, 'punto'), Celda(19, 'punto'), Celda(20, 'punto'), Celda(21, 'punto'), Celda(22, 'punto'), Celda(23, 'punto'), Celda(24, 'punto'), Celda(25, 'punto'), Celda(26, 'punto'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'pared'), Celda(4, 'pared'), Celda(5, 'pared'), Celda(6, 'pared'), Celda(7, 'punto'), Celda(8, 'pared'), Celda(9, 'pared'), Celda(10, 'pared'), Celda(11, 'pared'), Celda(12, 'punto'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'punto'), Celda(17, 'pared'), Celda(18, 'pared'), Celda(19, 'pared'), Celda(20, 'pared'), Celda(21, 'punto'), Celda(22, 'pared'), Celda(23, 'pared'), Celda(24, 'pared'), Celda(25, 'pared'), Celda(26, 'punto'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'pared'), Celda(4, 'pared'), Celda(5, 'pared'), Celda(6, 'pared'), Celda(7, 'punto'), Celda(8, 'pared'), Celda(9, 'pared'), Celda(10, 'pared'), Celda(11, 'pared'), Celda(12, 'punto'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'punto'), Celda(17, 'pared'), Celda(18, 'pared'), Celda(19, 'pared'), Celda(20, 'pared'), Celda(21, 'punto'), Celda(22, 'pared'), Celda(23, 'pared'), Celda(24, 'pared'), Celda(25, 'pared'), Celda(26, 'punto'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'pared'), Celda(4, 'pared'), Celda(5, 'pared'), Celda(6, 'pared'), Celda(7, 'punto'), Celda(8, 'pared'), Celda(9, 'pared'), Celda(10, 'pared'), Celda(11, 'pared'), Celda(12, 'punto'), Celda(13, 'punto'), Celda(14, 'punto'), Celda(15, 'punto'), Celda(16, 'punto'), Celda(17, 'pared'), Celda(18, 'pared'), Celda(19, 'pared'), Celda(20, 'pared'), Celda(21, 'punto'), Celda(22, 'pared'), Celda(23, 'pared'), Celda(24, 'pared'), Celda(25, 'pared'), Celda(26, 'punto'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'pared'), Celda(4, 'pared'), Celda(5, 'pared'), Celda(6, 'pared'), Celda(7, 'punto'), Celda(8, 'pared'), Celda(9, 'pared'), Celda(10, 'pared'), Celda(11, 'pared'), Celda(12, 'punto'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'punto'), Celda(17, 'pared'), Celda(18, 'pared'), Celda(19, 'pared'), Celda(20, 'pared'), Celda(21, 'punto'), Celda(22, 'pared'), Celda(23, 'pared'), Celda(24, 'pared'), Celda(25, 'pared'), Celda(26, 'punto'), Celda(27, 'pared')],
    [Celda(1, 'pared'), Celda(2, 'punto'), Celda(3, 'punto'), Celda(4, 'punto'), Celda(5, 'punto'), Celda(6, 'punto'), Celda(7, 'punto'), Celda(8, 'punto'), Celda(9, 'punto'), Celda(10, 'punto'), Celda(11, 'punto'), Celda(12, 'punto'), Celda(13, 'pared'), Celda(14, 'pared'), Celda(15, 'pared'), Celda(16, 'punto'), Celda(17, 'punto'), Celda(18, 'punto'), Celda(19, 'punto'), Celda(20, 'punto'), Celda(21, 'punto'), Celda(22, 'punto'), Celda(23, 'punto'), Celda(24, 'punto'), Celda(25, 'punto'), Celda(26, 'punto'), Celda(27, 'pared')],
]