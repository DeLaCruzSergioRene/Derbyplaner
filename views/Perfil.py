import flet as ft

def perfil(page: ft.Page):
    user = getattr(page, "current_user", {})
    nombre = user.get('nombre', 'Usuario')
    email = user.get('email', 'correo@ejemplo.com')
    
    return ft.Container(
        content=ft.Column([
            ft.Image(src="assets\\img\\perfil.png", width=400, height=230, fit="contain"),
            ft.Text(f"¡Bienvenido a tu perfil, {nombre}!", size=24, weight="bold", color="#744BB1"),
            ft.Divider(height=5, color="#E6C9F5"),
            ft.Text(f"Tu correo es: {email}", size=20, weight="bold", color="#643BAC", italic=True),
            ft.Image(src="assets\\img\\perfil2.png", width=400, height=230, fit="contain"),
        ], horizontal_alignment="center", spacing=12),
        padding=20,
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
        bgcolor="#CD88F5",
    )