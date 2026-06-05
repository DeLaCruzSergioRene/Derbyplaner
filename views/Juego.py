import flet as ft
from controller.game_controller import preparar_datos_juego
from controller.race_controller import RaceSimulation
from controller.carrera_visualizacion_controller import (
	crear_card_uma, ejecutar_carrera, MAPEO_UMA_ASSETS
)

# Vista principal del juego: muestra umas, setup de carrera y ejecuta la simulación
def juego(page: ft.Page):
	page.clean()
	
	# Preparar datos: uma del jugador, 4 competidoras aleatorias y config de carrera
	datos = preparar_datos_juego(page)
	uma_seleccionada = datos['uma_seleccionada']
	umas_competidoras = datos['umas_competidoras']
	carrera_cfg = datos['carrera']

	if not carrera_cfg:
		page.snack_bar = ft.SnackBar(
			ft.Text("No hay una carrera creada. Crea una carrera primero.", color="white"),
			bgcolor="#B8141C"
		)
		page.snack_bar.open = True
		page.update()
		return

	if not uma_seleccionada or not uma_seleccionada['uma']:
		page.snack_bar = ft.SnackBar(
			ft.Text("No hay uma seleccionada. Crea y selecciona una uma primero.", color="white"),
			bgcolor="#B8141C"
		)
		page.snack_bar.open = True
		page.update()
		return

	def volver_a_carreras(e):
		page.clean()
		from views.Carrera import carrera
		carrera(page)

	def iniciar_juego(e):
		# Inicia la carrera con animación.
		page.clean()
		
		# Construir UI: simular carrera con todas las umas
		todas_umas = [uma_seleccionada] + umas_competidoras
		# Extraer distancia de string (ej: "2000m" -> 2000)
		distancia_str = carrera_cfg.get('distancia', '2000m')
		distancia = int(distancia_str.replace('m', ''))
		
		# Iniciar simulación del motor de carreras
		simulacion = RaceSimulation(todas_umas, distancia)
		
		# Componentes UI
		contador_tiempo = ft.Text("00:00", size=32, weight="bold", color="#744BB1")
		texto_fase = ft.Text("Early Race", size=14, color="#B814CE")
		
		# Crear filas de umas
		filas_umas = []
		for idx, uma in enumerate(todas_umas):
			es_jugador = (idx == 0)
			uma_asset_name = MAPEO_UMA_ASSETS.get(uma['uma'], uma['uma'].replace('.png', ''))
			
			img = ft.Image(src=f"assets/Umascorriendo/{uma_asset_name}corriendo.png", width=100, height=100, fit="contain")
			barra = ft.ProgressBar(value=0, width=400, height=30, color="#E438AB" if es_jugador else "#B814CE")
			distancia_text = ft.Text("0 / " + str(distancia), size=12, color="#4A148C")
			skill_text = ft.Text("", size=14, weight="bold", color="#FFD700", text_align="center")
			
			fila = ft.Column([
				skill_text,
				ft.Row([
					img,
					ft.Column([
						ft.Text(uma['label'], size=16, weight="bold", color="#744BB1"),
						barra,
						distancia_text,
					], spacing=5, expand=True)
				], spacing=10, vertical_alignment="center"),
			], spacing=5)
			
			filas_umas.append({'row': fila, 'img': img, 'barra': barra, 'skill_text': skill_text, 'distancia_text': distancia_text, 'uma_asset_name': uma_asset_name, 'frame': 0, 'skill_timer': 0})
		
		# Layout: 2 arriba, 2 en medio, 1 abajo
		fila_arriba = ft.Row(
			[filas_umas[0]['row'], filas_umas[1]['row']] if len(filas_umas) > 1 else [filas_umas[0]['row']],
			spacing=20,
			alignment="center"
		)
		
		fila_medio = ft.Row(
			[filas_umas[2]['row'], filas_umas[3]['row']] if len(filas_umas) > 3 else [filas_umas[2]['row']] if len(filas_umas) > 2 else [],
			spacing=20,
			alignment="center"
		)
		
		fila_abajo = ft.Row(
			[filas_umas[4]['row']] if len(filas_umas) > 4 else [],
			spacing=20,
			alignment="center"
		)
		
		# Layout
		area_carrera = ft.Column([
			ft.Column([contador_tiempo, texto_fase], spacing=5, horizontal_alignment="center"),
			ft.Divider(height=10, color="#E6C9F5"),
			fila_arriba,
			fila_medio,
			fila_abajo,
		], spacing=10, expand=True, horizontal_alignment="center")
		
		layout = ft.Column([
			area_carrera,
			ft.Row([ft.Button("Volver", on_click=volver_a_carreras)], alignment="center"),
		], spacing=10, expand=True)
		
		page.add(layout)
		page.update()
		
		# Ejecutar carrera usando controlador
		page.run_task(
			ejecutar_carrera,
			page,
			simulacion,
			todas_umas,
			distancia,
			contador_tiempo,
			texto_fase,
			filas_umas,
			volver_a_carreras,
			carrera_cfg.get('terreno', 'Pasto')
		)


	# Sidebar izquierda
	sidebar_izquierda = ft.Column([
		ft.Button("EMPEZAR JUEGO", on_click=iniciar_juego, bgcolor="#E438AB", color="white", width=220, height=50),
		ft.Divider(height=10, color="#E6C9F5"),
		ft.Text("Tu Corredora", size=14, weight="bold", color="#744BB1", text_align="center"),
		crear_card_uma(uma_seleccionada, es_seleccionada=True),
		ft.Divider(height=10, color="#E6C9F5"),
		ft.Text("Competidoras", size=14, weight="bold", color="#744BB1", text_align="center"),
	], spacing=8, horizontal_alignment="center", width=220)

	for uma in umas_competidoras:
		sidebar_izquierda.controls.append(crear_card_uma(uma, es_seleccionada=False))

	# Contenido central
	header = ft.Column([
		ft.Text(f"Carrera: {carrera_cfg.get('nombre','')}", size=22, weight="bold", color="#744BB1"),
		ft.Text(f"Distancia: {carrera_cfg.get('distancia','')}   |   Terreno: {carrera_cfg.get('terreno','')}", size=16),
		ft.Divider(height=8, color="#E6C9F5"),
	], spacing=6, horizontal_alignment="center")

	zona_juego = ft.Column([ft.Text("Presiona 'EMPEZAR JUEGO' para iniciar la carrera", size=16, color="#4A148C")], spacing=16, horizontal_alignment="center")
	contenido_central = ft.Column([header, zona_juego], spacing=16, horizontal_alignment="center", expand=True, scroll="auto")

	# Layout principal
	contenido_principal = ft.Row([
		ft.Container(
			content=ft.Column([
				sidebar_izquierda,
				ft.Row([ft.Button("Volver a Carreras", on_click=volver_a_carreras, bgcolor="#A0A0A0", color="white")], alignment="center"),
			], spacing=8, scroll="auto"),
			bgcolor="#F9F9F9",
			padding=10,
			width=250,
			expand=False,
		),
		ft.Container(
			content=contenido_central,
			bgcolor="#FFFFFF",
			padding=20,
			expand=True,
		),
	], spacing=0, expand=True)

	page.add(contenido_principal)
	page.update()