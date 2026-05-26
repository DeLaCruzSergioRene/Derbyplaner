import flet as ft
import bcrypt
from database.db import BD

def vista_sesion(page: ft.Page, al_exito):
    campo_email = ft.TextField(keyboard_type=ft.KeyboardType.EMAIL, label="Correo", width=300)
    campo_contraseña = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text("", color="red")
    
    def iniciar_sesion(e):
        email = campo_email.value.strip()
        contraseña = campo_contraseña.value.strip()
        
        if not email or not contraseña:
            mensaje.value = "Completa todos los campos"
            page.update()
            return
        
        try:
            bd = BD()
            usuario_bd = bd.obtener_uno("SELECT * FROM usuarios WHERE email = %s", (email,))
            bd.cerrar()
            
            if not usuario_bd:
                mensaje.value = "✗ Correo no encontrado"
                page.update()
                return
            
            if bcrypt.checkpw(contraseña.encode(), usuario_bd['password'].encode()):
                mensaje.value = f"✓ Bienvenido {usuario_bd['nombre']}"
                mensaje.color = "green"
                page.update()
                al_exito(usuario_bd)
            else:
                mensaje.value = "✗ Contraseña incorrecta"
                page.update()
        except Exception as ex:
            mensaje.value = f"✗ Error: {str(ex)[:40]}"
            page.update()
    
    return ft.Container(
        content=ft.Column([
            ft.Text("INICIAR SESIÓN", size=24, weight="bold"),
            campo_email,
            campo_contraseña,
            ft.Button("Entrar", on_click=iniciar_sesion, width=300),
            mensaje,
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.Alignment(0, 0)
    )
