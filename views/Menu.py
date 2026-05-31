import flet as ft
from views.Seleccion import seleccion
from views.Perfil import perfil

def menu(page: ft.Page, usuario):

    def cambiar_vista(e):
        page.clean()
        if e.control.selected_index == 0:
            seleccion(page)
        elif e.control.selected_index == 2:
            page.add(perfil(page))
        else:
            page.add(ft.Image(
                src="assets/img/dormitorio.jpg",
                fit="cover",
            ))

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.GAMEPAD, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
        on_change=cambiar_vista,
    )

    page.add(ft.Image(
        src="assets/img/dormitorio.jpg",
        fit="cover",
    ))
    