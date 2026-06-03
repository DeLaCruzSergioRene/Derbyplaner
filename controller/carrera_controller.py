import flet as ft
from models.carrera_model import DISTANCIAS, TERRENOS, construir_carrera, resumen_creacion
from models.creacion_model import get_uma_label

# Controlador para la vista de creación de carreras. Provee los controles (nombre, distancia, terreno) y muestra un mini-resumen de la `uma` seleccionada y la configuración de creación.
def carrera(page: ft.Page):
    uma_img = page.current_user.get('uma_seleccionada', 'Air_Grove.png')
    uma_label = get_uma_label(uma_img)
    creacion_config = page.current_user.get('creacion', {})

    nombre_carrera = ft.TextField(label="Nombre de la carrera", width=300, value="Mi Carrera")
    distancia = ft.Dropdown(
        label="Distancia",
        width=300,
        value=str(DISTANCIAS[2]),
        options=[ft.dropdown.Option(str(d)) for d in DISTANCIAS],
    )
    terreno = ft.Dropdown(
        label="Terreno de la carrera",
        width=300,
        value=TERRENOS[0],
        options=[ft.dropdown.Option(t) for t in TERRENOS],
    )

    def crear_nueva_carrera(e):
        try:
            config = construir_carrera(
                nombre_carrera.value,
                int(distancia.value),
                terreno.value,
            )
            page.current_user['carrera'] = config
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Carrera '{config['nombre']}' creada", color="white"),
                bgcolor="#744BB1"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(
                ft.Text(str(err), color="white"),
                bgcolor="#B8141C"
            )
            page.snack_bar.open = True
            page.update()
        # Nota: almacenamos la carrera en `page.current_user` para uso del usuario actual.

    def volver(e):
        page.clean()
        from views.Creacion import creacion
        creacion(page)

    resumen_ui = []
    resumen = resumen_creacion(creacion_config)
    if resumen:
        # Convertimos cada línea del resumen en un control de texto.
        resumen_ui = [ft.Text(line, size=14, color="#4A148C") for line in resumen]
    else:
        resumen_ui = [ft.Text("No hay configuración de creación guardada aún.", size=14, color="#4A148C")]

    contenido = ft.Column([
        ft.Text("Crear tu propia carrera", size=28, weight="bold", color="#744BB1", text_align="center"),
        ft.Image(src=f"assets/umamusumes/{uma_img}", width=220, height=220, fit="contain"),
        ft.Text(uma_label, size=22, weight="bold", color="#B814CE", text_align="center"),
        ft.Divider(height=8, color="#E6C9F5"),
        ft.Column([
            ft.Text("Tu selección de creación:", size=16, weight="bold", color="#744BB1"),
            ft.Container(
                content=ft.Column(resumen_ui, spacing=4),
                padding=12,
                bgcolor="#F5E6FF",
                border_radius=10,
                width=340,
            )
        ], spacing=10),
        ft.Divider(height=8, color="#E6C9F5"),
        nombre_carrera,
        distancia,
        terreno,
        ft.Row([
            ft.Button("Crear carrera", on_click=crear_nueva_carrera, bgcolor="#744BB1", color="white"),
            ft.Button("Volver", on_click=volver, bgcolor="#A0A0A0", color="white"),
        ], spacing=10, alignment="center"),
    ], spacing=16, horizontal_alignment="center", scroll="auto")

    page.add(
        ft.Container(
            content=contenido,
            padding=20,
            expand=True,
            bgcolor="#FFFFFF"
        )
    )
    # Fin del controlador: la vista se renderiza y queda a la espera de interacciones del usuario.
