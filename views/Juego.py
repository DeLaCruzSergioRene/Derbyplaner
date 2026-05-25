import flet as ft

def juego(page: ft.Page):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="the"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="the"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Favorites",
            ),
        ]
    )

    page.add(
        ft.SafeArea(
            content=ft.Text("Vacio, no hay nada!"),
        )
    )