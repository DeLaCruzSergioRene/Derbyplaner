import flet as ft

# Define las habilidades agrupadas por tipo para la pantalla de creación
HABILIDADES = {
    "Velocidad": ["Sprint Boost", "Aceleración", "Velocidad Máxima", "Salida Rápida"],
    "Poder": ["Arrancada Fuerte", "Salto Poderoso", "Empuje Final", "Resistencia Bruta"],
    "Recuperación": ["Segundo Aire", "Resistencia", "Recuperación", "Defensa"],
}

def creacion(page: ft.Page):
    # Recupera la uma seleccionada y prepara el nombre legible
    uma_img = page.current_user.get('uma_seleccionada', 'Air_Grove.png')
    uma_label = uma_img.replace("_", " ").replace(".png", "")
    
    # Sliders
    slider_vel = ft.Slider(value=300, min=0, max=1000, divisions=20, label="{value}", width=300)
    slider_sta = ft.Slider(value=300, min=0, max=1000, divisions=20, label="{value}", width=300)
    slider_pow = ft.Slider(value=300, min=0, max=1000, divisions=20, label="{value}", width=300)
    slider_int = ft.Slider(value=300, min=0, max=1000, divisions=20, label="{value}", width=300)
    
    # Dropdown terreno
    terreno = ft.Dropdown(
        value="Pasto",
        options=[ft.dropdown.Option("Pasto"), ft.dropdown.Option("Tierra")],
        width=250,
        label="Terreno"
    )
    
    # Habilidades - Checkboxes con iconos
    habilidades_seleccionadas = {}
    
    # Restringe la selección a un máximo de 3 habilidades
    def limitar_habilidades(e):
        total = sum(1 for cb in habilidades_seleccionadas.values() if cb.value)
        if total > 3:
            e.control.value = False
            page.snack_bar = ft.SnackBar(ft.Text("Solo puedes seleccionar hasta 3 habilidades", color="white"), bgcolor="#B814CE")
            page.snack_bar.open = True
            page.update()
    
    # Crea cada sección de habilidades con icono y checkboxes
    def crear_seccion_habilidades(tipo, icono_path):
        hab_grupo = []
        for hab in HABILIDADES[tipo]:
            cb = ft.Checkbox(label=hab, value=False, label_style=ft.TextStyle(color="#B814CE"), on_change=limitar_habilidades)
            hab_grupo.append(cb)
            habilidades_seleccionadas[hab] = cb
        
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
    
    # Guarda la configuración seleccionada en el usuario actual, lo cambiare a futuro
    def guardar_creacion(e):
        config = {
            'uma': uma_img,
            'velocidad': slider_vel.value,
            'stamina': slider_sta.value,
            'poder': slider_pow.value,
            'inteligencia': slider_int.value,
            'terreno': terreno.value,
            'habilidades': [hab for hab, cb in habilidades_seleccionadas.items() if cb.value]
        }
        page.current_user['creacion'] = config
        print(f"Creación guardada: {config}")
        page.snack_bar = ft.SnackBar(ft.Text(f"¡{uma_label} creado exitosamente!", color="white"))
        page.snack_bar.open = True
        page.update()
    
    def volver(e):
        page.clean()
        from views.Seleccion import seleccion
        seleccion(page)
    
    contenido = ft.Column([
        ft.Text(uma_label, size=28, weight="bold", color="#B814CE", text_align="center"),
        ft.Image(src=f"assets/umamusumes/{uma_img}", width=180, height=180, fit="contain"),
        
        # Separador y título de la sección de estadísticas
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Text("ESTADÍSTICAS", size=16, weight="bold", color="#B814CE", text_align="center"),
        
        # Sliders para ajustar cada atributo principal
        ft.Row([ft.Text("Velocidad:", width=100, color="#B814CE"), slider_vel], spacing=10, alignment="center"),
        ft.Row([ft.Text("Stamina:", width=100, color="#B814CE"), slider_sta], spacing=10, alignment="center"),
        ft.Row([ft.Text("Poder:", width=100, color="#B814CE"), slider_pow], spacing=10, alignment="center"),
        ft.Row([ft.Text("Inteligencia:", width=100, color="#B814CE"), slider_int], spacing=10, alignment="center"),
        
        # Selección de terreno preferido para la uma
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Row([ft.Text("Terreno:", width=100, color="#B814CE"), terreno], spacing=10, alignment="center"),
        
        # Sección de habilidades agrupada por tipo
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Text("HABILIDADES", size=16, weight="bold", color="#B814CE", text_align="center"),
        
        crear_seccion_habilidades("Velocidad", "assets/img/habilidad_velocidad.png"),
        crear_seccion_habilidades("Poder", "assets/img/habilidad_poder.png"),
        crear_seccion_habilidades("Recuperación", "assets/img/habilidad_recuperacion.png"),
        
        # Botones de acción para guardar la configuración o regresar
        ft.Divider(height=10, color="#E6C9F5"),
        ft.Row([
            ft.Button("Guardar", on_click=guardar_creacion, bgcolor="#744BB1", color="white"),
            ft.Button("Volver", on_click=volver, bgcolor="#A0A0A0", color="white"),
        ], spacing=10, alignment="center"),
    ], spacing=12, horizontal_alignment="center", scroll="auto")
    
    page.add(
        ft.Container(
            content=contenido,
            padding=20,
            expand=True,
            bgcolor="#FFFFFF"
        )
    )
