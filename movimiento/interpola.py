""" fichero: interpola.py

Funciones de interpolación.
"""


def interpola_lineal(t0,t1,x0,x1,t):
    """
    t0: inicio del tramo
    t1: fin del tramo
    x0: posicion al inicio del tramo
    x1: posición al final del tramo
    t: tiempo entre t0 y t1 en el que queremos la posición
    """
    u = (t-t0)/(t1-t0) # Proporción de tiempo transcurrido
    x = x0 + u*(x1-x0)
    return x


