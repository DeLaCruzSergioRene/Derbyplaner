from models.race_engine_model import RaceEngine

class RaceSimulation:
	# Simula una carrera completa.
	
	def __init__(self, umas: list, distancia: int):
		# Inicializa la simulación. umas: lista de dicts con stats de umas, distancia: distancia en metros
		
		self.umas = [uma.copy() for uma in umas]
		self.distancia = distancia
		self.fases = ['early', 'mid', 'late']
		self.distancia_por_fase = distancia / 3
		
		# Tracking de simulación
		self.progreso = {i: 0.0 for i in range(len(umas))}
		self.tiempo = 0
		self.habilidades_activadas = {i: [] for i in range(len(umas))}
		self.habilidades_count = {i: 0 for i in range(len(umas))}  # Contar activaciones
		self.tiempo_llegada = {i: None for i in range(len(umas))}  # Trackear cuando cruzan meta
		self.tick = 0
	
	def _get_fase_actual(self) -> str:
		# Retorna la fase según el progreso promedio.
		progreso_promedio = sum(self.progreso.values()) / len(self.progreso)
		
		if progreso_promedio < self.distancia_por_fase:
			return 'early'
		elif progreso_promedio < self.distancia_por_fase * 2:
			return 'mid'
		else:
			return 'late'
	
	def _carrera_terminada(self) -> bool:
		# Verifica si la carrera terminó.
		# Termina si todas llegan, O si pasaron 150 segundos máximo (para no esperar infinito)
		todas_llegaron = all(prog >= self.distancia for prog in self.progreso.values())
		tiempo_maximo_excedido = self.tiempo >= 150
		
		return todas_llegaron or tiempo_maximo_excedido
