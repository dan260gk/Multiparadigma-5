#Escribir un programa que almacene el abecedario en una lista, elimine de la lista las letras que ocupen 
#posiciones múltiplos de 2, y muestre por pantalla la lista resultante.
import string
lista=list(string.ascii_lowercase) 
print(f"abecedario: {lista}")
for i in range(0,int(len(lista)/2),2):
  lista.pop(i)
print(lista)
