#Escribir un programa que contenga una función que reciba n parámetros de tipo numérico y calcule el 
#producto total y su suma total.

import random
def calcularProductoSuma(*n):
    producto=1
    suma=0
    for i in n:
        producto=producto*i
        suma=suma+i
    print(f"El producto de todos los numeros es: {producto}\nLa suma de todos los numeros es: {suma}")

valoresentrada = [random.randint(1,10) for _ in range(random.randint(2,10))]
print(f"Valores: {valoresentrada}")
calcularProductoSuma(*valoresentrada)