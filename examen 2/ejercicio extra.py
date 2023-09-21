import os

def buscarPalabra(archivo, PB):
    archivo = os.path.abspath(archivo)

    if not os.path.exists(archivo):
        return f"El archivo '{archivo}' no se encuentra."

    try:
        with open(archivo, 'r', encoding='utf-8') as AT:
            texto = AT.read()
    except FileNotFoundError:
        return "Error al abrir el archivo."

    palabras = texto.split()

    PI = []

    posicion_actual = 0

    for palabra in palabras:
        palabra = palabra.strip('.,!?').lower()

        if palabra == PB.lower():
            PI.append(posicion_actual)

        posicion_actual += len(palabra) + 1

    return f'La palabra "{PB}" comienza en las posiciones: {PI}'


archivo = "miTexto.txt"  
PB = input("Dame una palabra: ") 
if PB == "":
    print("La cadena no debe estar vacia, intenta nuevamente")
    exit()
if  PB.isdigit() == True:
    print("Debe se una plabra no digitos. Intenta nuevamente")
    exit()
resultado = buscarPalabra(archivo, PB)
print(resultado)
