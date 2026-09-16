# --------------------------------------------------------------
# IMPORTACIÓN DE LIBRERÍAS
# --------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# --------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------------------

COLOR_PRINCIPAL = "#173F5F"
COLOR_SECUNDARIO = "#20639B"
COLOR_EXITO = "#2A9D8F"
COLOR_ALERTA = "#F4A261"
COLOR_ERROR = "#E76F51"
COLOR_FONDO = "#F4F7FA"
COLOR_BLANCO = "#FFFFFF"


# --------------------------------------------------------------
# LISTA DONDE SE ALMACENARÁ LA INFORMACIÓN
# --------------------------------------------------------------

registros = []


# ==============================================================
# FUNCIÓN: AGREGAR SOFTWARE
# ==============================================================

def agregar_software():

    # ----------------------------------------------------------
    # OBTENER INFORMACIÓN DE LOS CAMPOS
    # ----------------------------------------------------------

    nombre = entry_software.get().strip()
    # Obtiene el nombre del software escrito en el Entry.

    licencia = entry_licencias.get().strip()
    # Obtiene la cantidad de licencias registradas.

    instalaciones = entry_instalaciones.get().strip()
    # Obtiene la cantidad de instalaciones encontradas.

    tipo = combo_tipo.get()
    # Obtiene el tipo de licencia seleccionado.

    evidencia = variable_evidencia.get()
    # Obtiene el estado del Checkbutton.


    # ----------------------------------------------------------
    # VALIDACIÓN DEL NOMBRE
    # ----------------------------------------------------------

    if nombre == "":
        messagebox.showwarning(
            "Información requerida",
            "Debe ingresar el nombre del software."
        )
        return


    # ----------------------------------------------------------
    # VALIDACIÓN DEL TIPO DE LICENCIA
    # ----------------------------------------------------------

    if tipo == "":
        messagebox.showwarning(
            "Información requerida",
            "Debe seleccionar el tipo de licencia."
        )
        return


    # ----------------------------------------------------------
    # VALIDACIÓN NUMÉRICA
    # ----------------------------------------------------------

    try:

        licencia = int(licencia)
        instalaciones = int(instalaciones)

    except ValueError:

        messagebox.showerror(
            "Dato inválido",
            "Las licencias e instalaciones deben ser números enteros."
        )

        return


    # ----------------------------------------------------------
    # VALIDAR QUE LOS NÚMEROS NO SEAN NEGATIVOS
    # ----------------------------------------------------------

    if licencia < 0 or instalaciones < 0:

        messagebox.showerror(
            "Dato inválido",
            "Las cantidades no pueden ser negativas."
        )

        return


    # ----------------------------------------------------------
    # CALCULAR DIFERENCIA
    # ----------------------------------------------------------

    diferencia = instalaciones - licencia
    # Si es positiva, existen más instalaciones que licencias.


    # ----------------------------------------------------------
    # DETERMINAR ESTADO
    # ----------------------------------------------------------

    if diferencia > 0:

        estado = "REQUIERE REVISIÓN"

    else:

        estado = "SIN DIFERENCIA"


    # ----------------------------------------------------------
    # CREAR REGISTRO
    # ----------------------------------------------------------

    registro = {

        "software": nombre,

        "licencias": licencia,

        "instalaciones": instalaciones,

        "diferencia": diferencia,

        "tipo": tipo,

        "evidencia": evidencia,

        "estado": estado
    }


    # ----------------------------------------------------------
    # GUARDAR REGISTRO
    # ----------------------------------------------------------

    registros.append(registro)


    # ----------------------------------------------------------
    # MOSTRAR EN LA TABLA
    # ----------------------------------------------------------

    tabla.insert(
        "",
        "end",
        values=(
            nombre,
            licencia,
            instalaciones,
            diferencia,
            tipo,
            evidencia,
            estado
        )
    )


    # ----------------------------------------------------------
    # ACTUALIZAR RESUMEN
    # ----------------------------------------------------------

    actualizar_resumen()


    # ----------------------------------------------------------
    # LIMPIAR FORMULARIO
    # ----------------------------------------------------------

    limpiar_formulario()


