# --------------------------------------------------------------
# SISTEMA DE AUDITORÍA - CASO GÉNESIS (UDES)
# --------------------------------------------------------------
# Herramienta de apoyo para el taller de Auditoría de Software.
#
# Caso auditado: Sistema de Información Académica "Génesis" de la
# Universidad de Santander (UDES).
#
# Las 5 vulnerabilidades intencionales del caso:
#   V1 - Falta de gestión de capacidad / sin sistema de colas
#   V2 - Política de contraseñas débil
#   V3 - Cuentas de usuario sin desactivar
#   V4 - Backups sin pruebas de restauración
#   V5 - Software e infraestructura desactualizada
#
# FUNCIONAMIENTO:
#   1. En cada pestaña V1..V5 los campos vienen precargados con la
#      evidencia del caso; basta presionar "Agregar registro".
#   2. El sistema aplica el criterio de auditoría y clasifica cada
#      registro como CUMPLE o NO CUMPLE.
#   3. Con "Auditar selección" se abre el resultado detallado del
#      registro elegido.
#   4. La pestaña "Resultados" consolida los hallazgos por
#      vulnerabilidad y permite exportar el informe.
# --------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta


# ==============================================================
# CONFIGURACIÓN GENERAL
# ==============================================================

COLOR_PRINCIPAL = "#173F5F"
COLOR_SECUNDARIO = "#20639B"
COLOR_EXITO = "#2A9D8F"
COLOR_ALERTA = "#F4A261"
COLOR_ERROR = "#E76F51"
COLOR_FONDO = "#F4F7FA"
COLOR_BLANCO = "#FFFFFF"

FILA_NO_CUMPLE = "#FBE2E1"
FILA_CUMPLE = "#E3F5F1"

FORMATO_FECHA = "%Y-%m-%d"


def parsear_fecha(texto):
    """Convierte un texto AAAA-MM-DD en un objeto date."""
    return datetime.strptime(texto.strip(), FORMATO_FECHA).date()


def dias_entre(fecha_inicial, fecha_final=None):
    """Días transcurridos entre una fecha y hoy (o una fecha final dada)."""
    if fecha_final is None:
        fecha_final = date.today()
    return (fecha_final - fecha_inicial).days


def hace(dias):
    """Devuelve como texto la fecha de hace N días (útil para los ejemplos)."""
    return (date.today() - timedelta(days=dias)).isoformat()


# ==============================================================
# ALMACENAMIENTO DE REGISTROS
# ==============================================================

registros = {
    "V1": [],
    "V2": [],
    "V3": [],
    "V4": [],
    "V5": [],
}


# ==============================================================
# FICHA TECNICA DE CADA VULNERABILIDAD
# ==============================================================
# Esta información alimenta la ventana de "Auditar selección" y el
# informe exportado.

FICHAS = {
    "V1": {
        "titulo": "Falta de gestión de capacidad y ausencia de sistema de colas",
        "proceso": "Matrícula académica",
        "criterio": ("ISO/IEC 27001 A.17 - Gestión de la capacidad y continuidad. "
                     "En periodos críticos la infraestructura debe soportar la demanda "
                     "concurrente o contar con balanceo de carga / fila virtual."),
        "causa": ("Dos servidores on-premise sin balanceo de carga, sin réplicas y sin "
                  "política formal de gestión de capacidad para el periodo de matrícula."),
        "efecto": ("Degradación severa del servicio: tiempos de espera altos, caídas de "
                   "sesión e imposibilidad de matricular, afectando a miles de estudiantes."),
        "recomendación": ("Implementar balanceo de carga y un sistema de fila virtual para la "
                          "matrícula, definir una política de capacidad con pruebas de carga "
                          "previas a cada periodo y evaluar auto-escalamiento."),
        "riesgo": "Alto",
    },
    "V2": {
        "titulo": "Política de contraseñas débil",
        "proceso": "Gestión de accesos",
        "criterio": ("ISO/IEC 27001 A.9.4.3 - Sistema de gestión de contraseñas. Mínimo 8 "
                     "caracteres, combinación de mayúsculas, números y símbolos, y caducidad "
                     "no mayor a 90 días."),
        "causa": ("Política de contraseñas incompleta: exige solo 6 caracteres, sin exigir "
                  "complejidad ni caducidad periódica."),
        "efecto": ("Facilita ataques de fuerza bruta y de diccionario sobre cuentas de "
                   "estudiantes y docentes, con posible acceso a notas y datos personales."),
        "recomendación": ("Actualizar la política a mínimo 8 caracteres con complejidad "
                          "obligatoria, caducidad cada 90 días, bloqueo por intentos fallidos "
                          "y segundo factor para perfiles administrativos."),
        "riesgo": "Alto",
    },
    "V3": {
        "titulo": "Cuentas de egresados y exfuncionarios sin desactivar",
        "proceso": "Baja de usuarios",
        "criterio": ("ISO/IEC 27001 A.9.2.6 - Retiro o ajuste de los derechos de acceso. "
                     "Las cuentas deben desactivarse al finalizar el vínculo con la institucion."),
        "causa": ("No existe un proceso formal de baja de usuarios ni revisión periódica de "
                  "perfiles en Génesis."),
        "efecto": ("Accesos no autorizados por personas sin vínculo vigente, con riesgo sobre "
                   "información académica y personal, y perdida de trazabilidad."),
        "recomendación": ("Formalizar el procedimiento de baja integrado con Talento Humano y "
                          "Registro y Control, con desactivacion automática y revisión "
                          "trimestral de cuentas activas."),
        "riesgo": "Alto",
    },
    "V4": {
        "titulo": "Copias de seguridad sin pruebas de restauración",
        "proceso": "Respaldo y recuperación",
        "criterio": ("ISO/IEC 27001 A.12.3.1 - Copias de respaldo. Las copias deben probarse "
                     "periódicamente (referencia de auditoría: al menos cada 180 días) y "
                     "documentarse la prueba."),
        "causa": ("El area de TI ejecuta backups diarios pero nunca ha ejecutado una prueba "
                  "de restauración documentada."),
        "efecto": ("No hay certeza técnica de que la información pueda recuperarse ante un "
                   "incidente; el respaldo puede resultar inservible justo cuando se necesita."),
        "recomendación": ("Definir un calendario de pruebas de restauración en ambiente de "
                          "pruebas, documentar cada ejercicio con actas y medir el tiempo real "
                          "de recuperación (RTO/RPO)."),
        "riesgo": "Crítico",
    },
    "V5": {
        "titulo": "Software e infraestructura desactualizada",
        "proceso": "Gestión de vulnerabilidades técnicas",
        "criterio": ("ISO/IEC 27001 A.12.6.1 - Gestión de vulnerabilidades técnicas. Los "
                     "componentes deben tener soporte vigente del fabricante y parches de "
                     "seguridad aplicados en los últimos 365 días."),
        "causa": ("Aplicación desarrollada hace 8 años sobre un framework fuera de soporte y "
                  "motor de base de datos con mas de 6 años de antigüedad, sin parches "
                  "recientes."),
        "efecto": ("Exposición a vulnerabilidades conocidas y publicadas, sin posibilidad de "
                   "recibir correcciones oficiales del fabricante."),
        "recomendación": ("Elaborar un plan de actualización tecnológica por fases, aplicar "
                          "parches de seguridad de forma programada y mantener un inventario "
                          "de componentes con su fecha de fin de soporte."),
        "riesgo": "Alto",
    },
}

ORDEN = ("V1", "V2", "V3", "V4", "V5")


# ==============================================================
# CRITERIOS DE EVALUACION AUTOMATICA
# ==============================================================

