"""
Control el movimiento de la coordenada x del objeto activo con
la función get_pos usando keyframes.

Si ejecutamos este script, se insertarán fotogramas clave para
la trayectoria del objeto activo. El script inserta fotogramas clave
en los tiempos y posiciones dictados por la función get_pos().

El script utiliza código del fichero posicion.py, que contiene la
función get_pos().

"""
import bpy
import posicion
from importlib import reload

reload(posicion)

# utilizamos un alias para la función get_posicion, por comodidad
get_posicion = posicion.get_posicion

paso_kf = 5 # Cada cuántos fotogramas insertamos un keyframe


# Almacenamos en una variable el objeto activo
obj = bpy.context.active_object

# Recorremos los fotogramas de la escena, insertando fotogramas clave
# en la posición del objeto activo, según el valor que devuelva
# la función get_pos para cada fotograma.
start = bpy.context.scene.frame_start
end = bpy.context.scene.frame_end
for i in range(start, end, paso_kf):
    obj.location[0] = get_posicion(i)
    obj.keyframe_insert(data_path="location", index=0,frame=i)


