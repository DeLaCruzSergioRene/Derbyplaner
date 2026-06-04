import flet as ft

def acercaDe(page: ft.Page):
    
    return ft.Container(    
        content=ft.Column([
            ft.Text("ACERCA DE:"),
            ft.Text("Un pequeño juego inspirado en Umamusume: Pretty Derby."),
            ft.Text("Este juego desarrollado en flet con python es muy simple, seleccionas a la Umamusume que mas te agrade, seleccionas sus estadisticas con las barras de abajo, su terreno preferido y las habilidades que podría usar, creas una carrera con distancia y terreno que prefieras y listo, a jugar."),
            ft.Text("(AVISO DE COPYRIGHT)"),
            ft.Text("Esto un projecto escolar solo con fines personales y educativos."),
            ft.Text("Umamusume es una marca registrada de Cygames."),
            ft.Text("El resto de recursos como imagenes y cualquier asset van con los derechos y creditos a sus respectivos creadores."),
            ft.Image(src="assets\\img\\biw.jpg", width=400, height=500, fit="contain"),
        ], horizontal_alignment="center", spacing=12),
        padding=20,
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
        bgcolor="#e4f4d0"
    )
