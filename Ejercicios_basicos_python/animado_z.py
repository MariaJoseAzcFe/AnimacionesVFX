import bpy
import random

# Limpieza de escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

num_cubos = 10
distancia = 2.0
frame_inicial = 1
frame_final = 50  

for i in range(num_cubos):
    tam = random.uniform(0.8, 1.2)
    x = i * distancia
    z_inicial = random.uniform(5.0, 8.0)
    z_final = 0.0

    bpy.ops.mesh.primitive_cube_add(size=tam, location=(x, 0, z_inicial))
    obj = bpy.context.active_object

    # Fotograma clave inicial (cubo arriba)
    obj.keyframe_insert(data_path='location', frame=frame_inicial)

    # Posición final (en el suelo)
    obj.location.z = z_final
    obj.keyframe_insert(data_path='location', frame=frame_final)
 