# Escribir un programa que muestre un menú con 2 opciones la primera opción “1.- Imprimir 
# YYYY/MM/DD” la segunda “2.- Imprimir MM/DD/YYYY” una vez seleccionada la opción imprimir la fecha 
# del día de hoy en el formato seleccionado.
import datetime
print("Opciones:")
print("1.- Imprimir YYYY/MM/DD")
print("2.- Imprimir MM/DD/YYYY")
opcion=0
try:
    opcion = int(input("Seleccione en que formato desea imprimir la fecha (1 o 2): "))
except:
    print("Solo puede ingresar 1 o 2")
    exit()

fechaActual = datetime.datetime.now()

if opcion == 1:
    fecha = fechaActual.strftime("%Y/%m/%d")
elif opcion == 2:
    fecha = fechaActual.strftime("%m/%d/%Y")
else:
    print("Solo puede ingresar 1 o 2")
    exit()

print("Fecha actual:", fecha)
