import asyncio
import random
import flet as ft
from models.race_engine_model import RaceEngine
from database.db_operations import guardar_resultado

# Mapeo de nombres de umas a nombres en assets
MAPEO_UMA_ASSETS = {
	"Air_Grove.png": "Grove",
	"El_Condor_Pasa.png": "Condor",
	"Daiwa_Scarlet.png": "Daiwa",
	"GoldShip.png": "Gold",
	"Grass_Wonder.png": "Wonder",
	"Kitasan_Black.png": "Kitasan",
	"Manhattan_Cafe.png": "Manhattan",
	"Mejiro_Bright.png": "Bright",
	"Mejiro_Dober.png": "Dober",
	"Mejiro_McQueen.png": "McQueen",
	"Narita_Brian.png": "Narita",
	"Oguri_Cap.png": "Oguri",
	"Silence_Suzuka.png": "Suzuka",
	"Special_Week.png": "Week",
	"Señorita_CB.png": "CB",
	"Still_In_Love.png": "Still",
	"Sweep_Tosho.png": "Tosho",
	"Symboli_Rudolf.png": "Rudolf",
	"Tokai_Teio.png": "Teio",
	"Vodka.png": "Vodka",
}


def crear_card_uma(uma: dict, es_seleccionada: bool = False) -> ft.Container:
	"""Crea una tarjeta con la información de una uma."""
	color_borde = "#E438AB" if es_seleccionada else "#B814CE"
	color_fondo = "#FFE6F7" if es_seleccionada else "#F5E6FF"
	ancho = 220 if es_seleccionada else 180
	grosor_borde = 3 if es_seleccionada else 1
	
	stats_text = f"""
Velocidad: {uma['velocidad']}
Stamina: {uma['stamina']}
Poder: {uma['poder']}
Inteligencia: {uma['inteligencia']}
Terreno: {uma['terreno']}"""
	
	habilidades_text = ", ".join(uma['habilidades']) if uma['habilidades'] else "Sin habilidades"
	
	contenido = ft.Column([
		ft.Text(
			uma['label'],
			size=14 if not es_seleccionada else 16,
			weight="bold",
			color=color_borde,
			text_align="center"
		),
		ft.Image(
			src=f"assets/umamusumes/{uma['uma']}",
			width=140 if es_seleccionada else 120,
			height=140 if es_seleccionada else 120,
			fit="contain"
		),
		ft.Text(
			stats_text.strip(),
			size=11 if not es_seleccionada else 12,
			color="#4A148C",
			text_align="center"
		),
		ft.Text(
			f"Habilidades: {habilidades_text}",
			size=10 if not es_seleccionada else 11,
			color="#744BB1",
			text_align="center",
			weight="w600"
		),
	], spacing=5, horizontal_alignment="center")
	
	# Envolver con borde usando container anidado
	return ft.Container(
		content=ft.Container(
			content=contenido,
			padding=10 if es_seleccionada else 8,
			bgcolor=color_fondo,
			border_radius=10,
		),
		bgcolor=color_borde,
		border_radius=10,
		padding=grosor_borde,
		width=ancho,
	)


