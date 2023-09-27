# Revisar su retícula para escribir un programa que cree un diccionario vacío para que el usuario capture 
# las materias y créditos de su semestre preferido (inferior a 8vo) al final imprimir en el formato 
# “{asignatura}” tiene “{créditos}” créditos. Y la suma de todos los créditos del semestre y una LISTA de 
# todas las materias 
x="0"
reticula={}
while x=="0":
    s=input("nombre de la asignatura")
    reticula[s]=input("creditos:")
    x = input("ingrese 0 para agregar otra asingatura o 1 para guardar los datos")
print(reticula)

