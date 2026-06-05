import flet as ft
from models.seleccion_model import UMAS, get_uma_label

# Controlador de selección de umas. Genera la rejilla de botones con imagenes y gestiona la selección.
def cargar_seleccion(page: ft.Page):
    def on_click_uma(e, uma_name):
        page.current_user['uma_seleccionada'] = uma_name
        page.clean()
        from views.Creacion import creacion
        creacion(page)

    # Se construye una lista de `buttons` usando una list comprehension.
    # Nota: se usa `on_click=lambda e, u=uma: on_click_uma(e, u)` para fijar...
    # El valor actual de `uma` en cada lambda.
    buttons = [
        ft.Container(
            content=ft.Column([
                ft.Text(get_uma_label(uma), size=18, weight="bold", color="#E438AB", text_align="center"),
                ft.Image(src=f"assets/umamusumes/{uma}", width=160, height=160, fit="contain"),
            ], spacing=3, horizontal_alignment="center"),
            ink=True,
            bgcolor="#EDEEEF",
            on_click=lambda e, u=uma: on_click_uma(e, u)
        )
        for uma in UMAS
    ]

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Selecciona a tu corredora:", size=28, weight="bold", color="#744BB1", text_align="center"),
                ft.GridView(
                    controls=buttons,
                    runs_count=5,
                    spacing=10,
                    run_spacing=10,
                    expand=True,
                    auto_scroll=True,
                )
            ], spacing=20, expand=True),
            padding=15,
            expand=True,
            bgcolor="#CCE6FF"
        )
    )
    # Guardamos en `page.current_user` para uso inmediato.
