import bpy
import random

def borrar_edificios(nombre_comun="Edificio"):
    """Borra todos los objetos que contienen nombre_comun en su nombre"""
    for obj in bpy.data.objects:
        if nombre_comun in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)

def crear_edificio(centro_xy, tam_base, altura, nombre="Edificio"):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = nombre
    
    # Escalar cubo 
    obj.scale = (tam_base/2, tam_base/2, altura)

    # Poner pivote en la base 
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    
    # Mover el objeto a la posición correcta
    # La altura/2 es para que la base quede en z=0 y el edificio crezca hacia arriba
    obj.location = (centro_xy[0], centro_xy[1], altura/2)


def generar_ciudad(P=(0,0,0), Nx=5, Ny=5, L=2.0, w=1.0, h_min=2.0, h_max=8.0):
    """
    Genera una ciudad en forma de rejilla de edificios.

    Args:
        P (tuple): esquina superior izquierda de la ciudad
        Nx, Ny (int): número de manzanas en x e y
        L (float): tamaño de la manzana
        w (float): ancho de las calles
        h_min, h_max (float): rango de alturas de edificios
    """
    for i in range(Nx):
        for j in range(Ny):
            x = P[0] + i * (L + w)
            y = P[1] + j * (L + w)
            altura = random.uniform(h_min, h_max)
            crear_edificio((x, y), L, altura)
 

 
# Script principal
if __name__ == "__main__":
    borrar_edificios()

    # Parámetros
    P = (0, 0, 0)  # esquina superior izquierda
    Nx = 6         
    Ny = 4         
    L = 2.0        # tamaño de la manzana
    w = 0.5        
    h_min = 3.0    
    h_max = 10.0   

    generar_ciudad(P, Nx, Ny, L, w, h_min, h_max)