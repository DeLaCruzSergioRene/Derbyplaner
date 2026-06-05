import flet as ft
from controller.recuperar_controller import enviar_codigo_recuperacion
from database.db_operations import actualizar_contraseña_usuario

def recuperar(page: ft.Page, al_iniciar_sesion):
    page.clean()
    
    email_input = ft.TextField(label="Email", width=300)
    codigo_input = ft.TextField(label="Código (se enviará al email)", width=300, visible=False)
    nueva_pass_input = ft.TextField(label="Nueva Contraseña", password=True, width=300, visible=False, can_reveal_password=True)
    confirmar_pass_input = ft.TextField(label="Confirmar Contraseña", password=True, width=300, visible=False, can_reveal_password=True)
    
    mensaje = ft.Text("", color="#B814CE", size=12)
    codigo_guardado = {"valor": None}
    
    async def enviar_codigo(e):
        if not email_input.value:
            mensaje.value = "Ingresa tu email"
            mensaje.color = "#B8141C"
            page.update()
            return
        
        # Mostrar indicador de carga
        mensaje.value = "Enviando código..."
        mensaje.color = "#744BB1"
        btn_enviar.disabled = True
        page.update()
        
        exito, msg, codigo = await enviar_codigo_recuperacion(email_input.value)
        
        if exito:
            codigo_guardado["valor"] = codigo
            mensaje.value = msg
            mensaje.color = "#4CAF50"
            
            # Mostrar campos de código y nueva contraseña
            codigo_input.visible = True
            nueva_pass_input.visible = True
            confirmar_pass_input.visible = True
            btn_enviar.visible = False
            btn_recuperar.visible = True
            
        else:
            mensaje.value = msg
            mensaje.color = "#B8141C"
            btn_enviar.disabled = False
        
        page.update()
    
    def recuperar_contraseña(e):
        if codigo_input.value.strip() != codigo_guardado["valor"]:
            mensaje.value = "Código incorrecto"
            mensaje.color = "#B8141C"
            page.update()
            return
        
        if nueva_pass_input.value != confirmar_pass_input.value:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "#B8141C"
            page.update()
            return
        
        if len(nueva_pass_input.value) < 8:
            mensaje.value = "La contraseña debe tener al menos 8 caracteres"
            mensaje.color = "#B8141C"
            page.update()
            return
        
        # Actualizar contraseña en BD
        actualizar_contraseña_usuario(email_input.value, nueva_pass_input.value)
        
        mensaje.value = "¡Contraseña recuperada! Volviendo a Iniciar Sesión..."
        mensaje.color = "#4CAF50"
        page.update()
        
        # Redirigir a login
        import time
        time.sleep(2)
        al_iniciar_sesion()
    
    btn_enviar = ft.Button("Enviar Código", on_click=lambda e: page.run_task(enviar_codigo, e), bgcolor="#E438AB", color="white", width=300)
    btn_recuperar = ft.Button("Recuperar Contraseña", on_click=recuperar_contraseña, bgcolor="#744BB1", color="white", width=300, visible=False)
    
    # Link para volver a sesión
    link_volver = ft.TextButton(
        "Volver a Iniciar Sesión",
        on_click=al_iniciar_sesion,
        style=ft.ButtonStyle(color="#744BB1")
    )
    
    contenido = ft.Column([
        ft.Text("Recuperar Contraseña", size=24, weight="bold", color="#744BB1", text_align="center"),
        ft.Divider(height=20, color="#E6C9F5"),
        
        email_input,
        ft.Text("Te enviaremos un código al email", size=12, color="#666"),
        btn_enviar,
        
        ft.Divider(height=20, color="#E6C9F5"),
        
        codigo_input,
        nueva_pass_input,
        confirmar_pass_input,
        btn_recuperar,
        
        ft.Divider(height=10, color="#E6C9F5"),
        mensaje,
        
        ft.Divider(height=20, color="#E6C9F5"),
        link_volver,
    ], spacing=15, horizontal_alignment="center", expand=True, alignment="center")
    
    page.add(ft.Container(content=contenido, padding=30, bgcolor="#FFFFFF", expand=True))
    page.update()