async def ejecutar_carrera(page: ft.Page, simulacion, todas_umas: list, distancia: int, 
							contador_tiempo, texto_fase, filas_umas: list, volver_callback, terreno_carrera: str = None):
	# Loop principal: cada tick actualiza velocidad, desgaste, habilidades e imagen
	habilidades_count = {}
	
	while not simulacion._carrera_terminada():
		simulacion.tick += 1
		fase = simulacion._get_fase_actual()
		
		# Actualizar cada uma
		for idx in range(len(todas_umas)):
			if simulacion.progreso[idx] >= distancia:
				# Registrar tiempo de llegada cuando cruza la meta
				if simulacion.tiempo_llegada[idx] is None:
					simulacion.tiempo_llegada[idx] = simulacion.tiempo
				continue
			
			uma = simulacion.umas[idx]
			
			# Aplicar desgaste y reducir stats (velocidad, stamina, poder)
			desgaste = RaceEngine.calcular_desgaste(uma, fase, terreno_carrera)
			uma['velocidad'] = max(0, uma['velocidad'] - desgaste['velocidad'])
			uma['stamina'] = max(0, uma['stamina'] - desgaste['stamina'])
			uma['poder'] = max(0, uma['poder'] - desgaste['poder'])
			
			# Calcular velocidad base y avanzar progreso (70% velocidad + 30% stamina)
			vel_base = (uma['velocidad'] * 0.7 + uma['stamina'] * 0.3) / 10
			simulacion.progreso[idx] += vel_base
			
			# Activar habilidad si cumple condiciones (no está en cooldown, tiene inteligencia suficiente)
			if filas_umas[idx]['skill_timer'] == 0:
				if RaceEngine.puede_activar_habilidad(simulacion.tick, uma['inteligencia']) and uma['habilidades']:
					hab_idx = random.randint(0, len(uma['habilidades']) - 1)
					habilidad = uma['habilidades'][hab_idx]
					
					# Limitar a 4 activaciones por habilidad en toda la carrera
					if habilidad not in habilidades_count:
						habilidades_count[habilidad] = 0
					
					# Solo activar si no hemos llegado a 4 activaciones de este tipo
					if habilidades_count[habilidad] < 4:
						filas_umas[idx]['skill_timer'] = 30
						filas_umas[idx]['skill_text'].value = f"¡{habilidad}!"
						habilidades_count[habilidad] += 1
						
						# Aplicar bonus
						uma_temp = RaceEngine.aplicar_habilidad(uma, hab_idx, fase)
						uma['velocidad'] = uma_temp['velocidad']
						uma['stamina'] = uma_temp['stamina']
						uma['poder'] = uma_temp['poder']
			
			# Actualizar animación cada 5 ticks
			if simulacion.tick % 5 == 0:
				filas_umas[idx]['frame'] = (filas_umas[idx]['frame'] + 1) % 2
				
				if filas_umas[idx]['skill_timer'] > 0:
					filas_umas[idx]['img'].src = f"assets/Umascorriendo/{filas_umas[idx]['uma_asset_name']}skill.png"
				else:
					estado = "corriendo" if filas_umas[idx]['frame'] == 0 else "corriendo2"
					filas_umas[idx]['img'].src = f"assets/Umascorriendo/{filas_umas[idx]['uma_asset_name']}{estado}.png"
			
			# Actualizar timer de skill
			if filas_umas[idx]['skill_timer'] > 0:
				filas_umas[idx]['skill_timer'] -= 1
			else:
				filas_umas[idx]['skill_text'].value = ""
			
			# Actualizar barra
			progreso_pct = min(simulacion.progreso[idx] / distancia, 1.0)
			filas_umas[idx]['barra'].value = progreso_pct
			
			# Actualizar texto de distancia
			filas_umas[idx]['distancia_text'].value = f"{int(simulacion.progreso[idx])} / {distancia}"
		
		# Actualizar contador
		minutos = simulacion.tiempo // 60
		segundos = simulacion.tiempo % 60
		contador_tiempo.value = f"{minutos:02d}:{segundos:02d}"
		
		# Actualizar fase
		texto_fase.value = {
			'early': 'Early Race',
			'mid': 'Mid Race',
			'late': 'Late Race'
		}.get(fase, 'Early Race')
		
		simulacion.tiempo += 1
		page.update()
		await asyncio.sleep(0.1)
	
	# Mostrar resultados
	await mostrar_resultados(page, simulacion, todas_umas, volver_callback)


async def mostrar_resultados(page: ft.Page, simulacion, todas_umas: list, volver_callback):
	"""Muestra los resultados finales de la carrera."""
	page.clean()
	
	# Obtener datos de usuario y carrera
	user_id = page.current_user.get('id')
	carrera_id = page.current_user.get('carrera_id_bd')
	
	# Ordenar por tiempo de llegada y filtrar solo umas que terminaron
	# Si alguna no terminó, mostrarla al final con DNF
	posiciones = sorted(
		[(idx, tiempo) for idx, tiempo in simulacion.tiempo_llegada.items()],
		key=lambda x: (x[1] is None, x[1] if x[1] is not None else float('inf'))
	)
	
	resultado_col = ft.Column([
		ft.Text("🏁 RESULTADOS 🏁", size=32, weight="bold", color="#744BB1", text_align="center"),
		ft.Divider(height=15, color="#E6C9F5"),
	], spacing=12)
	
	for lugar, (idx, tiempo_llegada) in enumerate(posiciones, 1):
		uma = todas_umas[idx]
		es_jugador = (idx == 0)
		
		medalla = ["🥇", "🥈", "🥉", "4º", "5º"][min(lugar - 1, 4)]
		color = "#E438AB" if es_jugador else "#B814CE"
		
		# Convertir tiempo a formato mm:ss o mostrar DNF
		if tiempo_llegada is not None:
			minutos = tiempo_llegada // 60
			segundos = tiempo_llegada % 60
			tiempo_str = f"{minutos:02d}:{segundos:02d}"
		else:
			tiempo_str = "DNF"
		
		# Destacar al jugador
		bgcolor_item = "#FFE6F7" if es_jugador else "#F5E6FF"
		border_color = "#E438AB" if es_jugador else "#B814CE"
		
		resultado_col.controls.append(
			ft.Container(
				content=ft.Container(
					content=ft.Row([
						ft.Text(medalla, size=32, weight="bold"),
						ft.Text(f"{lugar}. {uma['label']}", size=18, weight="bold", color=color, expand=True),
						ft.Text(tiempo_str, size=16, weight="bold", color="#744BB1"),
					], spacing=20, alignment="space-between"),
					padding=15,
					bgcolor=bgcolor_item,
					border_radius=8,
				),
				bgcolor=border_color,
				border_radius=8,
				padding=2,
			)
		)
		
		# Guardar resultado en BD (solo si terminó y es el jugador)
		if user_id and carrera_id and tiempo_llegada is not None and es_jugador:
			uma_id = page.current_user.get('uma_id_bd')
			if uma_id:
				habilidades = uma.get('habilidades', [])
				guardar_resultado(user_id, carrera_id, uma_id, lugar, tiempo_llegada, habilidades)
	
	resultado_col.controls.append(ft.Divider(height=15, color="#E6C9F5"))
	resultado_col.controls.append(
		ft.Row([
			ft.Button("Volver a Carreras", on_click=volver_callback, bgcolor="#744BB1", color="white", width=200, height=45),
		], alignment="center")
	)
	
	page.add(resultado_col)
	page.update()
