import flet as ft
from models.carrera_model import DISTANCIAS, TERRENOS, construir_carrera, resumen_creacion
from models.creacion_model import get_uma_label
from database.db_operations import guardar_carrera

# Controlador de carreras: configura distancia, terreno y guarda en BD para ejecutar la carrera
def carrera(page: ft.Page):
    # Cargar datos de la uma creada y la carrera actual (si existe)
    uma_img = page.current_user.get('uma_seleccionada', 'Air_Grove.png')
    uma_label = get_uma_label(uma_img)
    creacion_config = page.current_user.get('creacion', {})
    carrera_cfg = page.current_user.get('carrera')

    # Campos para configurar la carrera (nombre, distancia, terreno)
    nombre_carrera = ft.TextField(
        label="Nombre de la carrera",
        width=300,
        value=carrera_cfg.get('nombre', 'Mi Carrera') if carrera_cfg else 'Mi Carrera'
    )
    distancia = ft.Dropdown(
        label="Distancia",
        width=300,
        value=carrera_cfg.get('distancia', str(DISTANCIAS[2])) if carrera_cfg else str(DISTANCIAS[2]),
        options=[ft.dropdown.Option(str(d)) for d in DISTANCIAS],
    )
    terreno = ft.Dropdown(
        label="Terreno de la carrera",
        width=300,
        value=carrera_cfg.get('terreno', TERRENOS[0]) if carrera_cfg else TERRENOS[0],
        options=[ft.dropdown.Option(t) for t in TERRENOS],
    )

    def crear_nueva_carrera(e):
        try:
            # Construir y validar la configuración de la carrera
            config = construir_carrera(
                nombre_carrera.value,
                distancia.value,
                terreno.value,
            )
            page.current_user['carrera'] = config
            
            # Guardar carrera en BD
            distancia_int = int(config['distancia'].replace('m', ''))
            carrera_id = guardar_carrera(distancia_int, config['terreno'])
            if carrera_id:
                page.current_user['carrera_id_bd'] = carrera_id
            
            estado_text.value = "Carrera creada y lista para jugar."
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Carrera '{config['nombre']}' creada en BD", color="white"),
                bgcolor="#2E7D32"
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

    def volver(e):
        page.clean()
        from views.Creacion import creacion
        creacion(page)

    def ir_a_juego(e):
        carrera_cfg = page.current_user.get('carrera')
        if not carrera_cfg:
            nombre_seleccionado = nombre_carrera.value.strip() or f"Carrera de {uma_label}"
            distancia_seleccionada = distancia.value
            terreno_seleccionado = terreno.value
            try:
                config = construir_carrera(
                    nombre_seleccionado,
                    distancia_seleccionada,
                    terreno_seleccionado,
                )
                page.current_user['carrera'] = config
                carrera_cfg = config
                
                # Guardar en BD si no estaba
                if 'carrera_id_bd' not in page.current_user:
                    distancia_int = int(config['distancia'].replace('m', ''))
                    carrera_id = guardar_carrera(distancia_int, config['terreno'])
                    if carrera_id:
                        page.current_user['carrera_id_bd'] = carrera_id
                        
            except Exception:
                page.snack_bar = ft.SnackBar(
                    ft.Text("No hay una carrera creada. Crea una carrera primero.", color="white"),
                    bgcolor="#B8141C"
                )
                page.snack_bar.open = True
                page.update()
                return

        page.snack_bar = ft.SnackBar(
            ft.Text("Abriendo la vista de juego...", color="white"),
            bgcolor="#2E7D32"
        )
        page.snack_bar.open = True
        page.clean()
        from views.Juego import juego
        juego(page)
        page.update()

    resumen_ui = []
    resumen = resumen_creacion(creacion_config)
    if resumen:
        # Convertimos cada línea del resumen en un control de texto.
        resumen_ui = [ft.Text(line, size=14, color="#4A148C") for line in resumen]
    else:
        resumen_ui = [ft.Text("No hay configuración de creación guardada aún.", size=14, color="#4A148C")]

    estado_text = (
        f"Carrera '{carrera_cfg.get('nombre')}' creada y lista para jugar." if carrera_cfg else
        "Aún no has creado la carrera, por favor elige la distancia, el terreno y si gustas un nombre personalizado. Luego, pulsa 'Crear carrera'."
    )
    estado_ui = ft.Text(estado_text, size=14, color="#4A148C")

    contenido = ft.Column([
        ft.Text("Crear tu propia carrera", size=28, weight="bold", color="#744BB1", text_align="center"),
        ft.Image(src=f"assets/umamusumes/{uma_img}", width=220, height=220, fit="contain"),
        ft.Text(uma_label, size=22, weight="bold", color="#B814CE", text_align="center"),
        ft.Divider(height=8, color="#E6C9F5"),
        estado_ui,
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
            ft.Button("Ir al juego", on_click=ir_a_juego, bgcolor="#2E7D32", color="white"),
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
