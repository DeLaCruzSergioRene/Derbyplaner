import flet as ft
import os
import secrets
import bcrypt
from database.db import BD

try:
    import yagmail
except Exception:
    yagmail = None

def recuperar(page: ft.Page, volver):
    tokens = {}  # {email: token}
    
    def mostrar_formulario_email():
        campo_email = ft.TextField(label="Correo", width=300)
        mensaje = ft.Text("")

        def enviar(e):
            email = campo_email.value.strip()
            if not email:
                mensaje.value = "Completa el correo"
                page.update()
                return

            bd = BD()
            try:
                usuario = bd.obtener_uno("SELECT * FROM usuarios WHERE email = %s", (email,))
            finally:
                bd.cerrar()

            if not usuario:
                mensaje.value = "✗ Correo no encontrado"
                page.update()
                return

            token = secrets.token_urlsafe(8)
            tokens[email] = token
            
            subject = "Recuperación de contraseña - Derby Planer"
            body = f"Hola {usuario.get('nombre','')},\n\nHas solicitado recuperar tu contraseña. Código temporal: {token}\n\nSi no solicitaste esto, ignora este correo."

            if yagmail:
                user = os.getenv('EMAIL_USER')
                pwd = os.getenv('EMAIL_PASS')
                if user and pwd:
                    try:
                        yag = yagmail.SMTP(user, pwd)
                        yag.send(to=email, subject=subject, contents=body)
                        mensaje.value = "✓ Correo enviado"
                    except Exception as ex:
                        mensaje.value = f"✗ Error: {str(ex)[:30]}"
                else:
                    mensaje.value = "✗ Falta configurar EMAIL_USER/EMAIL_PASS"
            else:
                mensaje.value = "✗ yagmail no instalado"

            page.update()
            page.clean()
            mostrar_formulario_token(email)

        page.clean()
        page.add(ft.Container(
            content=ft.Column([
                ft.Text("RECUPERAR CONTRASEÑA", size=24, weight="bold"),
                campo_email,
                ft.Button("Enviar código", on_click=enviar, width=300),
                mensaje,
                ft.TextButton("Volver", on_click=lambda e: (page.clean(), volver()))
            ], spacing=15, horizontal_alignment="center"),
            padding=30, expand=True, alignment=ft.alignment.Alignment(0, 0)
        ))

    def mostrar_formulario_token(email):
        campo_token = ft.TextField(label="Código", width=300)
        campo_pass = ft.TextField(label="Nueva contraseña", password=True, width=300)
        mensaje = ft.Text("")

        def cambiar(e):
            if campo_token.value != tokens.get(email):
                mensaje.value = "✗ Código incorrecto"
                page.update()
                return
            
            if not campo_pass.value or len(campo_pass.value) < 6:
                mensaje.value = "✗ Mínimo 6 caracteres"
                page.update()
                return

            try:
                nueva_pass = bcrypt.hashpw(campo_pass.value.encode(), bcrypt.gensalt()).decode()
                bd = BD()
                bd.ejecutar("UPDATE usuarios SET password = %s WHERE email = %s", (nueva_pass, email))
                bd.cerrar()
                mensaje.value = "✓ Contraseña actualizada"
                page.update()
                page.clean()
                volver()
            except Exception as ex:
                mensaje.value = f"✗ Error: {str(ex)[:30]}"
                page.update()

        page.clean()
        page.add(ft.Container(
            content=ft.Column([
                ft.Text("Ingresa el código y nueva contraseña", size=16, weight="bold"),
                campo_token,
                campo_pass,
                ft.Button("Cambiar contraseña", on_click=cambiar, width=300),
                mensaje,
                ft.TextButton("Volver", on_click=lambda e: (page.clean(), mostrar_formulario_email()))
            ], spacing=15, horizontal_alignment="center"),
            padding=30, expand=True, alignment=ft.alignment.Alignment(0, 0)
        ))

    mostrar_formulario_email()