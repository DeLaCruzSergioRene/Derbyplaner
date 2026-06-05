import flet as ft
from controller.creacion_controller import creacion as cargar_creacion

# Vista ligera que delega la construcción a `controller.creacion_controller`. Mantener aquí solo la función wrapper facilita pruebas y navegación.
def creacion(page: ft.Page):
    cargar_creacion(page)