# ==============================================================
# FUNCIÓN: LIMPIAR FORMULARIO
# ==============================================================

def limpiar_formulario():

    entry_software.delete(0, tk.END)

    entry_licencias.delete(0, tk.END)

    entry_instalaciones.delete(0, tk.END)

    combo_tipo.set("")

    variable_evidencia.set("No")


# ==============================================================
# FUNCIÓN: ELIMINAR REGISTRO
# ==============================================================

def eliminar_registro():

    seleccion = tabla.selection()

    if not seleccion:

        messagebox.showwarning(
            "Selección requerida",
            "Seleccione un registro de la tabla."
        )

        return


    # Obtener índice seleccionado

    item = seleccion[0]

    valores = tabla.item(item, "values")

    nombre = valores[0]


    # Confirmar eliminación

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Desea eliminar el registro de {nombre}?"
    )


    if not confirmar:

        return


    # Eliminar de la tabla

    tabla.delete(item)


    # Buscar y eliminar del listado interno

    for registro in registros:

        if registro["software"] == nombre:

            registros.remove(registro)

            break


    actualizar_resumen()


# ==============================================================
# FUNCIÓN: ACTUALIZAR RESUMEN
# ==============================================================

def actualizar_resumen():

    total = len(registros)

    requieren = 0

    sin_diferencia = 0


    for registro in registros:

        if registro["diferencia"] > 0:

            requieren += 1

        else:

            sin_diferencia += 1


    label_total.config(
        text=f"Software auditado: {total}"
    )

    label_revision.config(
        text=f"Requieren revisión: {requieren}"
    )

    label_cumplen.config(
        text=f"Sin diferencia: {sin_diferencia}"
    )


# ==============================================================
# FUNCIÓN: AUDITAR SELECCIÓN
# ==============================================================