def evaluar_capacidad(usuarios_conectados, capacidad_maxima, balanceo, colas):
    supera_capacidad = usuarios_conectados > capacidad_maxima
    tiene_mitigacion = (balanceo == "Sí") or (colas == "Sí")

    if supera_capacidad and not tiene_mitigacion:
        return ("NO CUMPLE",
                f"{usuarios_conectados} usuarios conectados superan la capacidad máxima "
                f"({capacidad_maxima}) y no existe balanceo de carga ni sistema de colas "
                f"que regule el ingreso.")
    if supera_capacidad and tiene_mitigacion:
        return ("CUMPLE",
                "Se supera la capacidad base, pero existe un mecanismo de mitigación "
                "(balanceo de carga o fila virtual).")
    return ("CUMPLE", "La conexión simultánea está dentro de la capacidad soportada.")


def evaluar_password(longitud, mayus, numeros, simbolos, caduca, dias_desde_cambio):
    fallas = []
    if longitud < 8:
        fallas.append(f"longitud de {longitud} caracteres (mínimo 8)")
    if mayus == "No":
        fallas.append("no exige mayúsculas")
    if numeros == "No":
        fallas.append("no exige números")
    if simbolos == "No":
        fallas.append("no exige símbolos")
    if caduca == "No":
        fallas.append("la contraseña no caduca nunca")
    elif dias_desde_cambio is not None and dias_desde_cambio > 90:
        fallas.append(f"sin cambio hace {dias_desde_cambio} dias (máximo 90)")

    if fallas:
        return ("NO CUMPLE", "Incumple: " + "; ".join(fallas) + ".")
    return ("CUMPLE", "La contraseña cumple los criterios mínimos de complejidad y vigencia.")


def evaluar_cuenta(estado_cuenta, fecha_retiro_texto):
    if estado_cuenta == "Activa" and fecha_retiro_texto.strip() != "":
        try:
            fecha_retiro = parsear_fecha(fecha_retiro_texto)
        except ValueError:
            return ("DATO INVÁLIDO", "La fecha de retiro no tiene el formato AAAA-MM-DD.")

        if fecha_retiro <= date.today():
            dias = dias_entre(fecha_retiro)
            return ("NO CUMPLE",
                    f"La persona finalizó su vínculo el {fecha_retiro.isoformat()} "
                    f"(hace {dias} dias) y la cuenta continúa activa.")

    return ("CUMPLE",
            "La cuenta corresponde a una persona con vínculo vigente o ya fue desactivada.")


def evaluar_backup(prueba_restauracion, fecha_ultima_prueba_texto):
    if prueba_restauracion == "No":
        return ("NO CUMPLE",
                "Nunca se ha realizado una prueba de restauración sobre está copia de seguridad.")

    if fecha_ultima_prueba_texto.strip() == "":
        return ("NO CUMPLE",
                "Se indica que hubo prueba, pero no se registro la fecha (falta evidencia).")

    try:
        fecha_prueba = parsear_fecha(fecha_ultima_prueba_texto)
    except ValueError:
        return ("DATO INVÁLIDO", "La fecha de la última prueba no tiene el formato AAAA-MM-DD.")

    dias = dias_entre(fecha_prueba)
    if dias > 180:
        return ("NO CUMPLE", f"La última prueba de restauración fue hace {dias} dias (máximo 180).")

    return ("CUMPLE", f"Prueba de restauración vigente, realizada hace {dias} dias.")


def evaluar_software(soporte, fecha_ultimo_parche_texto):
    fallas = []

    if soporte == "Vencido":
        fallas.append("sin soporte vigente del fabricante")

    if fecha_ultimo_parche_texto.strip() == "":
        fallas.append("sin fecha registrada del último parche")
    else:
        try:
            fecha_parche = parsear_fecha(fecha_ultimo_parche_texto)
        except ValueError:
            return ("DATO INVÁLIDO", "La fecha del último parche no tiene el formato AAAA-MM-DD.")
        dias = dias_entre(fecha_parche)
        if dias > 365:
            fallas.append(f"sin parches hace {dias} dias (máximo 365)")

    if fallas:
        return ("NO CUMPLE", "Incumple: " + "; ".join(fallas) + ".")
    return ("CUMPLE", "El componente cuenta con soporte vigente y parches recientes.")


# ==============================================================
# DATOS PRECARGADOS DEL CASO
# ==============================================================
# Cada pestaña muestra sus campos ya diligenciados con evidencia del
# caso. El usuario solo presiona "Agregar". Al agregar, el formulario
# se recarga automaticamente con el siguiente ejemplo pendiente.

EJEMPLOS = {
    "V1": [
        {"fecha": hace(20), "usuarios": "5200", "capacidad": "1800", "balanceo": "No", "colas": "No",
         "nota": "Primer día de matrícula académica - pico máximo"},
        {"fecha": hace(19), "usuarios": "4300", "capacidad": "1800", "balanceo": "No", "colas": "No",
         "nota": "Segundo día de matrícula - liberación gradual"},
        {"fecha": hace(5), "usuarios": "950", "capacidad": "1800", "balanceo": "No", "colas": "No",
         "nota": "Día hábil ordinario fuera de matrícula"},
    ],
    "V2": [
        {"usuario": "Estudiantes (perfil general)", "longitud": "6", "días": "",
         "mayus": "No", "números": "No", "símbolos": "No", "caduca": "No",
         "nota": "Política vigente segun el caso: 6 caracteres, sin complejidad"},
        {"usuario": "Docentes", "longitud": "6", "días": "",
         "mayus": "No", "números": "No", "símbolos": "No", "caduca": "No",
         "nota": "Misma política aplicada al perfil docente"},
        {"usuario": "Registro y Control (administrativo)", "longitud": "8", "días": "45",
         "mayus": "Sí", "números": "Sí", "símbolos": "Sí", "caduca": "Sí",
         "nota": "Perfil administrativo con configuración reforzada"},
    ],
    "V3": [
        {"usuario": "Egresado - Ing. Sistemas", "tipo": "Estudiante egresado", "estado": "Activa",
         "retiro": hace(210), "nota": "Graduado hace mas de 6 meses, cuenta activa"},
        {"usuario": "Exdocente - Facultad Salud", "tipo": "Exdocente", "estado": "Activa",
         "retiro": hace(150), "nota": "Contrato finalizado, sin baja del usuario"},
        {"usuario": "Exfuncionario - Área financiera", "tipo": "Exfuncionario", "estado": "Inactiva",
         "retiro": hace(90), "nota": "Cuenta desactivada correctamente"},
        {"usuario": "Estudiante activo - Derecho", "tipo": "Estudiante activo", "estado": "Activa",
         "retiro": "", "nota": "Vínculo vigente, acceso legitimo"},
    ],
    "V4": [
        {"fecha": hace(1), "tipo": "Completo", "prueba": "No", "fecha_prueba": "",
         "nota": "Backup diario de la base de datos, sin prueba de restauración"},
        {"fecha": hace(2), "tipo": "Incremental", "prueba": "No", "fecha_prueba": "",
         "nota": "Copia incremental, tampoco verificada"},
        {"fecha": hace(30), "tipo": "Completo", "prueba": "No", "fecha_prueba": "",
         "nota": "Copia mensual almacenada, nunca restaurada"},
    ],
    "V5": [
        {"componente": "Framework web del aplicativo", "versión": "v3.2 (8 años de antigüedad)",
         "soporte": "Vencido", "parche": hace(760),
         "nota": "Framework fuera de soporte del fabricante"},
        {"componente": "Motor de base de datos", "versión": "Versión con mas de 6 años",
         "soporte": "Vencido", "parche": hace(700),
         "nota": "Servidor único, sin réplica ni clúster"},
        {"componente": "Sistema operativo del servidor", "versión": "Edición servidor legada",
         "soporte": "Vencido", "parche": hace(540),
         "nota": "Servidor on-premise del centro de cómputo"},
        {"componente": "Antivirus / endpoint del servidor", "versión": "Versión actual",
         "soporte": "Vigente", "parche": hace(20),
         "nota": "Componente sí actualizado (control que sí cumple)"},
    ],
}

