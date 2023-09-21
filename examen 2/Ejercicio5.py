AUX2 = []
print("Ingrese la cadena y presione enter para ingresar otra. Escriba fin para terminar de escribir")
def CapturarCadenas():
    cadenas = []
    y=0
    while True:
        y+=1
        cadena = input("Cadena "+str(y)+": ")

        if cadena.lower() == 'fin':
            break

        cadenas.append(cadena)
    AUX2 = cadenas
    return cadenas


def obtener(cadenas):

    palabras = []

    for cadena in cadenas:
        palabras.extend(cadena.split())

    return palabras

def mostrar(palabras):

    palabras.sort(key=lambda x: (x.isdigit(), x)) #de gugul :(

    salida=""
    for _ in palabras:
        salida=salida +" " +_ 
    print(f"Salida:{salida}")

        
       

if __name__ == "__main__":
    cadenas = CapturarCadenas()
    palabras = obtener(cadenas)
    mostrar(palabras)
