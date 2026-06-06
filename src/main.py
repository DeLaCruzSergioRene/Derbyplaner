import flet as ft
import dotenv 
dotenv.load_dotenv()
from views.Registro import vista_registro
from views.Sesion import vista_sesion
from views.Recuperar import recuperar
from views.Menu import menu

@ft.control
class boton(ft.Button):
    def init(self):
        self.bgcolor = ft.Colors.WHITE
        self.color = ft.Colors.BLUE_ACCENT_100
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=3)
        ) 


def main(page: ft.Page):
    page.title = "Derby Planer"

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
                    ft.Text("Derby Planer", size=32, weight="bold"),
                    boton("Registrarse", width=300, on_click=lambda e: mostrar_registro()),
                    boton("Iniciar Sesión", width=300, on_click=lambda e: mostrar_sesion()),
                ], spacing=20, horizontal_alignment="center"),
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
                    boton("Volver", on_click=lambda e: mostrar_menu(), width=300)
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
                    boton("Volver", on_click=lambda e: mostrar_menu(), width=300),
                    ft.TextButton("¿Haz olvidado la contraseña?", on_click=lambda e: recuperar(page, mostrar_menu))
                ], spacing=15, horizontal_alignment="center"),
                padding=10,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True 
            )
        )
    mostrar_menu()

ft.run(main)