indice_ejemplo = {"V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0}


# ==============================================================
# FUNCIONES DE APOYO A LAS TABLAS
# ==============================================================

def pintar_fila(tabla):
    tabla.tag_configure("NO CUMPLE", background=FILA_NO_CUMPLE)
    tabla.tag_configure("CUMPLE", background=FILA_CUMPLE)


def registrar(clave, tabla, registro, valores):
    """Guarda el registro, lo muestra en la tabla y refresca los totales."""
    registros[clave].append(registro)
    indice = len(registros[clave]) - 1
    tabla.insert("", "end", iid=str(indice), values=valores, tags=(registro["estado"],))
    pintar_fila(tabla)
    actualizar_resumen()


# ==============================================================
# ALTAS DE REGISTROS (BOTON "AGREGAR")
# ==============================================================

def agregar_capacidad():
    try:
        fecha = parsear_fecha(entry_v1_fecha.get())
        usuarios = int(entry_v1_usuarios.get())
        capacidad = int(entry_v1_capacidad.get())
    except ValueError:
        messagebox.showerror("Dato inválido",
                             "Revise la fecha (AAAA-MM-DD) y que usuarios/capacidad sean números enteros.")
        return

    balanceo = combo_v1_balanceo.get()
    colas = combo_v1_colas.get()

    if balanceo == "" or colas == "":
        messagebox.showwarning("Información requerida",
                               "Seleccione si existe balanceo de carga y sistema de colas.")
        return

    estado, detalle = evaluar_capacidad(usuarios, capacidad, balanceo, colas)

    registro = {
        "fecha": fecha.isoformat(),
        "usuarios": usuarios,
        "capacidad": capacidad,
        "balanceo": balanceo,
        "colas": colas,
        "nota": entry_v1_nota.get().strip(),
        "estado": estado,
        "detalle": detalle,
    }

    registrar("V1", tabla_v1, registro,
              (registro["fecha"], usuarios, capacidad, balanceo, colas, estado))
    precargar("V1", avanzar=True)


def agregar_password():
    usuario = entry_v2_usuario.get().strip()
    if usuario == "":
        messagebox.showwarning("Información requerida",
                               "Ingrese el usuario o perfil evaluado (ej: Estudiantes, Docentes).")
        return

    try:
        longitud = int(entry_v2_longitud.get())
    except ValueError:
        messagebox.showerror("Dato inválido", "La longitud mínima debe ser un numero entero.")
        return

    mayus = combo_v2_mayus.get()
    numeros = combo_v2_numeros.get()
    simbolos = combo_v2_simbolos.get()
    caduca = combo_v2_caduca.get()

    if "" in (mayus, numeros, simbolos, caduca):
        messagebox.showwarning("Información requerida", "Complete todas las selecciones Sí/No.")
        return

    dias_texto = entry_v2_dias.get().strip()
    dias_desde_cambio = int(dias_texto) if dias_texto.isdigit() else None

    estado, detalle = evaluar_password(longitud, mayus, numeros, simbolos, caduca, dias_desde_cambio)

    registro = {
        "usuario": usuario,
        "longitud": longitud,
        "días_cambio": dias_texto if dias_texto else "N/A",
        "mayus": mayus,
        "números": numeros,
        "símbolos": simbolos,
        "caduca": caduca,
        "nota": entry_v2_nota.get().strip(),
        "estado": estado,
        "detalle": detalle,
    }

    registrar("V2", tabla_v2, registro,
              (usuario, longitud, mayus, numeros, simbolos, caduca, estado))
    precargar("V2", avanzar=True)


def agregar_cuenta():
    usuario = entry_v3_usuario.get().strip()
    if usuario == "":
        messagebox.showwarning("Información requerida",
                               "Ingrese el identificador o rol del usuario.")
        return

    tipo = combo_v3_tipo.get()
    estado_cuenta = combo_v3_estado.get()

    if tipo == "" or estado_cuenta == "":
        messagebox.showwarning("Información requerida",
                               "Seleccione el tipo de usuario y el estado de la cuenta.")
        return

    fecha_retiro_texto = entry_v3_fecha_retiro.get().strip()
    estado, detalle = evaluar_cuenta(estado_cuenta, fecha_retiro_texto)

    if estado == "DATO INVÁLIDO":
        messagebox.showerror("Dato inválido", detalle)
        return

    registro = {
        "usuario": usuario,
        "tipo": tipo,
        "estado_cuenta": estado_cuenta,
        "fecha_retiro": fecha_retiro_texto if fecha_retiro_texto else "N/A",
        "nota": entry_v3_nota.get().strip(),
        "estado": estado,
        "detalle": detalle,
    }

    registrar("V3", tabla_v3, registro,
              (usuario, tipo, estado_cuenta, registro["fecha_retiro"], estado))
    precargar("V3", avanzar=True)


def agregar_backup():
    try:
        fecha_backup = parsear_fecha(entry_v4_fecha.get())
    except ValueError:
        messagebox.showerror("Dato inválido", "La fecha del backup debe tener formato AAAA-MM-DD.")
        return

    tipo = combo_v4_tipo.get()
    prueba = combo_v4_prueba.get()

    if tipo == "" or prueba == "":
        messagebox.showwarning("Información requerida",
                               "Seleccione el tipo de copia y si hubo prueba de restauración.")
        return

    fecha_prueba_texto = entry_v4_fecha_prueba.get().strip()
    estado, detalle = evaluar_backup(prueba, fecha_prueba_texto)

    if estado == "DATO INVÁLIDO":
        messagebox.showerror("Dato inválido", detalle)
        return

    registro = {
        "fecha_backup": fecha_backup.isoformat(),
        "tipo": tipo,
        "prueba": prueba,
        "fecha_prueba": fecha_prueba_texto if fecha_prueba_texto else "N/A",
        "nota": entry_v4_nota.get().strip(),
        "estado": estado,
        "detalle": detalle,
    }

    registrar("V4", tabla_v4, registro,
              (registro["fecha_backup"], tipo, prueba, registro["fecha_prueba"], estado))
    precargar("V4", avanzar=True)


def agregar_software_infra():
    componente = entry_v5_componente.get().strip()
    if componente == "":
        messagebox.showwarning("Información requerida",
                               "Ingrese el nombre del componente (ej: Framework web, Motor de BD).")
        return

    version = entry_v5_version.get().strip()
    soporte = combo_v5_soporte.get()

    if soporte == "":
        messagebox.showwarning("Información requerida",
                               "Seleccione el estado de soporte del fabricante.")
        return

    fecha_parche_texto = entry_v5_fecha_parche.get().strip()
    estado, detalle = evaluar_software(soporte, fecha_parche_texto)

    if estado == "DATO INVÁLIDO":
        messagebox.showerror("Dato inválido", detalle)
        return

    registro = {
        "componente": componente,
        "versión": version,
        "soporte": soporte,
        "fecha_parche": fecha_parche_texto if fecha_parche_texto else "N/A",
        "nota": entry_v5_nota.get().strip(),
        "estado": estado,
        "detalle": detalle,
    }

    registrar("V5", tabla_v5, registro,
              (componente, version, soporte, registro["fecha_parche"], estado))
    precargar("V5", avanzar=True)


# ==============================================================
# PRECARGA DE FORMULARIOS CON LOS DATOS DEL CASO
# ==============================================================

def _set_entry(widget, valor):
    widget.delete(0, tk.END)
    widget.insert(0, valor)


def precargar(clave, avanzar=False):
    """Deja el formulario de la pestaña listo con el siguiente ejemplo del caso."""
    lista = EJEMPLOS[clave]

    if avanzar:
        indice_ejemplo[clave] += 1

    if indice_ejemplo[clave] >= len(lista):
        indice_ejemplo[clave] = 0

    datos = lista[indice_ejemplo[clave]]
    posicion = f"Ejemplo {indice_ejemplo[clave] + 1} de {len(lista)}"

    if clave == "V1":
        _set_entry(entry_v1_fecha, datos["fecha"])
        _set_entry(entry_v1_usuarios, datos["usuarios"])
        _set_entry(entry_v1_capacidad, datos["capacidad"])
        combo_v1_balanceo.set(datos["balanceo"])
        combo_v1_colas.set(datos["colas"])
        _set_entry(entry_v1_nota, datos["nota"])
        label_v1_pos.config(text=posicion)

    elif clave == "V2":
        _set_entry(entry_v2_usuario, datos["usuario"])
        _set_entry(entry_v2_longitud, datos["longitud"])
        _set_entry(entry_v2_dias, datos["días"])
        combo_v2_mayus.set(datos["mayus"])
        combo_v2_numeros.set(datos["números"])
        combo_v2_simbolos.set(datos["símbolos"])
        combo_v2_caduca.set(datos["caduca"])
        _set_entry(entry_v2_nota, datos["nota"])
        label_v2_pos.config(text=posicion)

    elif clave == "V3":
        _set_entry(entry_v3_usuario, datos["usuario"])
        combo_v3_tipo.set(datos["tipo"])
        combo_v3_estado.set(datos["estado"])
        _set_entry(entry_v3_fecha_retiro, datos["retiro"])
        _set_entry(entry_v3_nota, datos["nota"])
        label_v3_pos.config(text=posicion)

    elif clave == "V4":
        _set_entry(entry_v4_fecha, datos["fecha"])
        combo_v4_tipo.set(datos["tipo"])
        combo_v4_prueba.set(datos["prueba"])
        _set_entry(entry_v4_fecha_prueba, datos["fecha_prueba"])
        _set_entry(entry_v4_nota, datos["nota"])
        label_v4_pos.config(text=posicion)

    elif clave == "V5":
        _set_entry(entry_v5_componente, datos["componente"])
        _set_entry(entry_v5_version, datos["versión"])
        combo_v5_soporte.set(datos["soporte"])
        _set_entry(entry_v5_fecha_parche, datos["parche"])
        _set_entry(entry_v5_nota, datos["nota"])
        label_v5_pos.config(text=posicion)


def precargar_todo():
    for clave in ORDEN:
        indice_ejemplo[clave] = 0
        precargar(clave)


def siguiente_ejemplo(clave):
    precargar(clave, avanzar=True)


def cargar_todos_los_ejemplos():
    """Carga de una sola vez toda la evidencia del caso en las 5 pestañas."""
    if sum(len(v) for v in registros.values()) > 0:
        if not messagebox.askyesno("Cargar evidencia completa",
                                   "Ya existen registros cargados. Se agregaran los ejemplos "
                                   "del caso a lo que ya hay. Desea continuar?"):
            return

    for clave in ORDEN:
        indice_ejemplo[clave] = 0
        for _ in range(len(EJEMPLOS[clave])):
            precargar(clave)
            if clave == "V1":
                agregar_capacidad()
            elif clave == "V2":
                agregar_password()
            elif clave == "V3":
                agregar_cuenta()
            elif clave == "V4":
                agregar_backup()
            elif clave == "V5":
                agregar_software_infra()

    messagebox.showinfo("Evidencia cargada",
                        "Se cargo toda la evidencia del caso Génesis en las cinco pestañas.\n\n"
                        "Use 'Auditar selección' en cada pestaña para ver el análisis detallado "
                        "de un registro.")


# ==============================================================
# BOTON "AUDITAR SELECCIÓN" - VENTANA DE RESUMEN
# ==============================================================

def descripcion_registro(clave, r):
    """Arma la lista de campos que se muestran en la ventana de análisis."""
    if clave == "V1":
        return [
            ("Fecha de la medición", r["fecha"]),
            ("Usuarios conectados", r["usuarios"]),
            ("Capacidad máxima del servidor", r["capacidad"]),
            ("Exceso sobre la capacidad", max(0, r["usuarios"] - r["capacidad"])),
            ("Balanceo de carga", r["balanceo"]),
            ("Sistema de colas / fila virtual", r["colas"]),
        ]
    if clave == "V2":
        return [
            ("Usuario / perfil evaluado", r["usuario"]),
            ("Longitud mínima exigida", r["longitud"]),
            ("Exige mayúsculas", r["mayus"]),
            ("Exige números", r["números"]),
            ("Exige símbolos", r["símbolos"]),
            ("Caduca periódicamente", r["caduca"]),
            ("Días desde el último cambio", r["días_cambio"]),
        ]
    if clave == "V3":
        return [
            ("Usuario", r["usuario"]),
            ("Tipo de vínculo", r["tipo"]),
            ("Estado de la cuenta", r["estado_cuenta"]),
            ("Fecha de retiro", r["fecha_retiro"]),
        ]
    if clave == "V4":
        return [
            ("Fecha de la copia", r["fecha_backup"]),
            ("Tipo de copia", r["tipo"]),
            ("Prueba de restauración", r["prueba"]),
            ("Fecha de la última prueba", r["fecha_prueba"]),
        ]
    return [
        ("Componente", r["componente"]),
        ("Versión", r["versión"]),
        ("Soporte del fabricante", r["soporte"]),
        ("Fecha del último parche", r["fecha_parche"]),
    ]


def auditar_seleccion(clave, tabla):
    """Abre el resumen de auditoría del registro seleccionado en la tabla."""
    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning("Selección requerida",
                               "Seleccione una fila de la tabla para generar el análisis de auditoría.")
        return

    indice = int(seleccion[0])
    registro = registros[clave][indice]
    ficha = FICHAS[clave]
    es_hallazgo = registro["estado"] == "NO CUMPLE"

    ventana = tk.Toplevel(root)
    ventana.title(f"Análisis de auditoría - {clave}")
    ventana.geometry("740x620")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(root)

    # ---------- Encabezado ----------
    cabecera = tk.Frame(ventana, bg=COLOR_ERROR if es_hallazgo else COLOR_EXITO)
    cabecera.pack(fill="x")

    tk.Label(cabecera,
             text="HALLAZGO DE AUDITORÍA" if es_hallazgo else "CONTROL SIN OBSERVACIONES",
             font=("Arial", 16, "bold"), bg=cabecera["bg"], fg=COLOR_BLANCO).pack(pady=(14, 2))

    tk.Label(cabecera, text=f"{clave}. {ficha['titulo']}",
             font=("Arial", 10), bg=cabecera["bg"], fg=COLOR_BLANCO,
             wraplength=700).pack(pady=(0, 12))

    # ---------- Área con scroll ----------
    contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=15, pady=12)

    canvas = tk.Canvas(contenedor, bg=COLOR_FONDO, highlightthickness=0)
    scroll = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    cuerpo = tk.Frame(canvas, bg=COLOR_FONDO)

    cuerpo.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=cuerpo, anchor="nw", width=700)
    canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # ---------- Evidencia registrada ----------
    marco = tk.LabelFrame(cuerpo, text=" Evidencia registrada ", bg=COLOR_BLANCO,
                          fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=15, pady=12)
    marco.pack(fill="x", pady=(0, 12))

    for etiqueta, valor in descripcion_registro(clave, registro):
        fila = tk.Frame(marco, bg=COLOR_BLANCO)
        fila.pack(fill="x", pady=3)
        tk.Label(fila, text=etiqueta + ":", font=("Arial", 9, "bold"), width=30,
                 anchor="w", bg=COLOR_BLANCO).pack(side="left")
        tk.Label(fila, text=str(valor), font=("Arial", 9), anchor="w",
                 bg=COLOR_BLANCO, wraplength=380, justify="left").pack(side="left")

    if registro.get("nota"):
        fila = tk.Frame(marco, bg=COLOR_BLANCO)
        fila.pack(fill="x", pady=3)
        tk.Label(fila, text="Observación del auditor:", font=("Arial", 9, "bold"), width=30,
                 anchor="w", bg=COLOR_BLANCO).pack(side="left")
        tk.Label(fila, text=registro["nota"], font=("Arial", 9, "italic"), anchor="w",
                 bg=COLOR_BLANCO, wraplength=380, justify="left").pack(side="left")

    # ---------- Conclusión preliminar ----------
    if es_hallazgo:
        conclusion = registro["detalle"]
    else:
        conclusion = ("Con la evidencia registrada, este elemento se encuentra dentro de lo "
                      "esperado y no genera hallazgo de auditoría.")

    tk.Label(cuerpo, text="CONCLUSIÓN PRELIMINAR", font=("Arial", 12, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=(10, 6))

    tk.Label(cuerpo, text=conclusion, wraplength=660, justify="left",
             font=("Arial", 10), bg=COLOR_FONDO).pack(fill="x", padx=10)

    # ---------- Advertencia ----------
    tk.Label(cuerpo,
             text=("IMPORTANTE: el resultado del sistema es apoyo a la auditoría y no "
                   "constituye por sí solo la calificación final del hallazgo. El auditor debe "
                   "validar la evidencia y entrevistar a los responsables del proceso."),
             wraplength=660, justify="left", font=("Arial", 8, "italic"),
             bg="#FFF3CD", fg="#856404", padx=12, pady=10).pack(fill="x", pady=12)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg=COLOR_PRINCIPAL,
              fg=COLOR_BLANCO, font=("Arial", 10, "bold"), padx=20).pack(pady=(0, 12))


