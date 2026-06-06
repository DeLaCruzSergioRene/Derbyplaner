import flet as ft
from models.creacion_model import (
    HABILIDADES,
    construir_configuracion,
    get_uma_label,
    obtener_habilidades_seleccionadas,
)
from database.db_operations import guardar_uma_creada

# Controlador de creación de umas: configura stats, terreno y habilidades, luego guarda en BD
def creacion(page: ft.Page):
    # Cargar uma seleccionada previamente
    uma_img = page.current_user.get('uma_seleccionada', 'Air_Grove.png')
    uma_label = get_uma_label(uma_img)

    # Sliders para los 4 stats principales (rango 0-1000)
    slider_vel = ft.Slider(value=300, min=200, max=1000, divisions=16, label="{value}", width=300)
    slider_sta = ft.Slider(value=300, min=200, max=1000, divisions=16, label="{value}", width=300)
    slider_pow = ft.Slider(value=300, min=200, max=1000, divisions=16, label="{value}", width=300)
    slider_int = ft.Slider(value=300, min=200, max=1000, divisions=16, label="{value}", width=300)

    # Dropdown para seleccionar terreno favorito (afecta el rendimiento)
    terreno = ft.Dropdown(
        value="Pasto",
        options=[ft.dropdown.Option("Pasto"), ft.dropdown.Option("Tierra")],
        width=250,
        label="Terreno"
    )

    # Dict para rastrear habilidades seleccionadas (máx 3)
    habilidades_seleccionadas = {}
    
    # Elemento para mostrar mensaje de éxito
    mensaje_ui = ft.Text("", size=14, color="#2E7D32", text_align="center", weight="bold")

    def limitar_habilidades(e):
        total = sum(1 for cb in habilidades_seleccionadas.values() if cb.value)
        if total > 3:
            e.control.value = False
            page.snack_bar = ft.SnackBar(
                ft.Text("Solo puedes seleccionar hasta 3 habilidades", color="white"),
                bgcolor="#B814CE"
            )
            page.snack_bar.open = True
            page.update()
            # Nota: el SnackBar informa al usuario dentro de la app.
            

    def crear_seccion_habilidades(tipo, icono_path):
        hab_grupo = []
        for hab in HABILIDADES[tipo]:
            cb = ft.Checkbox(
                label=hab,
                value=False,
                label_style=ft.TextStyle(color="#B814CE"),
                on_change=limitar_habilidades,
            )
            hab_grupo.append(cb)
            habilidades_seleccionadas[hab] = cb

        # Cada sección combina un título con una lista de checkboxes.
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Image(src=icono_path, width=28, height=28),
                    ft.Text(tipo, size=16, weight="bold", color="#B814CE")
                ], spacing=10),
                ft.Column(hab_grupo, spacing=5)
            ], spacing=8),
            padding=10,
            bgcolor="#F5E6FF",
            border_radius=10
        )

    def guardar_creacion(e):
        # Construir config de la uma con todos los valores de UI
        habilidades = obtener_habilidades_seleccionadas(habilidades_seleccionadas)
        config = construir_configuracion(
            uma_img,
            velocidad=slider_vel.value,
            stamina=slider_sta.value,
            poder=slider_pow.value,
            inteligencia=slider_int.value,
            terreno=terreno.value,
            habilidades=habilidades,
        )

        page.current_user['creacion'] = config
        
        # Guardar en BD si el usuario está autenticado
        user_id = page.current_user.get('id', None)
        if user_id:
            config_para_bd = {
                'uma': uma_img,
                'label': uma_label,
                'velocidad': slider_vel.value,
                'stamina': slider_sta.value,
                'poder': slider_pow.value,
                'inteligencia': slider_int.value,
                'terreno': terreno.value,
                'habilidades': habilidades,
            }
            uma_id = guardar_uma_creada(user_id, config_para_bd)
            if uma_id:
                page.current_user['uma_id_bd'] = uma_id
        
        mensaje_ui.value = f"✓ ¡{uma_label} creada exitosamente!"
        page.update()

    def crear_carrera(e):
        page.clean()
        from views.Carrera import carrera
        carrera(page)

    def volver(e):
        page.clean()
        from views.Seleccion import seleccion
        seleccion(page)

    contenido = ft.Column([
        ft.Text(uma_label, size=28, weight="bold", color="#B814CE", text_align="center"),
        ft.Image(src=f"assets/umamusumes/{uma_img}", width=200, height=200, fit="contain"),
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Text("ESTADÍSTICAS", size=16, weight="bold", color="#B814CE", text_align="center"),
        ft.Row([ft.Text("Velocidad:", width=100, color="#B814CE"), slider_vel], spacing=10, alignment="center"),
        ft.Row([ft.Text("Stamina:", width=100, color="#B814CE"), slider_sta], spacing=10, alignment="center"),
        ft.Row([ft.Text("Poder:", width=100, color="#B814CE"), slider_pow], spacing=10, alignment="center"),
        ft.Row([ft.Text("Inteligencia:", width=100, color="#B814CE"), slider_int], spacing=10, alignment="center"),
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Row([ft.Text("Terreno:", width=100, color="#B814CE"), terreno], spacing=10, alignment="center"),
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Text("HABILIDADES", size=16, weight="bold", color="#B814CE", text_align="center"),
        crear_seccion_habilidades("Velocidad", "assets/img/habilidad_velocidad.png"),
        crear_seccion_habilidades("Poder", "assets/img/habilidad_poder.png"),
        crear_seccion_habilidades("Recuperación", "assets/img/habilidad_recuperacion.png"),
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Row([
            ft.Button("Guardar", on_click=guardar_creacion, bgcolor="#744BB1", color="white"),
            ft.Button("Crear carrera", on_click=crear_carrera, bgcolor="#3D6AE3", color="white"),
            ft.Button("Volver", on_click=volver, bgcolor="#A0A0A0", color="white"),
        ], spacing=10, alignment="center"),
        mensaje_ui,
    ], spacing=12, horizontal_alignment="center", scroll="auto")

    page.add(
        ft.Container(
            content=contenido,
            padding=20,
            expand=True,
            bgcolor="#FFFFFF"
        )
    )
