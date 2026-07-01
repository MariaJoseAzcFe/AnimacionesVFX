import bpy
import os
import sys
import random

# Asegurar que se puede importar el script externo
dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

import delete_utils

# Limpiar objetos antiguos antes de crear nuevos
delete_utils.delete_objects("Building")

# Crear una nueva hilera de cubos animados
num_cubos = 10
distancia = 2.0

for i in range(num_cubos):
    tam = random.uniform(0.8, 1.2)
    x = i * distancia
    z_inicial = random.uniform(6.0, 9.0)
    z_final = 0.0

    bpy.ops.mesh.primitive_cube_add(size=tam, location=(x, 0, z_inicial))
    obj = bpy.context.active_object
    obj.name = f"Building_{i}"

    # Animación: caída
    obj.keyframe_insert(data_path='location', frame=1)
    obj.location.z = z_final
    obj.keyframe_insert(data_path='location', frame=50)

print("✅ Edificios generados y animados.")
