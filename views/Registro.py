import flet as ft
import bcrypt
from database.db import BD

def vista_registro(pagina: ft.Page, al_exito):
    campo_usuario = ft.TextField(label="Usuario", width=300)
    campo_contraseña = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text("", color="red")
    
    def registrar(e):
        usuario = campo_usuario.value.strip()
        contraseña = campo_contraseña.value.strip()
        
        if not usuario or not contraseña:
            mensaje.value = "Completa todos los campos"
            pagina.update()
            return
        
        try:
            bd = BD()
            hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()
            bd.ejecutar("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", 
                      (usuario, hashed))
            bd.cerrar()
            mensaje.value = "✓ Registrado exitosamente"
            mensaje.color = "green"
            campo_usuario.value = ""
            campo_contraseña.value = ""
            pagina.update()
        except Exception as ex:
            mensaje.value = f"✗ {str(ex)[:40]}"
            pagina.update()
    
    return ft.Container(
        content=ft.Column([
            ft.Text("REGISTRO", size=24, weight="bold"),
            campo_usuario,
            campo_contraseña,
            ft.ElevatedButton("Registrarse", on_click=registrar, width=300),
            mensaje
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.center
    )
