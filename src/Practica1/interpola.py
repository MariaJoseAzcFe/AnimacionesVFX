"""
interpola.py

Algoritmos de interpolación

Autores: Josemi, Maria José, Juan Pablo


"""

def lineal(t: float, t0: float, t1: float, x0: float, x1: float):
    """
    Algoritmo de interpolación lineal.
    Calcula el valor x(t) en una recta que pasa por (t0, x0) y (t1, x1).
    
    Parameters
    ----------
    t : float
        Tiempo (fotograma) actual en el que calcular el valor.
    t0 : float
        Tiempo (fotograma) inicial del segmento.
    t1 : float
        Tiempo (fotograma) final del segmento.
    x0 : float
        Valor de la posición en el tiempo t0.
    x1 : float
        Valor de la posición en el tiempo t1.

    Returns
    -------
    float
        El valor interpolado x(t).
    """
    
    delta_t = t1 - t0
    if delta_t == 0.0:
        # Evitar división por cero. Si los keyframes están en el mismo tiempo,
        # simplemente devuelve el primer valor.
        return x0
        
    # Normalizar t al rango [0, 1]
    t_norm = (t - t0) / delta_t
    
    # Aplicar la fórmula de interpolación lineal
    return x0 + t_norm * (x1 - x0)


def hermite(t: float, t0: float, t1: float, x0: float, x1: float, m0: float, m1: float):
    """
    Algoritmo de interpolación cúbica de Hermite.
    
    Parameters
    ----------
    t : float
        Tiempo (fotograma) actual.
    t0, t1 : float
        Tiempos inicial y final del segmento.
    x0, x1 : float
        Valores en t0 y t1.
    m0, m1 : float
        Tangentes (velocidades) en t0 y t1.
        
    Returns
    -------
    float
        El valor interpolado x(t).
    """
    delta_t = t1 - t0
    if delta_t == 0.0:
        return x0
        
    # Normalizar t al rango [0, 1]
    t_norm = (t - t0) / delta_t
    
    t2 = t_norm * t_norm
    t3 = t2 * t_norm
    
    # Polinomios base de Hermite
    h00 =  2*t3 - 3*t2 + 1
    h10 =    t3 - 2*t2 + t_norm
    h01 = -2*t3 + 3*t2
    h11 =    t3 -   t2
    
    # Aplicar la fórmula escalando las tangentes por la duración del segmento
    return h00*x0 + h10*m0*delta_t + h01*x1 + h11*m1*delta_t


def catmull_rom(t: float, t0: float, t1: float,
                x_m1: float, x0: float, x1: float, x2: float,
                t_m1: float, t2: float, tension=0.0):
    """
    Interpolación Catmull-Rom (no uniforme)
    basada en Hermite, pero con pasos intermedios explícitos.
    """
    # Factor de tensión: 0.0 = Catmull-Rom estándar
    s = (1 + tension)

    # ----tangentes ----
    dt0 = t1 - t_m1
    dt1 = t2 - t0

    if dt0 != 0:
        m0 = s * (x1 - x_m1) / dt0
    else:
        m0 = 0.0

    if dt1 != 0:
        m1 = s * (x2 - x0) / dt1
    else:
        m1 = 0.0

    # ----Hermite ----
    x_interp = hermite(t, t0, t1, x0, x1, m0, m1)
    return x_interp
