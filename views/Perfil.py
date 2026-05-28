import flet as ft

# Vista de perfil de usuario
def UserView(page: ft.Page):
    user = page.current_user

    # Vista simple del perfil
    return ft.View(
        route="/perfil",
        appbar=ft.AppBar(title=ft.Text("Perfil")),
        controls=[
            ft.Column([
                ft.Text(f"Nombre: {user['nombre']}", size=20),
                ft.Text(f"Email: {user['email']}", size=16),
                ft.Button("Volver", on_click=lambda _: page.go("/menu"))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        ]
    )