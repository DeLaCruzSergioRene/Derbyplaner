import flet as ft
from database.db_operations import obtener_resultados_usuario


def resultados(page: ft.Page):
	# Vista que muestra el historial de resultados de carreras del usuario.
	page.clean()
	
	user_id = page.current_user.get('id')
	if not user_id:
		page.snack_bar = ft.SnackBar(
			ft.Text("No hay usuario autenticado", color="white"),
			bgcolor="#B8141C"
		)
		page.snack_bar.open = True
		page.update()
		return
	
	# Obtener resultados del usuario
	resultados_list = obtener_resultados_usuario(user_id)
	
	def volver(e):
		page.clean()
		from views.Menu import menu
		menu(page)
	
	# Header
	header = ft.Column([
		ft.Text("📊 HISTORIAL DE CARRERAS", size=32, weight="bold", color="#744BB1", text_align="center"),
		ft.Divider(height=15, color="#E6C9F5"),
	], spacing=10, horizontal_alignment="center")
	
	# Si no hay resultados
	if not resultados_list:
		contenido = ft.Column([
			header,
			ft.Text("No hay carreras registradas aún", size=16, color="#B814CE", text_align="center"),
			ft.Divider(height=20),
			ft.Row([ft.Button("Volver", on_click=volver)], alignment="center"),
		], spacing=20, expand=True, horizontal_alignment="center")
		page.add(contenido)
		page.update()
		return
	
	# Construir lista de resultados
	resultados_col = ft.Column([header], spacing=15)
	
	for idx, res in enumerate(resultados_list, 1):
		# Convertir fecha a formato legible
		fecha_obj = res.get('fecha')
		if fecha_obj:
			fecha_str = fecha_obj.strftime("%d/%m/%Y %H:%M") if hasattr(fecha_obj, 'strftime') else str(fecha_obj)
		else:
			fecha_str = "N/A"
		
		# Convertir tiempo (segundos) a formato mm:ss o mostrar DNF
		tiempo_segundos = res.get('tiempo')
		if tiempo_segundos is not None:
			minutos = tiempo_segundos // 60
			segundos = tiempo_segundos % 60
			tiempo_str = f"{minutos:02d}:{segundos:02d}"
		else:
			tiempo_str = "DNF"
		
		# Obtener habilidades
		habilidades = []
		for i in range(1, 4):
			hab_key = f"hab_{i}"
			hab = res.get(hab_key)
			if hab:
				habilidades.append(hab)
		habilidades_str = ", ".join(habilidades) if habilidades else "Sin habilidades"
		
		# Medalla según posición
		posicion = res.get('posicion', 0)
		
		# Generar medalla solo para 1º, 2º, 3º; para 4º y 5º solo número
		if posicion <= 3:
			medalla_map = {1: "🥇", 2: "🥈", 3: "🥉"}
			medalla = medalla_map[posicion]
			posicion_str = f"{medalla} {posicion}º"
		else:
			posicion_str = f"{posicion}º"
		
		# Color según posición
		color_posicion = "#E438AB" if posicion == 1 else "#B814CE"
		
		# Contenedor del resultado
		resultado_item = ft.Container(
			content=ft.Container(
				content=ft.Column([
					# Fila superior: ID, posición, fecha
					ft.Row([
						ft.Text(f"ID: {res.get('id')}", size=12, color="#744BB1", weight="bold"),
						ft.Text(f"Posición: {posicion_str}", size=14, weight="bold", color=color_posicion, expand=True),
						ft.Text(f"Fecha: {fecha_str}", size=12, color="#744BB1"),
					], spacing=15, alignment="space-between"),
					
					# Fila: Uma y terreno
					ft.Row([
						ft.Text(f"Uma: {res.get('nombre', 'N/A')}", size=13, weight="bold", color="#4A148C", expand=True),
						ft.Text(f"Terreno: {res.get('terreno', 'N/A')}", size=13, color="#4A148C"),
					], spacing=15),
					
					# Fila: Distancia y tiempo
					ft.Row([
						ft.Text(f"Distancia: {res.get('dist', 0)}m", size=13, color="#4A148C", expand=True),
						ft.Text(f"⏱ Tiempo: {tiempo_str}", size=13, weight="bold", color="#E438AB"),
					], spacing=15),
					
					# Fila: Habilidades
					ft.Row([
						ft.Text("Habilidades usadas:", size=12, weight="bold", color="#744BB1"),
						ft.Text(habilidades_str, size=12, color="#4A148C", expand=True),
					], spacing=10),
				], spacing=8),
				padding=15,
				bgcolor="#F5E6FF",
				border_radius=8,
			),
			bgcolor=color_posicion,
			border_radius=8,
			padding=2,
		)
		
		resultados_col.controls.append(resultado_item)
	
	# Divider y botón volver
	resultados_col.controls.append(ft.Divider(height=15, color="#E6C9F5"))
	resultados_col.controls.append(
		ft.Row([
			ft.Button("Volver", on_click=volver, bgcolor="#744BB1", color="white", width=200, height=45),
		], alignment="center")
	)
	
	# Scroll view
	scroll_view = ft.Column([resultados_col], expand=True, scroll="auto")
	page.add(scroll_view)
	page.update()
