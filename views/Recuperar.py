import flet as ft
import os
import secrets
import time
import bcrypt
from database.db import BD

try:
    import yagmail
except Exception:
    yagmail = None

# Recuperación de contraseña sencilla mediante email.
# Esta vista muestra primero el formulario de correo y luego el de token.

def recuperar(page: ft.Page, volver):
    tokens = {}  # {email: (token, timestamp)}
    token_vigencia = 10 * 60  # 10 minutos

    # Guarda un token temporal válido para un email específico
    def guardar_token(email, token):
        tokens[email] = (token, time.time())

    # Verifica si el token aún está vigente y coincide con el valor esperado
    def token_valido(email, valor):
        data = tokens.get(email)
        if not data:
            return False
        token, creado = data
        if time.time() - creado > token_vigencia:
            tokens.pop(email, None)
            return False
        return token == valor

    # Muestra el formulario inicial donde se ingresa el correo electrónico
    def mostrar_formulario_email():
        campo_email = ft.TextField(label="Correo", width=300)
        mensaje = ft.Text("")

        # Envía el código temporal al email si el usuario existe
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
            guardar_token(email, token)
            enviado = False
            subject = "Recuperación de contraseña - Derby Planer"
            body = f"Hola {usuario.get('nombre', '')},\n\nHas solicitado recuperar tu contraseña. Código temporal: {token}\n\nSi no solicitaste esto, ignora este correo."

            if yagmail:
                user = os.getenv('EMAIL_USER', '').strip()
                pwd = os.getenv('EMAIL_PASS', '').strip()
                if user and pwd:
                    try:
                        yag = yagmail.SMTP(user, pwd)
                        yag.send(to=email, subject=subject, contents=body)
                        mensaje.value = "✓ Correo enviado. Revisa tu email."
                        enviado = True
                    except Exception as ex:
                        mensaje.value = f"✗ Error al enviar correo: {ex}"
                        print(f"Error al enviar correo: {ex}")
                else:
                    mensaje.value = "✗ Falta EMAIL_USER/EMAIL_PASS en .env"
            else:
                mensaje.value = "✗ yagmail no instalado. Ejecuta pip install yagmail"

            page.update()
            if enviado:
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
            padding=30,
            expand=True,
            alignment=ft.alignment.Alignment(0, 0)
        ))

    # Muestra el formulario para ingresar el token y la nueva contraseña
    def mostrar_formulario_token(email):
        campo_token = ft.TextField(label="Código", width=300)
        campo_pass = ft.TextField(label="Nueva contraseña", password=True, width=300)
        mensaje = ft.Text("")

        # Cambia la contraseña si el token es válido y la nueva clave cumple requisitos
        def cambiar(e):
            if not token_valido(email, campo_token.value.strip()):
                mensaje.value = "✗ Código incorrecto o expirado"
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
                tokens.pop(email, None)
                mensaje.value = "✓ Contraseña actualizada"
                page.update()
                page.clean()
                volver()
            except Exception:
                mensaje.value = "✗ No se pudo actualizar la contraseña"
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
            padding=30,
            expand=True,
            alignment=ft.alignment.Alignment(0, 0)
        ))

    mostrar_formulario_email()
