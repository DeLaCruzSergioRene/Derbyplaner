import flet as ft
import bcrypt
from database.db import BD
from controller.auth_controller import validar_datos_registro

def vista_registro(page: ft.Page, al_exito):
    # Campos para crear un nuevo usuario
    campo_nombre = ft.TextField(label="Nombre", width=300)
    campo_email = ft.TextField(keyboard_type=ft.KeyboardType.EMAIL, label="Correo", width=300)
    campo_contraseña = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text("", color="red")
    
    # Procesa el formulario de registro y valida los datos ingresados
    def registrar(e):
        nombre = campo_nombre.value.strip()
        email = campo_email.value.strip()
        contraseña = campo_contraseña.value.strip()
        
        ok, msg = validar_datos_registro(nombre, email, contraseña)
        if not ok:
            mensaje.value = f"✗ {msg}"
            page.update()
            return
        # Si pasa la validación, se crea el usuario en la base de datos
        
        try:
            # Inserta el nuevo usuario en la base de datos con contraseña segura
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
            page.update()
        except Exception as ex:
            # Muestra cualquier error que ocurra durante el registro
            mensaje.value = f"✗ {str(ex)[:40]}"
            page.update()
    
    return ft.Container(
        content=ft.Column([
            ft.Text("REGISTRO", size=24, weight="bold"),
            campo_nombre,
            campo_email,
            campo_contraseña,
            ft.Button("Registrarse", on_click=registrar, width=300),
            mensaje
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.Alignment(0, 0)
    )
