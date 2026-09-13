import re  # Realiza busquedas mediante patrones
import os  # Conocer la ubicacion del archivo

archivo_auditar = "sistema_matriculas.py"

# obtenemos la carpeta donde se encuentra este programa
carpeta_Actual = os.path.dirname(os.path.abspath(__file__))

# construir la ruta completa del archivo
ruta_archivo = os.path.join(carpeta_Actual, archivo_auditar)

print("Archivo que se va a auditar: ")
print(ruta_archivo)


def agregar_hallazgo(lista, id_hallazgo, categoria, numero_linea, evidencia, problema, riesgo, severidad, recomendacion):
    """Registra un hallazgo con la estructura pedida en la matriz de auditoria."""
    lista.append(
        (
            id_hallazgo,
            categoria,
            numero_linea,
            evidencia,
            problema,
            riesgo,
            severidad,
            recomendacion,
        )
    )


def imprimir_hallazgo(id_hallazgo, categoria, numero_linea, evidencia, problema, riesgo, severidad, recomendacion):
    """Muestra un hallazgo con el mismo formato de reporte usado en clase."""
    print("ID:", id_hallazgo)
    print("categoria:", categoria)
    print("linea ", numero_linea)
    print("severidad:", severidad)
    print("evidencia: ", evidencia)
    print("Problema:", problema)
    print("riesgo:", riesgo)
    print("recomendacion:", recomendacion)
    print("___________________________________________________________")


# averiguamos si el archivo existe
if not os.path.exists(ruta_archivo):
    # informamos que el archivo no fue encontrado
    print("Error: El archivo no fue encontrado")

    # Informamos donde se debe ubicar el archivo
    print(
        "Debe ubicar auditor_matriculas.py y sistema_matriculas.py en la misma carpeta"
    )