def ver_detalle_vulnerabilidad():
    """Desde la pestaña de resultados, abre el consolidado de la vulnerabilidad elegida."""
    seleccion = tabla_resultados.selection()
    if not seleccion:
        messagebox.showwarning("Selección requerida",
                               "Seleccione una vulnerabilidad de la tabla de resultados.")
        return

    clave = tabla_resultados.item(seleccion[0], "values")[0]
    lista = registros[clave]

    if not lista:
        messagebox.showinfo("Sin evidencia",
                            f"Todavía no se ha cargado evidencia para {clave}.")
        return

    ficha = FICHAS[clave]
    no_cumple = [r for r in lista if r["estado"] == "NO CUMPLE"]
    hay_hallazgo = len(no_cumple) > 0

    ventana = tk.Toplevel(root)
    ventana.title(f"Resultado consolidado - {clave}")
    ventana.geometry("760x560")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(root)

    cabecera = tk.Frame(ventana, bg=COLOR_ERROR if hay_hallazgo else COLOR_EXITO)
    cabecera.pack(fill="x")
    tk.Label(cabecera,
             text="HALLAZGO DE AUDITORÍA" if hay_hallazgo else "SIN HALLAZGOS",
             font=("Arial", 16, "bold"), bg=cabecera["bg"], fg=COLOR_BLANCO).pack(pady=(14, 2))
    tk.Label(cabecera, text=f"{clave}. {ficha['titulo']}", font=("Arial", 10),
             bg=cabecera["bg"], fg=COLOR_BLANCO, wraplength=720).pack(pady=(0, 12))

    cuerpo = tk.Frame(ventana, bg=COLOR_FONDO)
    cuerpo.pack(fill="both", expand=True, padx=20, pady=14)

    resumen = (f"Proceso evaluado: {ficha['proceso']}\n"
               f"Registros analizados: {len(lista)}\n"
               f"Registros en NO CUMPLE: {len(no_cumple)}\n"
               f"Registros en CUMPLE: {len(lista) - len(no_cumple)}\n"
               f"Nivel de riesgo asociado: {ficha['riesgo']}")

    tk.Label(cuerpo, text=resumen, justify="left", anchor="w", font=("Arial", 10),
             bg=COLOR_BLANCO, padx=15, pady=12).pack(fill="x", pady=(0, 12))

    if hay_hallazgo:
        conclusion = (f"Se identificaron {len(no_cumple)} registros que incumplen el criterio "
                      f"de auditoría aplicado a esta vulnerabilidad. La situación requiere "
                      f"validación y tratamiento por parte del área responsable.")
    else:
        conclusion = ("Toda la evidencia cargada para está vulnerabilidad cumple el criterio "
                      "de auditoría aplicado. No se genera hallazgo.")

    tk.Label(cuerpo, text="CONCLUSIÓN PRELIMINAR", font=("Arial", 12, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=(10, 6))

    tk.Label(cuerpo, text=conclusion, wraplength=690, justify="left",
             font=("Arial", 10), bg=COLOR_FONDO).pack(fill="x", padx=10)

    if hay_hallazgo:
        marco = tk.Frame(cuerpo, bg=COLOR_BLANCO, padx=15, pady=12)
        marco.pack(fill="x", pady=12)
        for i_r, r in enumerate(no_cumple, start=1):
            tk.Label(marco, text=f"{i_r}. {r['detalle']}", font=("Arial", 9),
                     bg=COLOR_BLANCO, wraplength=680, justify="left",
                     anchor="w").pack(fill="x", pady=3)

    tk.Label(cuerpo,
             text=("IMPORTANTE: el resultado del sistema es apoyo a la auditoría y no "
                   "constituye por sí solo la calificación final del hallazgo."),
             wraplength=690, justify="left", font=("Arial", 8, "italic"),
             bg="#FFF3CD", fg="#856404", padx=12, pady=10).pack(fill="x", pady=(6, 0))

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg=COLOR_PRINCIPAL,
              fg=COLOR_BLANCO, font=("Arial", 10, "bold"), padx=20).pack(pady=(0, 14))


