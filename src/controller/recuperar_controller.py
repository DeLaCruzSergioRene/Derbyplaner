import yagmail
import random
import string
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

def generar_codigo():
    # Genera un código aleatorio de 6 dígitos
    return ''.join(random.choices(string.digits, k=6))

def _enviar_email_bloqueante(email: str, codigo: str) -> tuple:
    # Envío bloqueante (ejecutado en thread)
    try:
        usuario = os.getenv('EMAIL_USER')
        contraseña = os.getenv('EMAIL_PASS')
        
        if not usuario or not contraseña:
            return False, "Error: Credenciales de email no configuradas"
        
        # Conectar a Gmail
        yag = yagmail.SMTP(usuario, contraseña)
        
        # Enviar email
        asunto = "Recuperación de Contraseña - Derby Planer"
        contenido = f"""Hola, Tu código de recuperación es: {codigo} Este código es válido por 10 minutos. Si no solicitaste esto, ignora este mensaje. Saludos, Derby Planer"""
        
        yag.send(to=email, subject=asunto, contents=contenido)
        yag.close()
        
        return True, "Código enviado al correo"
    
    except Exception as e:
        return False, f"Error al enviar email: {str(e)}"

async def enviar_codigo_recuperacion(email: str) -> tuple:
    # Envía código de recuperación al email sin bloquear. Devuelve (éxito, mensaje, código)
    codigo = generar_codigo()
    
    # Ejecutar el envío en thread para no bloquear Flet
    exito, msg = await asyncio.to_thread(_enviar_email_bloqueante, email, codigo)
    
    if exito:
        return True, msg, codigo
    else:
        return False, msg, None
