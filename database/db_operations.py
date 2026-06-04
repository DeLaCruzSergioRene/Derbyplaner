# Operaciones de BD específicas para el juego Derby Planer.
from database.db import BD


def guardar_uma_creada(user_id, config_uma):
	# Guarda una uma creada en la BD. Args: user_id: ID del usuario, config_uma: dict con {uma, label, velocidad, stamina, poder, inteligencia, terreno, habilidades}
	# Returns: int: ID de la uma creada, o None si falla
	try:
		bd = BD()
		
		# Insertar en tabla umas (sin estilo ya que no lo usamos)
		consulta_umas = "INSERT INTO umas (user_id, nombre, suelo_fav, imagen) VALUES (%s, %s, %s, %s)"
		parametros_umas = (
			user_id,
			config_uma.get('label', 'Uma Sin Nombre'),
			config_uma.get('terreno', 'Pasto'),
			config_uma.get('uma', '')
		)
		bd.ejecutar(consulta_umas, parametros_umas)
		
		# Obtener ID de la uma insertada
		consulta_obtener_id = "SELECT LAST_INSERT_ID() as id"
		resultado = bd.obtener_uno(consulta_obtener_id)
		uma_id = resultado['id'] if resultado else None
		
		if not uma_id:
			return None
		
		# Guardar estadísticas de la uma (velocidad, stamina, poder, inteligencia)
		consulta_stats = "INSERT INTO stats (uma_id, vel, sta, pwr, intel) VALUES (%s, %s, %s, %s, %s)"
		parametros_stats = (
			uma_id,
			int(config_uma.get('velocidad', 0)),
			int(config_uma.get('stamina', 0)),
			int(config_uma.get('poder', 0)),
			int(config_uma.get('inteligencia', 0))
		)
		bd.ejecutar(consulta_stats, parametros_stats)
		
		# Vincular habilidades seleccionadas a esta uma
		habilidades = config_uma.get('habilidades', [])
		for hab_nombre in habilidades:
			# Buscar ID de la habilidad en tabla habilidades
			consulta_hab_id = "SELECT id FROM habilidades WHERE nombre = %s"
			resultado_hab = bd.obtener_uno(consulta_hab_id, (hab_nombre,))
			if resultado_hab:
				hab_id = resultado_hab['id']
				# Insertar relación uma-habilidad
				consulta_uma_habs = "INSERT INTO uma_habs (uma_id, hab_id) VALUES (%s, %s)"
				bd.ejecutar(consulta_uma_habs, (uma_id, hab_id))
		
		bd.cerrar()
		return uma_id
		
	except Exception as e:
		print(f"Error guardando uma: {e}")
		return None


def guardar_carrera(distancia, terreno, nombre="Carrera"):
	# Guarda una carrera en la BD. Args: distancia: int (ej: 2000), terreno: str (ej: "Pasto", "Tierra"), nombre: str (nombre de la carrera)
	# Returns: int: ID de la carrera creada, o None si falla
	
	try:
		bd = BD()
		
		# Insertar nueva carrera con distancia y terreno
		consulta = "INSERT INTO carreras (dist, terreno) VALUES (%s, %s)"
		parametros = (distancia, terreno)
		bd.ejecutar(consulta, parametros)
		
		# Recuperar el ID de la carrera recién insertada
		consulta_obtener_id = "SELECT LAST_INSERT_ID() as id"
		resultado = bd.obtener_uno(consulta_obtener_id)
		carrera_id = resultado['id'] if resultado else None
		
		bd.cerrar()
		return carrera_id
		
	except Exception as e:
		print(f"Error guardando carrera: {e}")
		return None


def guardar_resultado(user_id, carrera_id, uma_id, posicion, tiempo_llegada, habilidades):
	# Guarda el resultado de una carrera en la BD. Args: user_id: ID del usuario, carrera_id: ID de la carrera uma_id: ID de la uma que participó, posicion: int (1, 2, 3, 4, 5), tiempo_llegada: int (ticks totales hasta terminar), habilidades: list de str (nombres de habilidades usadas)
	# Returns: int: ID del resultado, o None si falla
	
	try:
		bd = BD()
		
		# Mapear nombres de habilidades a sus IDs en la BD
		hab_ids = [None, None, None]
		for idx, hab_nombre in enumerate(habilidades[:3]):
			consulta = "SELECT id FROM habilidades WHERE nombre = %s"
			resultado = bd.obtener_uno(consulta, (hab_nombre,))
			if resultado:
				hab_ids[idx] = resultado['id']
		
		# Registrar resultado de la carrera con posición, tiempo y habilidades
		consulta = """
		INSERT INTO resultados (user_id, race_id, uma_id, posicion, tiempo, habilidad_1, habilidad_2, habilidad_3)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
		"""
		parametros = (
			user_id,
			carrera_id,
			uma_id,
			posicion,
			tiempo_llegada,
			hab_ids[0],
			hab_ids[1],
			hab_ids[2]
		)
		bd.ejecutar(consulta, parametros)
		
		# Obtener ID del resultado insertado
		consulta_obtener_id = "SELECT LAST_INSERT_ID() as id"
		resultado = bd.obtener_uno(consulta_obtener_id)
		resultado_id = resultado['id'] if resultado else None
		
		bd.cerrar()
		return resultado_id
		
	except Exception as e:
		print(f"Error guardando resultado: {e}")
		return None


def obtener_umas_usuario(user_id):
	# Obtiene todas las umas creadas por un usuario.
	#Returns: list: Lista de dicts con info de umas
	
	try:
		bd = BD()
		consulta = "SELECT * FROM umas WHERE user_id = %s"
		resultados = bd.obtener_todos(consulta, (user_id,))
		bd.cerrar()
		return resultados if resultados else []
	except Exception as e:
		print(f"Error obteniendo umas: {e}")
		return []


def obtener_resultados_usuario(user_id):
	# Obtiene todos los resultados de carreras de un usuario.
	# Returns: list: Lista de dicts con resultados
	
	try:
		bd = BD()
		consulta = """
		SELECT r.*, u.nombre, c.dist, c.terreno 
		FROM resultados r
		JOIN umas u ON r.uma_id = u.id
		JOIN carreras c ON r.race_id = c.id
		WHERE r.user_id = %s
		ORDER BY r.fecha DESC
		"""
		resultados = bd.obtener_todos(consulta, (user_id,))
		bd.cerrar()
		return resultados if resultados else []
	except Exception as e:
		print(f"Error obteniendo resultados: {e}")
		return []
