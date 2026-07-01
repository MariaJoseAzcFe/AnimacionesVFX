""" 
Control el movimiento de la coordenada x del objeto activo con
la función get_pos usando un driver.

Si ejecutamos este script, el movimiento del objeto que esté activo 
quedará controlado por el valor de la función get_pos(). Para
ello, este script crea un driver, que lo que hace es vincular el valor
de una propiedad de un objeto al resultado de una expresión en Python.

El script contiene el código para vincular las funciones al movimiento
del cubo.

"""
import bpy
import posicion
from importlib import reload

reload(posicion)

# utilizamos un alias para la función get_posicion, por comodidad
get_posicion = posicion.get_posicion

"""
Código para vincular las funciones al movimiento del cubo
"""

# Le decimos a python que debe considerar la función get_posicion
# como una de las funciones que se pueden llamar desde un driver.
# De esta forma, podemos usarla en una expresión de un driver.
# Allí, se deberá usar el nombre get_pos, que es el nombre que
# se le da a la función en el espacio de nombres de los drivers.
bpy.app.driver_namespace['get_pos'] = get_posicion



# Añadimos un driver, que vincula el valor de una propiedad del objeto
# al valor que devuelve una expresión en Python.
# En este caso, lo hacemos para la propiedad "location", en su
# coordenada 0, que equivale a la coordenada X
# Cambiando el nombre del objeto se cambia el objeto controlado por
# el driver.
obj = bpy.data.objects['Cube']
drv = obj.driver_add('location',0).driver

# La expresión del driver será, simplemente, una llamada a
# get_pos, pasándole el valor del fotograma actual, que está siempre
# guardado en la variable 'frame'.
drv.expression = "get_pos(frame)"

# Cuando llegamos a este punto, se ha creado el driver y el valor de
# la posición del objeto activo ha quedado vinculado al resultado de
# la expresión anterior. Cada vez que cambie el fotograma de la escena
# se llama a la función get_pos (que es un alias para la función
# get_posicion) dándole el número de fotograma, y el
# resultado se guarda en la propiedad location.x del objeto activo.
