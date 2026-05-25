import flet as ft
from views.Juego import juego 

def menu(page: ft.Page, al_exito):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Favorites",
            ),
        ]
    )

    page.add(
        ft.SafeArea(
            content=ft.Text("Body!"),
        )
    )
    #page.add(ft.Container(
    #        content=ft.Column([
    #            ft.Text("eeeeeeeeeeeeeeeeeeeeee", size=16, weight="bold"),
    #        ], spacing=15, horizontal_alignment="center"),
    #        padding=30, expand=True, alignment=ft.alignment.Alignment(0, 0),
    #    ))