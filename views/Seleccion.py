import flet as ft
from controller.seleccion_controller import cargar_seleccion

# Vista para la selección; delega la lógica al controlador. Mantener la vista ligera permite mantener separación de responsabilidades.
def seleccion(page: ft.Page):
    cargar_seleccion(page)
