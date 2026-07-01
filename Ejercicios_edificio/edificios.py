import bpy
from random import random

def rand_min_max(a,b):
    x = random() * (b - a) 
    x = x + a
    return x
n_cube = 25
tam_cube = 2.0
h = 8.0
dx = 2.5
dy = 2.5

p = (8,15,2)

def crea_edificio(p, n_cube, tam_cube, h, dx, dy):
    for i in range (n_cube):
        posx = rand_min_max(p[0] - dx/2, p[0] + dx/2)
        posy = rand_min_max(p[1] - dx/2, p[1] + dx/2)
        posz = rand_min_max(p[2], p[2]+h)
        bpy.ops.mesh.primitive_cube_add(size=tam_cube, enter_editmode=False, align='WORLD', location=(posx,posy,posz))

if __name__ == "__main__":
    crea_edificio(p, n_cube, tam_cube, h, dx, dy)
     