def eliminar_seleccion(clave, tabla):
    """Elimina el registro seleccionado y reconstruye la tabla."""
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Selección requerida", "Seleccione una fila para eliminar.")
        return

    if not messagebox.askyesno("Confirmar", "Desea eliminar el registro seleccionado?"):
        return

    indice = int(seleccion[0])
    registros[clave].pop(indice)
    reconstruir_tabla(clave, tabla)
    actualizar_resumen()


def reconstruir_tabla(clave, tabla):
    for item in tabla.get_children():
        tabla.delete(item)

    for i, r in enumerate(registros[clave]):
        if clave == "V1":
            valores = (r["fecha"], r["usuarios"], r["capacidad"], r["balanceo"], r["colas"], r["estado"])
        elif clave == "V2":
            valores = (r["usuario"], r["longitud"], r["mayus"], r["números"], r["símbolos"], r["caduca"], r["estado"])
        elif clave == "V3":
            valores = (r["usuario"], r["tipo"], r["estado_cuenta"], r["fecha_retiro"], r["estado"])
        elif clave == "V4":
            valores = (r["fecha_backup"], r["tipo"], r["prueba"], r["fecha_prueba"], r["estado"])
        else:
            valores = (r["componente"], r["versión"], r["soporte"], r["fecha_parche"], r["estado"])

        tabla.insert("", "end", iid=str(i), values=valores, tags=(r["estado"],))

    pintar_fila(tabla)


def limpiar_todo():
    if not messagebox.askyesno("Confirmar", "Se eliminarán todos los registros cargados. Continuar?"):
        return
    for clave, tabla in (("V1", tabla_v1), ("V2", tabla_v2), ("V3", tabla_v3),
                         ("V4", tabla_v4), ("V5", tabla_v5)):
        registros[clave].clear()
        reconstruir_tabla(clave, tabla)
    precargar_todo()
    actualizar_resumen()


# ==============================================================
# RESUMEN GENERAL Y COMPARACIÓN
# ==============================================================

def hay_no_cumple(clave):
    return any(r["estado"] == "NO CUMPLE" for r in registros[clave])


def actualizar_resumen():
    total_registros = sum(len(v) for v in registros.values())
    total_no_cumple = sum(1 for lista in registros.values()
                          for r in lista if r["estado"] == "NO CUMPLE")
    vulnerabilidades_detectadas = sum(1 for c in ORDEN if hay_no_cumple(c))

    label_total.config(text=f"Registros cargados: {total_registros}")
    label_hallazgos.config(text=f"Registros en NO CUMPLE: {total_no_cumple}")
    label_vulns.config(text=f"Vulnerabilidades detectadas por el sistema: {vulnerabilidades_detectadas} de 5")

    actualizar_resultados()


