# Importamos tkinter para crear la interfaz gráfica.
import tkinter as tk

# Importamos messagebox para mostrar mensajes.
from tkinter import messagebox

# Definimos el usuario administrador.
USUARIO = "admin"

# Definimos deliberadamente una contraseña insegura para la práctica de auditoría.
CONTRASENA = "Admin123"

# Definimos un segundo usuario.
USUARIO2 = "vendedor"

# Definimos deliberadamente otra contraseña insegura.
CONTRASENA2 = "Venta2026"

# Creamos la ventana principal.
ventana = tk.Tk()

# Establecemos el título de la ventana.
ventana.title("Sistema de Ventas")

# Establecemos el tamaño de la ventana.
ventana.geometry("400x300")

# Creamos la etiqueta del usuario.
etiqueta_usuario = tk.Label(ventana, text="Usuario:")

# Ubicamos la etiqueta.
etiqueta_usuario.pack(pady=10)

# Creamos el campo para escribir el usuario.
entrada_usuario = tk.Entry(ventana)

# Ubicamos el campo.
entrada_usuario.pack()

# Creamos la etiqueta de contraseña.
etiqueta_contrasena = tk.Label(ventana, text="Contraseña:")

# Ubicamos la etiqueta.
etiqueta_contrasena.pack(pady=10)

# Creamos el campo para escribir la contraseña.
entrada_contrasena = tk.Entry(ventana, show="*")

# Ubicamos el campo de contraseña.
entrada_contrasena.pack()

# Definimos la función para iniciar sesión.
def iniciar_sesion():

    # Obtenemos el usuario ingresado.
    usuario = entrada_usuario.get()

    # Obtenemos la contraseña ingresada.
    contrasena = entrada_contrasena.get()

    # Comparamos el usuario y la contraseña del administrador.
    if usuario == USUARIO and contrasena == CONTRASENA:

        # Mostramos el mensaje de bienvenida.
        messagebox.showinfo("Acceso", "Bienvenido administrador.")

    # Comparamos el usuario y la contraseña del vendedor.
    elif usuario == USUARIO2 and contrasena == CONTRASENA2:

        # Mostramos el mensaje de bienvenida.
        messagebox.showinfo("Acceso", "Bienvenido vendedor.")

    # Ejecutamos esta opción cuando las credenciales son incorrectas.
    else:

        # Mostramos un mensaje de error.
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Creamos el botón para iniciar sesión.
boton = tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion)

# Ubicamos el botón.
boton.pack(pady=20)

# Iniciamos el ciclo principal de la aplicación.
ventana.mainloop()