import flet as ft

def acercaDe(page: ft.Page):
    return ft.Container(
        content=ft.Column([
            ft.Text("ACERCA DE"),
            ft.Text("Un pequeño juego inspirado en Uma Musume"),
            ft.Text("No tomamos ningun derecho de cualquier imagen/recurso usado en este projecto, es un projecto escolar solo con fines personales y educativos"),
            ft.Text("Uma Musume es una marca registrada de Cygames"),
            ft.Text("BIWA MI ESPOSA"),
        ], horizontal_alignment="center", spacing=12),
        padding=20,
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
    )
