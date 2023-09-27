#Escribir un programa que permita al usuario capturar su nombre completo e imprima su nombre de 
#manera inversa letra por letra intercalando una letra minuscula a una mayuscula ejemplo Luis : s I u L

nombre=input("ingrese su nombre completo: ")
cadena=reversed(list(nombre))
x=True
temp=list()
for _ in cadena:
    if x==True:
        temp.append(_.lower())
        x=False
    else:
        temp.append(_.upper())
        x=True
        
res=" ".join(temp)
print(res)
    