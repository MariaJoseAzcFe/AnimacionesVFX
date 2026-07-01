import bpy

def delete_objects(prefix):
    """Elimina todos los objetos cuyo nombre empiece por 'prefix'."""
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.context.scene.objects:
        if obj.name.startswith(prefix):
            obj.select_set(True)
    
    bpy.ops.object.delete()
    print(f"🧹 Objetos que comienzan con '{prefix}' eliminados.")
 