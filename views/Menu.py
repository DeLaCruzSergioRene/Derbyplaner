import flet as ft
from views.Seleccion import seleccion
from views.Perfil import perfil
from views.Acerca import acercaDe
from views.Resultados import resultados

# Menú principal con navegación entre secciones
def menu(page: ft.Page, usuario=None):

    # Cambia la vista al navegar en la barra inferior
    def cambiar_vista(e):
        page.clean()
        if e.control.selected_index == 0:
            seleccion(page)
        elif e.control.selected_index == 1:
            resultados(page)
        elif e.control.selected_index == 2:
            page.add(perfil(page))
        elif e.control.selected_index == 3:
            page.add(acercaDe(page))
        else:
            page.add(ft.Image(
                src="assets/img/dormitorio.jpg",
                fit="cover",
            ))

    # Barra de navegación principal con opciones de juego, historial y perfil
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.GAMEPAD, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Historial"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Acerca de..."),
        ],
        on_change=cambiar_vista,
    )

    # Muestra el fondo inicial del menú cuando se abre la aplicación
    # El contenido se reemplaza cuando el usuario navega a otra sección
    page.add(ft.Image(
        src="assets/img/dormitorio.jpg",
        fit="cover",
    ))
    