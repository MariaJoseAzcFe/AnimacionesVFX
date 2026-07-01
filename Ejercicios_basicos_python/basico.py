import math 
import boolean_ops 
# ejemplos de bucles for

a = [1,2,"hola"]
a.append("adios")
for v in a:
    print(v)

# otro ejemplo

a = [1,2,"hola","adios"]
b = []
for v in a:
    b.append(v)
    print(v)
print(b)

# otro ejemplo

a = [1,2,"hola","adios"]
b = []
for v in a:
    b.append(v)
    print(v)
    print(b)

# ejercicio: hacer una funcion que calcule la interseccion de dos listas

def intersect(l1,l2):
    intersec = []
    for x in l1:
        if x in l2: # True si x es un elemento de b
            intersec.append(x)
    return intersec
a = [1,3,5,2,7,9]
b = [1,4,1,9,8]
intersec_ab = intersect(a,b)
print(intersec_ab)

# ejercicio: hacer una funcion que calcule la raiz cuadrada de los numeros del 0 al 9

for n in range(10):
    print(math.sqrt(n))


a = [1,3,5,2,7,9]
b = [1,4,1,9,8]
intersec_ab = boolean_ops.intersect(a,b)
print(intersec_ab)

import boolean_ops as bo
a = [1,3,5,2,7,9]
b = [1,4,1,9,8]
intersec_ab = bo.intersect(a,b)
print(intersec_ab)

#from boolean_ops import intersect
a = [1,3,5,2,7,9]
b = [1,4,1,9,8]
intersec_ab = intersect(a,b)
print(intersec_ab)