def actualizar_resultados():
    """Consolida en la pestaña de resultados el estado de cada vulnerabilidad."""
    for item in tabla_resultados.get_children():
        tabla_resultados.delete(item)

    detectadas = 0

    for clave in ORDEN:
        lista = registros[clave]
        total = len(lista)
        n_no_cumple = sum(1 for r in lista if r["estado"] == "NO CUMPLE")
        n_cumple = total - n_no_cumple

        if total == 0:
            resultado = "Sin evidencia cargada"
            tag = "neutro"
        elif n_no_cumple > 0:
            resultado = f"HALLAZGO DETECTADO (riesgo {FICHAS[clave]['riesgo']})"
            tag = "hallazgo"
            detectadas += 1
        else:
            resultado = "Sin hallazgos"
            tag = "ok"

        tabla_resultados.insert("", "end", values=(
            clave,
            FICHAS[clave]["titulo"],
            total,
            n_cumple,
            n_no_cumple,
            resultado,
        ), tags=(tag,))

    tabla_resultados.tag_configure("ok", background=FILA_CUMPLE)
    tabla_resultados.tag_configure("hallazgo", background=FILA_NO_CUMPLE)
    tabla_resultados.tag_configure("neutro", background=COLOR_BLANCO)

    label_vulns_hallazgo.config(
        text=f"Vulnerabilidades con hallazgo: {detectadas} de 5"
    )


# ==============================================================
# EXPORTACION DEL INFORME
# ==============================================================

def exportar_informe():
    total_registros = sum(len(v) for v in registros.values())
    if total_registros == 0:
        messagebox.showwarning("Sin información", "No hay registros cargados para exportar.")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt")],
        title="Guardar informe de auditoría - Caso Génesis"
    )
    if not archivo:
        return

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("=" * 66 + "\n")
        f.write("   INFORME DE AUDITORÍA DE SISTEMAS\n")
        f.write("   Sistema de Información Académica GÉNESIS - UDES\n")
        f.write("=" * 66 + "\n\n")
        f.write(f"Fecha de generación: {date.today().isoformat()}\n")
        f.write(f"Registros de evidencia analizados: {total_registros}\n\n")

        f.write("1. RESULTADO POR VULNERABILIDAD\n")
        f.write("-" * 66 + "\n\n")

        for clave in ORDEN:
            ficha = FICHAS[clave]
            f.write(f"{clave}. {ficha['titulo']}\n")
            f.write(f"   Proceso evaluado: {ficha['proceso']}\n")
            f.write(f"   Criterio: {ficha['criterio']}\n")

            if not registros[clave]:
                f.write("   Sin evidencia cargada.\n\n")
                continue

            no_cumple = [r for r in registros[clave] if r["estado"] == "NO CUMPLE"]
            f.write(f"   Registros analizados: {len(registros[clave])} "
                    f"(en NO CUMPLE: {len(no_cumple)})\n\n")

            for i, r in enumerate(registros[clave], start=1):
                f.write(f"   Registro {i} - {r['estado']}\n")
                for etiqueta, valor in descripcion_registro(clave, r):
                    f.write(f"      {etiqueta}: {valor}\n")
                f.write(f"      Condición detectada: {r['detalle']}\n")
                if r.get("nota"):
                    f.write(f"      Observación: {r['nota']}\n")
                f.write("\n")

            if no_cumple:
                f.write(f"   CONCLUSIÓN: se detectaron {len(no_cumple)} registros que "
                        f"incumplen el criterio (nivel de riesgo {ficha['riesgo']}).\n")
            else:
                f.write("   CONCLUSIÓN: sin hallazgos con la evidencia cargada.\n")
            f.write("\n")

        f.write("2. RESUMEN CONSOLIDADO\n")
        f.write("-" * 66 + "\n\n")

        detectadas = 0
        for clave in ORDEN:
            lista = registros[clave]
            n_no_cumple = sum(1 for r in lista if r["estado"] == "NO CUMPLE")

            if not lista:
                estado = "Sin evidencia cargada"
            elif n_no_cumple > 0:
                estado = (f"HALLAZGO DETECTADO - {n_no_cumple} de {len(lista)} registros "
                          f"en NO CUMPLE (riesgo {FICHAS[clave]['riesgo']})")
                detectadas += 1
            else:
                estado = f"Sin hallazgos - {len(lista)} registros conformes"

            f.write(f"{clave} - {FICHAS[clave]['titulo']}\n")
            f.write(f"   {estado}\n\n")

        f.write(f"Vulnerabilidades con hallazgo: {detectadas} de 5.\n\n")

        f.write("3. NOTA\n")
        f.write("-" * 66 + "\n")
        f.write("Este informe es el resultado del análisis automatizado sobre la evidencia "
                "cargada. La calificación final de cada hallazgo corresponde al juicio "
                "profesional del auditor y debe soportarse en evidencia verificable.\n")

    messagebox.showinfo("Informe generado",
                        "El informe de auditoría fue exportado correctamente.")


# ==============================================================
# CONSTRUCCION DE LA VENTANA PRINCIPAL
# ==============================================================

root = tk.Tk()
root.title("Sistema de Auditoría - Caso Génesis (UDES)")
root.geometry("1200x760")
root.minsize(1050, 660)
root.configure(bg=COLOR_FONDO)

# ---------- Encabezado ----------

encabezado = tk.Frame(root, bg=COLOR_PRINCIPAL)
encabezado.pack(fill="x")

tk.Label(encabezado, text="AUDITORÍA DE SISTEMAS - SISTEMA GÉNESIS (UDES)",
         font=("Arial", 18, "bold"), bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=(14, 0))

tk.Label(encabezado,
         text="Evaluación automatizada de las 5 vulnerabilidades del caso (V1 a V5)",
         font=("Arial", 10), bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=(0, 14))

# ---------- Pestanas ----------

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)

tab_v1 = tk.Frame(notebook, bg=COLOR_FONDO)
tab_v2 = tk.Frame(notebook, bg=COLOR_FONDO)
tab_v3 = tk.Frame(notebook, bg=COLOR_FONDO)
tab_v4 = tk.Frame(notebook, bg=COLOR_FONDO)
tab_v5 = tk.Frame(notebook, bg=COLOR_FONDO)
tab_resumen = tk.Frame(notebook, bg=COLOR_FONDO)

notebook.add(tab_v1, text=" V1 - Capacidad ")
notebook.add(tab_v2, text=" V2 - Contraseñas ")
notebook.add(tab_v3, text=" V3 - Cuentas ")
notebook.add(tab_v4, text=" V4 - Backups ")
notebook.add(tab_v5, text=" V5 - Software ")
notebook.add(tab_resumen, text=" Resultados de la auditoría ")


def barra_acciones(tab, clave, tabla, comando_agregar):
    """Crea la barra con los botones Agregar / Auditar selección / Eliminar / Siguiente."""
    barra = tk.Frame(tab, bg=COLOR_FONDO)
    barra.pack(fill="x", padx=15, pady=(0, 6))

    tk.Button(barra, text="Agregar registro", command=comando_agregar,
              bg=COLOR_SECUNDARIO, fg=COLOR_BLANCO, font=("Arial", 10, "bold"),
              padx=14, pady=4).pack(side="left", padx=(0, 8))

    tk.Button(barra, text="Auditar selección",
              command=lambda: auditar_seleccion(clave, tabla),
              bg=COLOR_EXITO, fg=COLOR_BLANCO, font=("Arial", 10, "bold"),
              padx=14, pady=4).pack(side="left", padx=8)

    tk.Button(barra, text="Siguiente ejemplo del caso",
              command=lambda: siguiente_ejemplo(clave),
              bg=COLOR_ALERTA, fg=COLOR_BLANCO, font=("Arial", 9, "bold"),
              padx=10, pady=4).pack(side="left", padx=8)

    tk.Button(barra, text="Eliminar selección",
              command=lambda: eliminar_seleccion(clave, tabla),
              bg=COLOR_ERROR, fg=COLOR_BLANCO, font=("Arial", 9, "bold"),
              padx=10, pady=4).pack(side="left", padx=8)

    tk.Label(barra, text="Doble clic sobre una fila = auditar",
             bg=COLOR_FONDO, fg="#666666", font=("Arial", 8, "italic")).pack(side="right")

    tabla.bind("<Double-1>", lambda e: auditar_seleccion(clave, tabla))


