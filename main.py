import flet as ft
import dotenv 
dotenv.load_dotenv()
from views.Registro import vista_registro
from views.Sesion import vista_sesion
from views.Recuperar import recuperar
from views.Menu import menu

def main(page: ft.Page):
    page.title = "Derby Planer"
    page.window_width = 400
    page.window_height = 500
    
    #page.foreground_decoration = ft.BoxDecoration(
    #    gradient=ft.LinearGradient(
    #        colors=[
    #            ft.Colors.with_opacity(0.2, ft.Colors.RED),  # use lightly transparent colors instead of solid ones
    #           ft.Colors.with_opacity(0.2, ft.Colors.BLUE),
    #        ],
    #    ),
    #    image=ft.DecorationImage(
    #       src="assets\img\dormitorio.jpg",            opacity=0.2,
    #   ),
    #)
    
    def al_iniciar_sesion(usuario):
        page.current_user = usuario
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    menu(page, usuario)
                ], spacing=20, horizontal_alignment="center"),                #padding=30,
                #alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        )
    
    def mostrar_menu():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Derby Planer", size=32, weight="bold"),
                    ft.Button("Registrarse", width=300, on_click=lambda e: mostrar_registro()),
                    ft.Button("Iniciar Sesión", width=300, on_click=lambda e: mostrar_sesion())
                ], spacing=20, horizontal_alignment="center"),
                padding=30,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        )
    
    def mostrar_registro():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    vista_registro(page, al_iniciar_sesion),
                    ft.Button("Volver", on_click=lambda e: mostrar_menu(), width=300)
                ], spacing=15, horizontal_alignment="center"),
                padding=10,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        )
    
    def mostrar_sesion():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    vista_sesion(page, al_iniciar_sesion),
                    ft.Button("Volver", on_click=lambda e: mostrar_menu(), width=300),
                    ft.TextButton("¿Haz olvidado la contraseña?", on_click=lambda e: recuperar(page, mostrar_menu))
                ], spacing=15, horizontal_alignment="center"),
                padding=10,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True 
            )
        )
    mostrar_menu()

ft.run(main)
