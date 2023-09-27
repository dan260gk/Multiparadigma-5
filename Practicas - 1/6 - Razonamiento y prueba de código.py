# Escribir un programa que reciba un numero entre 0 y 20 e imprimir el numero en letra, no utilizar 
# condicionales, máximo 5 líneas de código. 
numeroATexto = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte"]
numero = int(input("Ingrese un numero entre 0 y 20: "))
#supongo que no usar condicionales solo aplica para obtener el numero en texto y no para verificar si el
#valor entra en el rango
print(numeroATexto[numero] if 0 <= numero <= 20 else "Numero fuera del rango.")
