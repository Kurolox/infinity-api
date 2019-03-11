def es_punto_valido(punto: tuple) -> bool:
    x, y = punto 
    puntos_invalidos = [(x, y) for x in range(0, 7) for y in range(0, 7) if x not in range(2, 5) and y not in range(2, 5)] 
    return not punto in puntos_invalidos and (0 <= x < 7 and 0 <= y < 7 and max(min(x, 6-x), min(y, 6-y)) > 1)


def dibujar_tablero(tablero: list) -> None:
    """Dibuja el tablero en pantalla con decoraciones."""

    print(r"""
  a b c d e f g
 ┏━━━━━━━━━━━━━┓
A┃    {}-{}-{}    ┃
 ┃    |\|/|    ┃
B┃    {}-{}-{}    ┃
 ┃    |/|\|    ┃
C┃{}-{}-{}-{}-{}-{}-{}┃
 ┃|\|/|\|/|\|/|┃
D┃{}-{}-{}-{}-{}-{}-{}┃              
 ┃|/|\|/|\|/|\|┃
E┃{}-{}-{}-{}-{}-{}-{}┃             
 ┃    |\|/|    ┃
F┃    {}-{}-{}    ┃
 ┃    |/|\|    ┃
G┃    {}-{}-{}    ┃
 ┗━━━━━━━━━━━━━┛
 """.format(*[ficha for y, fila in enumerate(tablero) for x, ficha in enumerate(fila) if es_punto_valido((x, y))]))


tablero = [["*" for lado in range(7)] for lado in range(7)]

for fila in tablero:
    print(" ".join(fila))
