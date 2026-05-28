import flet as ft
from views.Juego import juego
from views.Perfil import perfil

def menu(page: ft.Page, usuario):
    page.current_user = usuario

    def cambiar_vista(e):
        page.clean()
        if e.control.selected_index == 2:
            page.add(perfil(page))
        else:
            page.add(ft.Image(
                src="assets\\img\\dormitorio.jpg",
                fit="cover",
                border_radius=ft.BorderRadius.all(10),
                repeat=ft.ImageRepeat.NO_REPEAT
            ))

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
        on_change=cambiar_vista,
    )

    page.add(ft.Image(
        src="assets\\img\\dormitorio.jpg",
        fit="cover",
        border_radius=ft.BorderRadius.all(10),
        repeat=ft.ImageRepeat.NO_REPEAT
    ))
    #page.add(ft.Container(
    #        content=ft.Column([
    #            ft.Text("eeeeeeeeeeeeeeeeeeeeee", size=16, weight="bold"),
    #        ], spacing=15, horizontal_alignment="center"),
    #        padding=30, expand=True, alignment=ft.alignment.Alignment(0, 0),
    #    ))