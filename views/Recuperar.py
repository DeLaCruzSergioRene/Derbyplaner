import flet as ft
import os
import secrets
from database.db import BD

try:
    import yagmail
except Exception:
    yagmail = None

def recuperar(page: ft.Page, volver):
    campo_email = ft.TextField(label="Correo", width=300)
    mensaje = ft.Text("")

    def enviar(e):
        email = campo_email.value.strip()
        if not email:
            mensaje.value = "Completa el correo"
            page.update()
            return

        bd = BD()
        usuario = bd.obtener_uno("SELECT * FROM usuarios WHERE email = %s", (email,))
        bd.cerrar()

        if not usuario:
            mensaje.value = "✗ Correo no encontrado"
            page.update()
            return

        token = secrets.token_urlsafe(8)
        subject = "Recuperación de contraseña - Derby Planer"
        body = f"Hola {usuario.get('nombre','')},\n\nHas solicitado recuperar tu contraseña. Las contraseñas están encriptadas; usa este código temporal para restablecer la contraseña en la app: {token}\n\nSi no solicitaste esto, ignora este correo."

        enviado = False
        if yagmail:
            user = os.getenv('EMAIL_USER')
            pwd = os.getenv('EMAIL_PASS')
            if user and pwd:
                try:
                    yag = yagmail.SMTP(user, pwd)
                    yag.send(to=email, subject=subject, contents=body)
                    mensaje.value = "✓ Correo enviado"
                    enviado = True
                except Exception as ex:
                    mensaje.value = f"✗ Error enviando correo: {str(ex)[:40]}"
            else:
                mensaje.value = "✗ Falta configurar EMAIL_USER/EMAIL_PASS"
        else:
            mensaje.value = "✗ yagmail no instalado; token mostrado en pantalla"

        page.update()

        # Mostrar token en diálogo para permitir recuperación mínima sin backend adicional
        dlg = ft.AlertDialog(
            title=ft.Text("Código de recuperación"),
            content=ft.Text(token),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(page.dialog, 'open', False), page.update()))]
        )
        page.dialog = dlg
        page.dialog.open = True
        page.update()

    return ft.Container(
        content=ft.Column([
            ft.Text("RECUPERAR CONTRASEÑA", size=24, weight="bold"),
            campo_email,
            ft.ElevatedButton("Enviar correo", on_click=enviar, width=300),
            mensaje,
            ft.TextButton("Volver", on_click=lambda e: (page.clean(), volver()))
        ], spacing=15, horizontal_alignment="center"),
        padding=30,
        alignment=ft.alignment.Alignment(0, 0)
    )