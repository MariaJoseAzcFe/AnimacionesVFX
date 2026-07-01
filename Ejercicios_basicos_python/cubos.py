import bpy

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crea varios cubos con diferente tamaño y posición
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-3, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 3, 0))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -3, 0))

 