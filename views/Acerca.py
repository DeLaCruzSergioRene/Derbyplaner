import flet as ft

def acercaDe(page: ft.Page):
    
    return ft.Container(    
        content=ft.Column([
            ft.Text("ACERCA DE"),
            ft.Text("Un pequeño juego inspirado en Uma Musume"),
            ft.Text("Este juego desarrollado en flet con python es muy simple, solo crea selecciona un personaje, sus estadisticas, habilidades, etc y le das a guardar y luego ya a jugar"),
            ft.Text("AVISO DE COPYRIGHT"),
            ft.Text("esto un projecto escolar solo con fines personales y educativos"),
            ft.Text("Uma Musume es una marca registrada de Cygames"),
            ft.Text("El resto de recursos como imagenes los derechos van a sus respectivos creadores"),
            ft.Image(src="assets\\img\\biw.jpg", width=700, height=700, fit="contain"),
        ], horizontal_alignment="center", spacing=12),
        padding=20,
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
        bgcolor="#e4f4d0"
    )
    
