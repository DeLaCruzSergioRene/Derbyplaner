import flet as ft
import bcrypt
from database.db import BD

def vista_registro(pagina: ft.Page, al_exito):
    campo_nombre = ft.TextField(label="Nombre", width=300)
    campo_email = ft.TextField(label="Correo", width=300)
    campo_contraseña = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text("", color="red")
    
    def registrar(e):
        nombre = campo_nombre.value.strip()
        email = campo_email.value.strip()
        contraseña = campo_contraseña.value.strip()
        
        if not nombre or not email or not contraseña:
            mensaje.value = "Completa todos los campos"
            pagina.update()
            return
        
        try:
            bd = BD()
            hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()
            bd.ejecutar("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                      (nombre, email, hashed))
            bd.cerrar()
            mensaje.value = "✓ Registrado exitosamente"
            mensaje.color = "green"
            campo_nombre.value = ""
            campo_email.value = ""
            campo_contraseña.value = ""
            pagina.update()
        except Exception as ex:
            mensaje.value = f"✗ {str(ex)[:40]}"
            pagina.update()
    
    return ft.Container(
        content=ft.Column([
            ft.Text("REGISTRO", size=24, weight="bold"),
            campo_nombre,
            campo_email,
            campo_contraseña,
            ft.ElevatedButton("Registrarse", on_click=registrar, width=300),
            mensaje
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.Alignment(0, 0)
    )
