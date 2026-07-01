import bpy
import random

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Parámetros
num_cubos = 10
distancia = 2.0  # separación entre cubos

# Crear cubos con ligeras variaciones de tamaño
for i in range(num_cubos):
    tam = random.uniform(0.8, 1.2)
    x = i * distancia
    bpy.ops.mesh.primitive_cube_add(size=tam, location=(x, 0, 0))
    cubo = bpy.context.active_object
 