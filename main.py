import flet as ft
from views.Registro import vista_registro
from views.Sesion import vista_sesion

def principal(pagina: ft.Page):
    pagina.title = "Derby Planer"
    pagina.window_width = 400
    pagina.window_height = 500
    
    def al_iniciar_sesion(usuario):
        pagina.clean()
        pagina.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"ID Usuario: {usuario['id']}", size=14),
                    ft.Text(f"Usuario: {usuario['usuario']}", size=14),
                    ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: mostrar_menu(), width=300)
                ], spacing=20, horizontal_alignment="center"),
                padding=30,
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def mostrar_menu():
        pagina.clean()
        pagina.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Derby Planer", size=32, weight="bold"),
                    ft.ElevatedButton("Registrarse", width=300, on_click=lambda e: mostrar_registro()),
                    ft.ElevatedButton("Iniciar Sesión", width=300, on_click=lambda e: mostrar_sesion())
                ], spacing=20, horizontal_alignment="center"),
                padding=30,
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def mostrar_registro():
        pagina.clean()
        pagina.add(
            ft.Container(
                content=ft.Column([
                    vista_registro(pagina, al_iniciar_sesion),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_menu(), width=300)
                ], spacing=15, horizontal_alignment="center"),
                padding=10,
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def mostrar_sesion():
        pagina.clean()
        pagina.add(
            ft.Container(
                content=ft.Column([
                    vista_sesion(pagina, al_iniciar_sesion),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_menu(), width=300)
                ], spacing=15, horizontal_alignment="center"),
                padding=10,
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    mostrar_menu()

if __name__ == "__main__":
    ft.app(target=principal)
