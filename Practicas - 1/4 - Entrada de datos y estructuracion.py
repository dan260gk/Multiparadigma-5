# Revisar su retícula para escribir un programa que cree un diccionario vacío para que el usuario capture 
# las materias y créditos de su semestre preferido (inferior a 8vo) al final imprimir en el formato 
# “{asignatura}” tiene “{créditos}” créditos. Y la suma de todos los créditos del semestre y una LISTA de 
# todas las materias 
x="0"
semestre={}
totalCreditos=0
materias=[]
while x=="0":
    s=input("\nnombre de la asignatura: ")
    semestre[s]=input("creditos: ")
    x = input("ingrese 0 para agregar otra asingatura o 1 para guardar los datos: ")
for asignatura, creditos in semestre.items():
    print(f'"{asignatura}" tiene "{creditos}" créditos')
    totalCreditos = totalCreditos+int(creditos)
    materias.append(asignatura)

print(f"\nTotal de créditos del semestre: {totalCreditos}")
print(f"lista de materias: {materias}")

