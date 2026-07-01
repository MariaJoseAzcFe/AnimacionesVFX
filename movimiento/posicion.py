""" fichero: posicion.py

Este fichero contiene la función get_posicion, que devuelve un valor
a partir de una función sencilla.

"""

# Importamos la función interpola_lineal del módulo interpola
# La utilizaremos más adelante.
#from interpola import interpola_lineal

"""
Variables y parámetros
Algunas variables, para facilitar cambios en el código y
para facilitar la lectura del código.

"""

t_inicial = 0
t_final = 5

pos_inicial = 0
pos_final = 10


"""

"""


def get_posicion(frm : float):
    """ Devuelve un valor para la posición para el fotograma
    que se le pasa como argumento.

    Para un script más complejo esta función podría descomponerse
    en varias funciones.

    Argumentos:

    frm : float
        Número de fotograma para el que se quiere calcular la posición.


    Devuelve:

    posx : float
        Posición para el fotograma que se le pasa como argumento.
    """
    t_min = t_inicial
    t_max = t_final
    x_min = pos_inicial
    x_max = pos_final

    # Cada fotograma es 1/24 secs.
    # Empezamos calculando el tiempo
    t = frm/24.0

    if t <= t_min:
        posx = x_min
    elif t >= t_max:
        posx = x_max
    else:
        # Interpolamos linealmente
        u = (t - t_min) / (t_max - t_min)
        posx = x_min + u * (x_max - x_min)

    return posx
#

