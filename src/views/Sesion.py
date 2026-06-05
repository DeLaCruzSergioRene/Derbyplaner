import flet as ft
import bcrypt
from database.db import BD
from controller.auth_controller import validar_datos_sesion

class boton4(ft.Button):
    def init(self):
        self.bgcolor = ft.Colors.WHITE
        self.color = ft.Colors.BLUE_ACCENT_100
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=3)
        )

def vista_sesion(page: ft.Page, al_exito):
    # Campos de entrada para iniciar sesión
    campo_email = ft.TextField(keyboard_type=ft.KeyboardType.EMAIL, label="Correo", width=300)
    campo_contraseña = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text("", color="red")
    
    # Valida los datos del usuario y llama al callback de éxito si todo está bien
    def iniciar_sesion(e):
        email = campo_email.value.strip()
        contraseña = campo_contraseña.value.strip()
        
        ok, msg = validar_datos_sesion(email, contraseña)
        if not ok:
            mensaje.value = f"✗ {msg}"
            page.update()
            return
        
        try:
            # Busca el usuario en la base de datos usando el email
            bd = BD()
            usuario_bd = bd.obtener_uno("SELECT * FROM usuarios WHERE email = %s", (email,))
            bd.cerrar()
            
            if not usuario_bd:
                mensaje.value = "✗ Correo no encontrado"
                page.update()
                return
            
            if bcrypt.checkpw(contraseña.encode(), usuario_bd['password'].encode()):
                page.update()
                al_exito(usuario_bd)
            else:
                mensaje.value = "✗ Contraseña incorrecta"
                page.update()
        except Exception as ex:
            mensaje.value = f"✗ Error: {str(ex)[:40]}"
            page.update()
    
    # Retorna la interfaz de inicio de sesión con botón y mensajes
    # Construye la vista final de inicio de sesión con todos los controles
    return ft.Container(
        content=ft.Column([
            ft.Text("INICIAR SESIÓN", size=24, weight="bold"),
            campo_email,
            campo_contraseña,
            boton4("Entrar", on_click=iniciar_sesion, width=300),
            mensaje,
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.Alignment(0, 0)
    )
