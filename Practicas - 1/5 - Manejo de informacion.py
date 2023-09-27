# Escribir una función que reciba n parámetros de llave valor e imprima la información en formato 
# “{valor}”: “{llave}” 
def imprimirInformacion(**kwargs):
    for llave, valor in kwargs.items():
        print(f'"{valor}": "{llave}"')

#comprobaciones
print("un parametro")
imprimirInformacion(nombre="Juan")
print("\ndos parametros")
imprimirInformacion(nombre="Paco",apellidos="Martinez Lopez")
print("\ntres parametros")
imprimirInformacion(nombre="Pedro Quegus",apellidos="Tode Verte", edad=22)
