import flet as ft
from views.Juego import juego 

def menu(page: ft.Page, al_exito):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ]
    )

    #page.add(
    #    ft.SafeArea(
    #        content=ft.Text("Selecciona una opción"),
    #    )
    #)
    page.add(ft.Image(
        src="assets\img\dormitorio.jpg",
        #width=200,
        #height=200,
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