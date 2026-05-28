import flet as ft
from views.Perfil import UserView


def menu(page: ft.Page, al_exito):
    body = ft.Container(expand=True)

    def mostrar_tab(e):
        if e.control.selected_index == 2:
            body.content = UserView(page)
        else:
            body.content = ft.Text("Selecciona una opción")
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
        selected_index=0,
        on_change=mostrar_tab,
    )

    page.add(body)
    body.content = ft.Text("Selecciona una opción")
    page.update()
    #page.add(ft.Container(
    #        content=ft.Column([
    #            ft.Text("eeeeeeeeeeeeeeeeeeeeee", size=16, weight="bold"),
    #        ], spacing=15, horizontal_alignment="center"),
    #        padding=30, expand=True, alignment=ft.alignment.Alignment(0, 0),
    #    ))