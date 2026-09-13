import re  # Realiza busquedas mediante patrones
import os  # Conocer la ubicación del archivo

archivo_auditar = "sistema_ventas.py"

# obtenemos la carptea donde se encuentra este programa
carpeta_Actual = os.path.dirname(os.path.abspath(__file__))

# construir la ruta completa del archivo
ruta_archivo = os.path.join(carpeta_Actual, archivo_auditar)

print("Aechivo que se va a auditar: ")
print(ruta_archivo)

# averiguamos si el archivo existe
if not os.path.exists(ruta_archivo):
    # informamos que el archivo no fue encontrado
    print("Error: El archivo no fue encontrado")

    # Informamos donde se debe ubicar el archivo
    print(
        "Debe ubicar Auditoria_software.py y sistema_ventas.py en la misma carpeta que el archivo a auditar"
    )

    #Ejecutamos esta parte si el archivo existe
else:
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        codigo = archivo.read()

        # dividimos el programa en linea

        lineas_codigo = codigo.splitlines()

        hallazgos = [] #creamos una lista para almacenar los hallazgos

for numero_linea, linea in enumerate(lineas_codigo, start=1):
    
    linea_minuscula = linea.lower()
    if "contrasena" in linea_minuscula:
        hallazgos.append((numero_linea, linea.strip()))

#mostramos el encabezado del informe
print("===========================================================")
print("Reporte de auditoria de software")
print("Archivo auditado: ", archivo_auditar)
print("lineas analizadas: ", len(lineas_codigo))
print("===========================================================")

if hallazgos:
    print("Hallazgos encontrados:")
    print("___________________________________________________________")
    for numero_linea, evidencia in hallazgos:
        print("linea ", numero_linea)
        print("severidad: alta")
        print("evidencia: ", evidencia)

        #explicamos el problema encontrado
        print("Problema:posible contraseña almacenada directamente en el codigo")
        print("recomendacion: usar variables de entorno o archivos de configuracion para almacenar las contraseñas")
        print("___________________________________________________________")

else:
    print("No se encontraron posibles contraseñas almacenadas directamente en el codigo")
    print("___________________________________________________________")

