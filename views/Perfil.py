import flet as ft

# Vista de perfil de usuario
def perfil(page: ft.Page):
    user = getattr(page, "current_user", {})
    return ft.Container(
        content=ft.Column([
            ft.Image(
                src="assets\\img\\perfil.png",
                width=400,
                height=400,
                fit="contain"
            ),
            ft.Text(f"¡Bienvenido a tu perfil, {user.get('nombre', '')}!", size=20),
            ft.Text(f"¡Tu correo es: {user.get('email', '')}!", size=16),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
    )