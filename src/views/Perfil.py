import flet as ft

def perfil(page: ft.Page):
    # Obtiene los datos del usuario actual para mostrar en el perfil
    user = getattr(page, "current_user", {})
    nombre = user.get('nombre', 'Usuario')
    email = user.get('email', 'correo@ejemplo.com')
    
    # Muestra la pantalla de perfil con imágenes y datos del usuario
    # Usa una caja centrada con estilo morado para mayor visibilidad
    return ft.Container(
        content=ft.Column([
            ft.Image(src="assets\\img\\perfil.png", width=400, height=230, fit="contain"),
            # Saludo personalizado usando el nombre del usuario
            ft.Text(f"¡Bienvenido a tu perfil, {nombre}!", size=24, weight="bold", color="#147bcb"),
            ft.Divider(height=5, color="#E6C9F5"),
            ft.Text(f"Tu correo es: {email}", size=20, weight="bold", color="#147bcb", italic=True),
            # Imagen adicional para enriquecer la pantalla de perfil
            ft.Image(src="assets\\img\\perfil2.png", width=400, height=230, fit="contain"),
        ], horizontal_alignment="center", spacing=12),
        padding=20,
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
        bgcolor="#d0e4f4",
    )