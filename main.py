import flet as ft
import dotenv 
dotenv.load_dotenv()
from views.Registro import vista_registro
from views.Sesion import vista_sesion
from views.Recuperar import recuperar
from views.Menu import menu

def main(page: ft.Page):
    page.title = "Derby Planer"
    #page.window_width = 400
    #page.window_height = 500
    
    def al_iniciar_sesion(usuario):
        page.current_user = usuario
        page.foreground_decoration = None
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    menu(page, usuario),
                ], spacing=20, horizontal_alignment="center"),                
                expand=True
            )
        )
    
    def mostrar_menu():
        page.foreground_decoration = ft.BoxDecoration(
            image=ft.DecorationImage(
                src="assets/img/umc.jpg",
                fit="cover",
                opacity=0.2,
            ),
        )
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Derby Planer", size=36, weight="bold"),
                    ft.Button("Registrarse", width=300, height=55, elevation=4, on_click=lambda e: mostrar_registro(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.Button("Iniciar Sesión", width=300, height=55, elevation=4, on_click=lambda e: mostrar_sesion(), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))),
                ], spacing=25, horizontal_alignment="center"),
                padding=30,
                alignment=ft.alignment.Alignment(0, 0.25),
                expand=True
            )
            
        )
    
    def mostrar_registro():
        page.foreground_decoration = None
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
        page.foreground_decoration = None
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
