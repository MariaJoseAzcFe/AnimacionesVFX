def intersect(l1,l2):
    intersec = []
    for x in l1:
        if x in l2: # True si x es un elemento de b
            intersec.append(x)
    return intersec