def auditar_seleccion():

    seleccion = tabla.selection()


    if not seleccion:

        messagebox.showwarning(
            "Selección requerida",
            "Seleccione un software para generar el análisis."
        )

        return


    item = seleccion[0]

    valores = tabla.item(item, "values")


    software = valores[0]

    licencias = int(valores[1])

    instalaciones = int(valores[2])

    diferencia = int(valores[3])

    tipo = valores[4]

    evidencia = valores[5]

    estado = valores[6]


    # ----------------------------------------------------------
    # CREAR VENTANA DE RESULTADO
    # ----------------------------------------------------------

    ventana = tk.Toplevel(root)

    ventana.title(
        f"Detalle de auditoría - {software}"
    )

    ventana.geometry("650x520")

    ventana.configure(
        bg=COLOR_FONDO
    )


    # ----------------------------------------------------------
    # TÍTULO
    # ----------------------------------------------------------

    tk.Label(
        ventana,
        text="ANÁLISIS DE AUDITORÍA",
        font=("Arial", 18, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    ).pack(
        pady=20
    )


    # ----------------------------------------------------------
    # INFORMACIÓN
    # ----------------------------------------------------------

    marco = tk.Frame(
        ventana,
        bg=COLOR_BLANCO,
        padx=20,
        pady=20
    )

    marco.pack(
        padx=30,
        fill="both"
    )


    datos = [

        ("Software", software),

        ("Tipo de licencia", tipo),

        ("Licencias registradas", licencias),

        ("Instalaciones encontradas", instalaciones),

        ("Diferencia", diferencia),

        ("Evidencia documental", evidencia),

        ("Estado", estado)
    ]


    for etiqueta, valor in datos:

        fila = tk.Frame(
            marco,
            bg=COLOR_BLANCO
        )

        fila.pack(
            fill="x",
            pady=5
        )


        tk.Label(
            fila,
            text=etiqueta + ":",
            font=("Arial", 10, "bold"),
            width=25,
            anchor="w",
            bg=COLOR_BLANCO
        ).pack(
            side="left"
        )


        tk.Label(
            fila,
            text=str(valor),
            font=("Arial", 10),
            anchor="w",
            bg=COLOR_BLANCO
        ).pack(
            side="left"
        )


    # ----------------------------------------------------------
    # CONCLUSIÓN
    # ----------------------------------------------------------

    if diferencia > 0:

        conclusion = (
            "Se identificó una diferencia entre las instalaciones "
            "encontradas y las licencias registradas. Esta situación "
            "requiere validación documental y contractual."
        )

    else:

        conclusion = (
            "No se identificó una diferencia positiva entre "
            "las instalaciones y las licencias registradas."
        )


    tk.Label(
        ventana,
        text="CONCLUSIÓN PRELIMINAR",
        font=("Arial", 12, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    ).pack(
        pady=(20, 5)
    )


    tk.Label(
        ventana,
        text=conclusion,
        wraplength=560,
        justify="left",
        font=("Arial", 10),
        bg=COLOR_FONDO
    ).pack(
        padx=40
    )


    # ----------------------------------------------------------
    # ADVERTENCIA DE AUDITORÍA
    # ----------------------------------------------------------

    tk.Label(
        ventana,
        text=(
            "IMPORTANTE: el resultado del sistema no demuestra "
            "por sí solo un incumplimiento contractual. "
            "El auditor debe verificar criterios, contratos "
            "y evidencias."
        ),
        wraplength=560,
        justify="left",
        font=("Arial", 9, "italic"),
        bg="#FFF3CD",
        fg="#856404",
        padx=10,
        pady=10
    ).pack(
        padx=30,
        pady=20
    )


# ==============================================================
# FUNCIÓN: EXPORTAR INFORME
# ==============================================================

def exportar_informe():

    if len(registros) == 0:

        messagebox.showwarning(
            "Sin información",
            "No existen registros para exportar."
        )

        return


    archivo = filedialog.asksaveasfilename(

        defaultextension=".txt",

        filetypes=[
            ("Archivo de texto", "*.txt")
        ],

        title="Guardar informe de auditoría"
    )


    if not archivo:

        return


    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "====================================================\n"
        )

        f.write(
            "       INFORME DE AUDITORÍA DE SOFTWARE\n"
        )

        f.write(
            "       TECHNOVA SOLUTIONS S.A.S.\n"
        )

        f.write(
            "====================================================\n\n"
        )


        for registro in registros:

            f.write(
                f"Software: {registro['software']}\n"
            )

            f.write(
                f"Licencias: {registro['licencias']}\n"
            )

            f.write(
                f"Instalaciones: {registro['instalaciones']}\n"
            )

            f.write(
                f"Diferencia: {registro['diferencia']}\n"
            )

            f.write(
                f"Tipo de licencia: {registro['tipo']}\n"
            )

            f.write(
                f"Evidencia documental: {registro['evidencia']}\n"
            )

            f.write(
                f"Estado: {registro['estado']}\n"
            )

            f.write(
                "----------------------------------------------------\n"
            )


        f.write("\nCONCLUSIÓN:\n")

        f.write(
            "Los resultados identifican situaciones que requieren "
            "validación de auditoría. El programa no sustituye "
            "el análisis profesional del auditor.\n"
        )


    messagebox.showinfo(
        "Informe generado",
        "El informe fue exportado correctamente."
    )


# ==============================================================
# CREACIÓN DE LA VENTANA PRINCIPAL
# ==============================================================

root = tk.Tk()

root.title(
    "Sistema de Auditoría de Software - TechNova"
)

root.geometry(
    "1100x700"
)

root.minsize(
    950,
    600
)

root.configure(
    bg=COLOR_FONDO
)


# ==============================================================
# ENCABEZADO
# ==============================================================

encabezado = tk.Frame(
    root,
    bg=COLOR_PRINCIPAL,
    height=100
)

encabezado.pack(
    fill="x"
)


tk.Label(
    encabezado,
    text="AUDITORÍA DE SOFTWARE",
    font=("Arial", 22, "bold"),
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO
).pack(
    pady=(18, 2)
)


tk.Label(
    encabezado,
    text="Gestión y evaluación de licencias de software",
    font=("Arial", 11),
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO
).pack()


# ==============================================================
# PANEL DE FORMULARIO
# ==============================================================

panel_formulario = tk.LabelFrame(
    root,
    text=" Registro de software ",
    font=("Arial", 11, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_PRINCIPAL,
    padx=15,
    pady=10
)

panel_formulario.pack(
    fill="x",
    padx=20,
    pady=15
)


# --------------------------------------------------------------
# SOFTWARE
# --------------------------------------------------------------

tk.Label(
    panel_formulario,
    text="Software:",
    bg=COLOR_FONDO
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)


entry_software = ttk.Entry(
    panel_formulario,
    width=25
)

entry_software.grid(
    row=0,
    column=1,
    padx=5
)


# --------------------------------------------------------------
# LICENCIAS
# --------------------------------------------------------------

tk.Label(
    panel_formulario,
    text="Licencias:",
    bg=COLOR_FONDO
).grid(
    row=0,
    column=2,
    padx=5,
    sticky="w"
)


entry_licencias = ttk.Entry(
    panel_formulario,
    width=12
)

entry_licencias.grid(
    row=0,
    column=3,
    padx=5
)


# --------------------------------------------------------------
# INSTALACIONES
# --------------------------------------------------------------

tk.Label(
    panel_formulario,
    text="Instalaciones:",
    bg=COLOR_FONDO
).grid(
    row=0,
    column=4,
    padx=5,
    sticky="w"
)


entry_instalaciones = ttk.Entry(
    panel_formulario,
    width=12
)

entry_instalaciones.grid(
    row=0,
    column=5,
    padx=5
)


# --------------------------------------------------------------
# TIPO DE LICENCIA
# --------------------------------------------------------------

tk.Label(
    panel_formulario,
    text="Tipo:",
    bg=COLOR_FONDO
).grid(
    row=1,
    column=0,
    padx=5,
    pady=10,
    sticky="w"
)


combo_tipo = ttk.Combobox(
    panel_formulario,
    values=[
        "Perpetua",
        "Suscripción",
        "Por usuario",
        "Por dispositivo",
        "Open Source",
        "Por capacidad"
    ],
    state="readonly",
    width=22
)

combo_tipo.grid(
    row=1,
    column=1,
    padx=5
)


# --------------------------------------------------------------
# CHECKBUTTON
# --------------------------------------------------------------

variable_evidencia = tk.StringVar(
    value="No"
)


check_evidencia = tk.Checkbutton(
    panel_formulario,
    text="Existe evidencia documental",
    variable=variable_evidencia,
    onvalue="Sí",
    offvalue="No",
    bg=COLOR_FONDO
)

check_evidencia.grid(
    row=1,
    column=2,
    columnspan=2,
    padx=10
)


# --------------------------------------------------------------
# BOTÓN AGREGAR
# --------------------------------------------------------------

boton_agregar = tk.Button(
    panel_formulario,
    text="Agregar",
    command=agregar_software,
    bg=COLOR_SECUNDARIO,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5
)

boton_agregar.grid(
    row=1,
    column=5,
    padx=5
)


# ==============================================================
# TABLA DE RESULTADOS
# ==============================================================

panel_tabla = tk.Frame(
    root,
    bg=COLOR_FONDO
)

panel_tabla.pack(
    fill="both",
    expand=True,
    padx=20
)


columnas = (

    "software",
    "licencias",
    "instalaciones",
    "diferencia",
    "tipo",
    "evidencia",
    "estado"
)


tabla = ttk.Treeview(
    panel_tabla,
    columns=columnas,
    show="headings",
    height=12
)


tabla.heading(
    "software",
    text="Software"
)

tabla.heading(
    "licencias",
    text="Licencias"
)

tabla.heading(
    "instalaciones",
    text="Instalaciones"
)

tabla.heading(
    "diferencia",
    text="Diferencia"
)

tabla.heading(
    "tipo",
    text="Tipo de licencia"
)

tabla.heading(
    "evidencia",
    text="Evidencia"
)

tabla.heading(
    "estado",
    text="Estado"
)


tabla.column(
    "software",
    width=180
)

tabla.column(
    "licencias",
    width=80,
    anchor="center"
)

tabla.column(
    "instalaciones",
    width=100,
    anchor="center"
)

tabla.column(
    "diferencia",
    width=80,
    anchor="center"
)

tabla.column(
    "tipo",
    width=130
)

tabla.column(
    "evidencia",
    width=90,
    anchor="center"
)

tabla.column(
    "estado",
    width=170
)


tabla.pack(
    side="left",
    fill="both",
    expand=True
)


scroll = ttk.Scrollbar(
    panel_tabla,
    orient="vertical",
    command=tabla.yview
)

scroll.pack(
    side="right",
    fill="y"
)


tabla.configure(
    yscrollcommand=scroll.set
)


# ==============================================================
# BOTONES DE OPERACIÓN
# ==============================================================

panel_botones = tk.Frame(
    root,
    bg=COLOR_FONDO
)

panel_botones.pack(
    fill="x",
    padx=20,
    pady=10
)


tk.Button(
    panel_botones,
    text="Auditar selección",
    command=auditar_seleccion,
    bg=COLOR_EXITO,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold"),
    padx=15
).pack(
    side="left",
    padx=5
)


tk.Button(
    panel_botones,
    text="Eliminar",
    command=eliminar_registro,
    bg=COLOR_ERROR,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold"),
    padx=15
).pack(
    side="left",
    padx=5
)


tk.Button(
    panel_botones,
    text="Limpiar",
    command=limpiar_formulario,
    font=("Arial", 10, "bold"),
    padx=15
).pack(
    side="left",
    padx=5
)


tk.Button(
    panel_botones,
    text="Exportar informe",
    command=exportar_informe,
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold"),
    padx=15
).pack(
    side="right",
    padx=5
)


# ==============================================================
# PANEL DE RESUMEN
# ==============================================================

panel_resumen = tk.Frame(
    root,
    bg=COLOR_PRINCIPAL,
    height=50
)

panel_resumen.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)


label_total = tk.Label(
    panel_resumen,
    text="Software auditado: 0",
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold")
)

label_total.pack(
    side="left",
    padx=20,
    pady=12
)


label_revision = tk.Label(
    panel_resumen,
    text="Requieren revisión: 0",
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold")
)

label_revision.pack(
    side="left",
    padx=20
)


label_cumplen = tk.Label(
    panel_resumen,
    text="Sin diferencia: 0",
    bg=COLOR_PRINCIPAL,
    fg=COLOR_BLANCO,
    font=("Arial", 10, "bold")
)

label_cumplen.pack(
    side="left",
    padx=20
)


# ==============================================================
# DATOS INICIALES PARA LA DEMOSTRACIÓN
# ==============================================================

entry_software.insert(
    0,
    "Microsoft Office"
)

entry_licencias.insert(
    0,
    "70"
)

entry_instalaciones.insert(
    0,
    "76"
)

combo_tipo.set(
    "Suscripción"
)

variable_evidencia.set(
    "Sí"
)


# ==============================================================
# INICIAR APLICACIÓN
# ==============================================================

root.mainloop()