# Ejecutamos esta parte si el archivo existe
else:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        codigo = archivo.read()

    # dividimos el programa en lineas
    lineas_codigo = codigo.splitlines()

    hallazgos = []  # creamos una lista para almacenar los hallazgos
    codigo_minuscula = codigo.lower()
    contador_id = 1

    # analisis linea por linea, igual que en el ejercicio de clase
    for numero_linea, linea in enumerate(lineas_codigo, start=1):
        linea_minuscula = linea.lower()
        evidencia = linea.strip()

        # Validacion de datos: se leen entradas del usuario sin comprobarlas
        if re.search(r"entrada_\w+\.get\(\)", linea_minuscula):
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Validacion de datos",
                numero_linea,
                evidencia,
                "el dato se toma del formulario y se usa sin validar si esta vacio o es correcto",
                "pueden crearse registros incompletos o con informacion no valida",
                "Alta",
                "validar cada campo antes de usarlo: que no este vacio y que el tipo sea el esperado",
            )
            contador_id += 1

        # Manejo de errores: conversion numerica sin proteccion
        if re.search(r"\bint\s*\(", linea_minuscula) and "try" not in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Manejo de errores",
                numero_linea,
                evidencia,
                "se convierte un dato a entero sin controlar errores",
                "si el usuario deja el campo vacio o escribe texto, el programa se detiene",
                "Alta",
                "usar try/except o comprobar que el valor sea numerico antes de convertirlo",
            )
            contador_id += 1

        # Gestion de archivos: apertura directa sin with ni control de errores
        if re.search(r"\bopen\s*\(", linea_minuscula) and "with " not in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Gestion de archivos",
                numero_linea,
                evidencia,
                "el archivo se abre de forma directa, sin with y sin comprobar si la operacion falla",
                "si el archivo no puede abrirse o escribirse, el sistema falla y ademas el archivo puede quedar abierto",
                "Alta",
                "abrir el archivo con with open y manejar los errores de lectura o escritura",
            )
            contador_id += 1

        # Seguridad de la informacion: datos personales en texto plano
        if "str(estudiante)" in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Seguridad de la informacion",
                numero_linea,
                evidencia,
                "se guarda informacion personal del estudiante en un archivo de texto plano",
                "nombre, documento, edad y programa quedan expuestos y pueden ser leidos o alterados",
                "Alta",
                "restringir el acceso al archivo y no almacenar datos personales sin proteccion",
            )
            contador_id += 1

        # Integridad de los datos: eliminacion dentro del ciclo
        if ".remove(" in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Integridad de los datos",
                numero_linea,
                evidencia,
                "se elimina un elemento de la lista mientras se recorre esa misma lista",
                "puede saltarse un registro, borrar mas de uno o no afectar solo al estudiante esperado",
                "Alta",
                "recorrer una copia de la lista o guardar el elemento y eliminarlo despues del ciclo",
            )
            contador_id += 1

        # Integridad de los datos: se registra sin revisar documentos repetidos
        if "estudiantes.append" in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Integridad de los datos",
                numero_linea,
                evidencia,
                "el estudiante se agrega a la lista sin verificar si el documento ya existe",
                "puede registrarse dos veces el mismo documento y duplicar la informacion",
                "Media",
                "antes de registrar, buscar si el documento ya esta en la lista y rechazar el duplicado",
            )
            contador_id += 1

        # Integridad de los datos: el mensaje no confirma si el estudiante existia
        if "proceso terminado" in linea_minuscula:
            agregar_hallazgo(
                hallazgos,
                "H" + str(contador_id).zfill(2),
                "Integridad de los datos",
                numero_linea,
                evidencia,
                "al eliminar se muestra el mismo mensaje aunque el estudiante no exista",
                "el usuario no sabe si realmente se borro un registro o si no se encontro",
                "Media",
                "informar de forma distinta cuando se elimina y cuando el documento no existe",
            )
            contador_id += 1

    # analisis general del archivo: criterios que no se ven en una sola linea
    # usamos \btry\b para no confundir la palabra try con Entry de tkinter
    if re.search(r"\btry\b", codigo_minuscula) is None:
        agregar_hallazgo(
            hallazgos,
            "H" + str(contador_id).zfill(2),
            "Manejo de errores",
            "general",
            "no aparece ninguna instruccion try/except en el archivo",
            "el sistema no contempla situaciones inesperadas al convertir datos o trabajar con archivos",
            "un error no controlado puede cerrar la aplicacion y perder los datos en memoria",
            "Alta",
            "agregar manejo de excepciones en las operaciones de conversion y de archivos",
        )
        contador_id += 1

    if "with open" not in codigo_minuscula:
        agregar_hallazgo(
            hallazgos,
            "H" + str(contador_id).zfill(2),
            "Gestion de archivos",
            "general",
            "no se usa with open para trabajar el archivo de estudiantes",
            "el archivo de datos no se cierra de forma segura si ocurre un error",
            "pueden perderse datos o quedar el archivo bloqueado",
            "Media",
            "usar with open para garantizar que el archivo se cierre siempre",
        )
        contador_id += 1

    if ".strip(" not in codigo_minuscula and 'if not ' not in codigo_minuscula:
        agregar_hallazgo(
            hallazgos,
            "H" + str(contador_id).zfill(2),
            "Validacion de datos",
            "general",
            "no hay comprobaciones de campos vacios (strip, if not)",
            "el programa no revisa si el usuario deja un campo vacio antes de registrar o calcular",
            "se pueden guardar estudiantes sin nombre, sin documento o con edad vacia",
            "Alta",
            "rechazar el registro cuando algun campo obligatorio este vacio",
        )
        contador_id += 1

    # Mantenibilidad: la interfaz y la logica de negocio estan mezcladas
    if "tkinter" in codigo_minuscula and "def registrar_estudiante" in codigo_minuscula:
        agregar_hallazgo(
            hallazgos,
            "H" + str(contador_id).zfill(2),
            "Mantenibilidad",
            "general",
            "las funciones leen widgets globales y actualizan la interfaz directamente",
            "las funciones no tienen responsabilidades claramente separadas: mezclan captura, regla de negocio e interfaz",
            "cualquier cambio de pantalla o de regla obliga a modificar varias partes del mismo codigo",
            "Media",
            "separar la logica de registro, eliminacion y guardado de la interfaz grafica",
        )
        contador_id += 1

    # mostramos el encabezado del informe
    print("===========================================================")
    print("Reporte de auditoria de software")
    print("Archivo auditado: ", archivo_auditar)
    print("lineas analizadas: ", len(lineas_codigo))
    print("===========================================================")

    if hallazgos:
        print("Hallazgos encontrados:")
        print("___________________________________________________________")
        for (
            id_hallazgo,
            categoria,
            numero_linea,
            evidencia,
            problema,
            riesgo,
            severidad,
            recomendacion,
        ) in hallazgos:
            imprimir_hallazgo(
                id_hallazgo,
                categoria,
                numero_linea,
                evidencia,
                problema,
                riesgo,
                severidad,
                recomendacion,
            )

        # resumen por severidad para apoyar la conclusion de la auditoria
        altas = 0
        medias = 0
        bajas = 0
        for hallazgo in hallazgos:
            if hallazgo[6].lower() == "alta":
                altas += 1
            elif hallazgo[6].lower() == "media":
                medias += 1
            else:
                bajas += 1

        print("Resumen de hallazgos:")
        print("Total:", len(hallazgos))
        print("Alta:", altas)
        print("Media:", medias)
        print("Baja:", bajas)
        print("___________________________________________________________")
        print("Nota: esta herramienta apoya el analisis, no reemplaza el criterio del auditor.")

    else:
        print("No se encontraron posibles hallazgos automaticos en el codigo")
        print("___________________________________________________________")