# ==============================================================
# PESTAÑA V1 - CAPACIDAD
# ==============================================================

frm = tk.LabelFrame(tab_v1, text=" Registrar medición de capacidad (campos precargados con el caso) ",
                    bg=COLOR_FONDO, fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=10, pady=10)
frm.pack(fill="x", padx=15, pady=10)

tk.Label(frm, text="Fecha (AAAA-MM-DD):", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entry_v1_fecha = ttk.Entry(frm, width=14); entry_v1_fecha.grid(row=0, column=1, padx=5)

tk.Label(frm, text="Usuarios conectados:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=5)
entry_v1_usuarios = ttk.Entry(frm, width=10); entry_v1_usuarios.grid(row=0, column=3, padx=5)

tk.Label(frm, text="Capacidad máxima servidor:", bg=COLOR_FONDO).grid(row=0, column=4, sticky="w", padx=5)
entry_v1_capacidad = ttk.Entry(frm, width=10); entry_v1_capacidad.grid(row=0, column=5, padx=5)

label_v1_pos = tk.Label(frm, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=("Arial", 8, "bold"))
label_v1_pos.grid(row=0, column=6, padx=10)

tk.Label(frm, text="Balanceo de carga:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=5, pady=6)
combo_v1_balanceo = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v1_balanceo.grid(row=1, column=1, padx=5)

tk.Label(frm, text="Sistema de colas:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=5)
combo_v1_colas = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v1_colas.grid(row=1, column=3, padx=5)

tk.Label(frm, text="Observación:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=5, pady=6)
entry_v1_nota = ttk.Entry(frm, width=70); entry_v1_nota.grid(row=2, column=1, columnspan=5, sticky="w", padx=5)

tabla_v1 = ttk.Treeview(tab_v1, columns=("fecha", "usuarios", "capacidad", "balanceo", "colas", "estado"),
                        show="headings", height=11)
for col, txt, w in [("fecha", "Fecha", 110), ("usuarios", "Usuarios", 90),
                    ("capacidad", "Capacidad max.", 110), ("balanceo", "Balanceo", 90),
                    ("colas", "Colas", 80), ("estado", "Resultado", 120)]:
    tabla_v1.heading(col, text=txt); tabla_v1.column(col, width=w, anchor="center")

barra_acciones(tab_v1, "V1", tabla_v1, agregar_capacidad)
tabla_v1.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# ==============================================================
# PESTAÑA V2 - CONTRASENAS
# ==============================================================

frm = tk.LabelFrame(tab_v2, text=" Registrar política de contraseña observada (campos precargados) ",
                    bg=COLOR_FONDO, fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=10, pady=10)
frm.pack(fill="x", padx=15, pady=10)

tk.Label(frm, text="Usuario / perfil:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entry_v2_usuario = ttk.Entry(frm, width=28); entry_v2_usuario.grid(row=0, column=1, padx=5)

tk.Label(frm, text="Longitud mínima:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=5)
entry_v2_longitud = ttk.Entry(frm, width=8); entry_v2_longitud.grid(row=0, column=3, padx=5)

tk.Label(frm, text="Días desde último cambio:", bg=COLOR_FONDO).grid(row=0, column=4, sticky="w", padx=5)
entry_v2_dias = ttk.Entry(frm, width=8); entry_v2_dias.grid(row=0, column=5, padx=5)

label_v2_pos = tk.Label(frm, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=("Arial", 8, "bold"))
label_v2_pos.grid(row=0, column=6, padx=10)

tk.Label(frm, text="Exige mayúsculas:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=5, pady=6)
combo_v2_mayus = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v2_mayus.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frm, text="Exige números:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=5)
combo_v2_numeros = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v2_numeros.grid(row=1, column=3, padx=5)

tk.Label(frm, text="Exige símbolos:", bg=COLOR_FONDO).grid(row=1, column=4, sticky="w", padx=5)
combo_v2_simbolos = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v2_simbolos.grid(row=1, column=5, padx=5)

tk.Label(frm, text="Caduca periódicamente:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=5, pady=6)
combo_v2_caduca = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v2_caduca.grid(row=2, column=1, padx=5, sticky="w")

tk.Label(frm, text="Observación:", bg=COLOR_FONDO).grid(row=3, column=0, sticky="w", padx=5, pady=6)
entry_v2_nota = ttk.Entry(frm, width=70); entry_v2_nota.grid(row=3, column=1, columnspan=5, sticky="w", padx=5)

tabla_v2 = ttk.Treeview(tab_v2, columns=("usuario", "longitud", "mayus", "números", "símbolos", "caduca", "estado"),
                        show="headings", height=11)
for col, txt, w in [("usuario", "Usuario / perfil", 230), ("longitud", "Longitud", 80),
                    ("mayus", "Mayusc.", 80), ("números", "Números", 80),
                    ("símbolos", "Símbolos", 80), ("caduca", "Caduca", 80), ("estado", "Resultado", 120)]:
    tabla_v2.heading(col, text=txt); tabla_v2.column(col, width=w, anchor="center")

barra_acciones(tab_v2, "V2", tabla_v2, agregar_password)
tabla_v2.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# ==============================================================
# PESTAÑA V3 - CUENTAS
# ==============================================================

frm = tk.LabelFrame(tab_v3, text=" Registrar cuenta de usuario (campos precargados) ",
                    bg=COLOR_FONDO, fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=10, pady=10)
frm.pack(fill="x", padx=15, pady=10)

tk.Label(frm, text="Usuario / identificador:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entry_v3_usuario = ttk.Entry(frm, width=30); entry_v3_usuario.grid(row=0, column=1, padx=5)

tk.Label(frm, text="Tipo de vínculo:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=5)
combo_v3_tipo = ttk.Combobox(frm, values=["Estudiante activo", "Estudiante egresado", "Docente",
                                          "Exdocente", "Administrativo", "Exfuncionario"],
                             state="readonly", width=20)
combo_v3_tipo.grid(row=0, column=3, padx=5)

label_v3_pos = tk.Label(frm, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=("Arial", 8, "bold"))
label_v3_pos.grid(row=0, column=4, padx=10)

tk.Label(frm, text="Estado de la cuenta:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=5, pady=6)
combo_v3_estado = ttk.Combobox(frm, values=["Activa", "Inactiva"], state="readonly", width=12)
combo_v3_estado.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frm, text="Fecha de retiro (si aplica):", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=5)
entry_v3_fecha_retiro = ttk.Entry(frm, width=14); entry_v3_fecha_retiro.grid(row=1, column=3, padx=5, sticky="w")

tk.Label(frm, text="Observación:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=5, pady=6)
entry_v3_nota = ttk.Entry(frm, width=70); entry_v3_nota.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

tabla_v3 = ttk.Treeview(tab_v3, columns=("usuario", "tipo", "estado_cuenta", "fecha_retiro", "estado"),
                        show="headings", height=11)
for col, txt, w in [("usuario", "Usuario", 250), ("tipo", "Tipo de vínculo", 170),
                    ("estado_cuenta", "Estado cuenta", 110), ("fecha_retiro", "Fecha retiro", 120),
                    ("estado", "Resultado", 120)]:
    tabla_v3.heading(col, text=txt); tabla_v3.column(col, width=w, anchor="center")

barra_acciones(tab_v3, "V3", tabla_v3, agregar_cuenta)
tabla_v3.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# ==============================================================
# PESTAÑA V4 - BACKUPS
# ==============================================================

frm = tk.LabelFrame(tab_v4, text=" Registrar copia de seguridad (campos precargados) ",
                    bg=COLOR_FONDO, fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=10, pady=10)
frm.pack(fill="x", padx=15, pady=10)

tk.Label(frm, text="Fecha del backup (AAAA-MM-DD):", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entry_v4_fecha = ttk.Entry(frm, width=14); entry_v4_fecha.grid(row=0, column=1, padx=5)

tk.Label(frm, text="Tipo de copia:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=5)
combo_v4_tipo = ttk.Combobox(frm, values=["Completo", "Incremental"], state="readonly", width=14)
combo_v4_tipo.grid(row=0, column=3, padx=5)

label_v4_pos = tk.Label(frm, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=("Arial", 8, "bold"))
label_v4_pos.grid(row=0, column=4, padx=10)

tk.Label(frm, text="Prueba de restauración realizada:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=5, pady=6)
combo_v4_prueba = ttk.Combobox(frm, values=["Sí", "No"], state="readonly", width=8)
combo_v4_prueba.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frm, text="Fecha de la última prueba:", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=5)
entry_v4_fecha_prueba = ttk.Entry(frm, width=14); entry_v4_fecha_prueba.grid(row=1, column=3, padx=5, sticky="w")

tk.Label(frm, text="Observación:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=5, pady=6)
entry_v4_nota = ttk.Entry(frm, width=70); entry_v4_nota.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

tabla_v4 = ttk.Treeview(tab_v4, columns=("fecha_backup", "tipo", "prueba", "fecha_prueba", "estado"),
                        show="headings", height=11)
for col, txt, w in [("fecha_backup", "Fecha backup", 130), ("tipo", "Tipo", 120),
                    ("prueba", "Prueba restauración", 150), ("fecha_prueba", "Fecha prueba", 130),
                    ("estado", "Resultado", 120)]:
    tabla_v4.heading(col, text=txt); tabla_v4.column(col, width=w, anchor="center")

barra_acciones(tab_v4, "V4", tabla_v4, agregar_backup)
tabla_v4.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# ==============================================================
# PESTAÑA V5 - SOFTWARE E INFRAESTRUCTURA
# ==============================================================

frm = tk.LabelFrame(tab_v5, text=" Registrar componente de software / infraestructura (campos precargados) ",
                    bg=COLOR_FONDO, fg=COLOR_PRINCIPAL, font=("Arial", 10, "bold"), padx=10, pady=10)
frm.pack(fill="x", padx=15, pady=10)

tk.Label(frm, text="Componente:", bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entry_v5_componente = ttk.Entry(frm, width=32); entry_v5_componente.grid(row=0, column=1, padx=5)

tk.Label(frm, text="Versión:", bg=COLOR_FONDO).grid(row=0, column=2, sticky="w", padx=5)
entry_v5_version = ttk.Entry(frm, width=26); entry_v5_version.grid(row=0, column=3, padx=5)

label_v5_pos = tk.Label(frm, text="", bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, font=("Arial", 8, "bold"))
label_v5_pos.grid(row=0, column=4, padx=10)

tk.Label(frm, text="Soporte del fabricante:", bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=5, pady=6)
combo_v5_soporte = ttk.Combobox(frm, values=["Vigente", "Vencido"], state="readonly", width=12)
combo_v5_soporte.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frm, text="Fecha último parche (AAAA-MM-DD):", bg=COLOR_FONDO).grid(row=1, column=2, sticky="w", padx=5)
entry_v5_fecha_parche = ttk.Entry(frm, width=14); entry_v5_fecha_parche.grid(row=1, column=3, padx=5, sticky="w")

tk.Label(frm, text="Observación:", bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=5, pady=6)
entry_v5_nota = ttk.Entry(frm, width=70); entry_v5_nota.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

tabla_v5 = ttk.Treeview(tab_v5, columns=("componente", "versión", "soporte", "fecha_parche", "estado"),
                        show="headings", height=11)
for col, txt, w in [("componente", "Componente", 250), ("versión", "Versión", 210),
                    ("soporte", "Soporte", 100), ("fecha_parche", "Último parche", 130),
                    ("estado", "Resultado", 120)]:
    tabla_v5.heading(col, text=txt); tabla_v5.column(col, width=w, anchor="center")

barra_acciones(tab_v5, "V5", tabla_v5, agregar_software_infra)
tabla_v5.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# ==============================================================
# PESTAÑA RESULTADOS DE LA AUDITORÍA
# ==============================================================

tk.Label(tab_resumen, text="Resultados de la auditoría por vulnerabilidad",
         font=("Arial", 13, "bold"), bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=(18, 4))

tk.Label(tab_resumen,
         text=("La tabla se actualiza automáticamente con la evidencia cargada en las pestañas "
               "V1 a V5. Una vulnerabilidad se marca como hallazgo cuando al menos un registro "
               "quedó en estado NO CUMPLE."),
         wraplength=980, justify="left", font=("Arial", 9), bg=COLOR_FONDO, fg="#444444").pack(padx=25, pady=(0, 10))

tabla_resultados = ttk.Treeview(tab_resumen,
                                 columns=("clave", "titulo", "total", "cumple", "no_cumple", "resultado"),
                                 show="headings", height=8)
for col, txt, w in [("clave", "V#", 50), ("titulo", "Vulnerabilidad", 330),
                    ("total", "Registros", 90), ("cumple", "Cumple", 80),
                    ("no_cumple", "No cumple", 90), ("resultado", "Resultado", 300)]:
    tabla_resultados.heading(col, text=txt); tabla_resultados.column(col, width=w, anchor="center")
tabla_resultados.column("titulo", anchor="w")
tabla_resultados.column("resultado", anchor="w")
tabla_resultados.pack(fill="x", padx=25, pady=10)

label_vulns_hallazgo = tk.Label(tab_resumen, text="Vulnerabilidades con hallazgo: 0 de 5",
                               font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_SECUNDARIO)
label_vulns_hallazgo.pack(pady=6)

tk.Label(tab_resumen,
         text="Seleccione una fila y use 'Ver detalle del hallazgo' para ver el análisis completo.",
         font=("Arial", 9, "italic"), bg=COLOR_FONDO, fg="#666666").pack()

panel_botones_resumen = tk.Frame(tab_resumen, bg=COLOR_FONDO)
panel_botones_resumen.pack(pady=14)

tk.Button(panel_botones_resumen, text="Ver detalle del hallazgo",
          command=lambda: ver_detalle_vulnerabilidad(), bg=COLOR_EXITO, fg=COLOR_BLANCO,
          font=("Arial", 10, "bold"), padx=14, pady=5).pack(side="left", padx=8)

tk.Button(panel_botones_resumen, text="Cargar toda la evidencia del caso",
          command=cargar_todos_los_ejemplos, bg=COLOR_ALERTA, fg=COLOR_BLANCO,
          font=("Arial", 10, "bold"), padx=14, pady=5).pack(side="left", padx=8)

tk.Button(panel_botones_resumen, text="Exportar informe de auditoría",
          command=exportar_informe, bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO,
          font=("Arial", 10, "bold"), padx=14, pady=5).pack(side="left", padx=8)

tk.Button(panel_botones_resumen, text="Limpiar registros",
          command=lambda: limpiar_todo(), bg=COLOR_ERROR, fg=COLOR_BLANCO,
          font=("Arial", 10, "bold"), padx=14, pady=5).pack(side="left", padx=8)


# ==============================================================
# PIE DE PAGINA
# ==============================================================

panel_resumen = tk.Frame(root, bg=COLOR_PRINCIPAL)
panel_resumen.pack(fill="x", padx=15, pady=(0, 12))

label_total = tk.Label(panel_resumen, text="Registros cargados: 0", bg=COLOR_PRINCIPAL,
                       fg=COLOR_BLANCO, font=("Arial", 10, "bold"))
label_total.pack(side="left", padx=20, pady=10)

label_hallazgos = tk.Label(panel_resumen, text="Registros en NO CUMPLE: 0", bg=COLOR_PRINCIPAL,
                           fg=COLOR_BLANCO, font=("Arial", 10, "bold"))
label_hallazgos.pack(side="left", padx=20)

label_vulns = tk.Label(panel_resumen, text="Vulnerabilidades detectadas por el sistema: 0 de 5",
                       bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO, font=("Arial", 10, "bold"))
label_vulns.pack(side="left", padx=20)


# ==============================================================
# ESTADO INICIAL
# ==============================================================

precargar_todo()
actualizar_resumen()


# ==============================================================
# INICIAR APLICACIÓN
# ==============================================================

if __name__ == "__main__":
    root.mainloop()
