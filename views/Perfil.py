import flet as ft

# Vista de perfil de usuario
def UserView(page: ft.Page):
    user = getattr(page, "current_user", {"nombre": "Usuario", "email": "desconocido@example.com"})
    return ft.Column(
        [
            ft.Image(src="assets/img/perfil.png", width=120, height=120),
            ft.Text(user["nombre"], size=20),
            ft.Text(user["email"], size=16),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )