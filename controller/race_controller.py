import random
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
	
	def simular(self) -> dict:
		#Simula la carrera completa. Retorna datos para visualización.
		datos_visual = {
			'progreso_umas': [],
			'eventos': [],  # Habilidades activadas
			'tiempo_carrera': 0,
			'posiciones': []
		}
		
		while not self._carrera_terminada():
			self.tick += 1
			fase_actual = self._get_fase_actual()
			
			# Simular cada uma
			for idx, uma in enumerate(self.umas):
				if self.progreso[idx] >= self.distancia:
					continue
				
				# Velocidad base
				velocidad = RaceEngine.calcular_velocidad_fase(uma)
				
				# Aplicar desgaste
				desgaste = RaceEngine.calcular_desgaste(uma, fase_actual)
				uma['velocidad'] = max(0, uma['velocidad'] - desgaste['velocidad'])
				uma['stamina'] = max(0, uma['stamina'] - desgaste['stamina'])
				uma['poder'] = max(0, uma['poder'] - desgaste['poder'])
				
				# Avanzar progreso
				self.progreso[idx] += velocidad
				
				# Registrar tiempo de llegada si cruza la meta
				if self.progreso[idx] >= self.distancia and self.tiempo_llegada[idx] is None:
					self.tiempo_llegada[idx] = self.tiempo
				
				# Intentar activar habilidad
				if RaceEngine.activar_habilidad(uma, fase_actual):
					habilidad_idx = random.randint(0, len(uma['habilidades']) - 1)
					uma_temp = RaceEngine.aplicar_habilidad(uma, habilidad_idx, fase_actual)
					
					habilidad_nombre = uma['habilidades'][habilidad_idx]
					self.habilidades_activadas[idx].append({
						'fase': fase_actual,
						'habilidad': habilidad_nombre,
						'tick': self.tick
					})
					
					# Aplicar bonus
					uma['velocidad'] = uma_temp['velocidad']
					uma['stamina'] = uma_temp['stamina']
					uma['poder'] = uma_temp['poder']
			
			self.tiempo += 1
		
		# Calcular posiciones finales ordenadas por tiempo de llegada
		posiciones = sorted(
			self.tiempo_llegada.items(),
			key=lambda x: x[1] if x[1] is not None else float('inf')
		)
		
		datos_visual['tiempo_carrera'] = self.tiempo
		datos_visual['posiciones'] = [
			{
				'lugar': i + 1,
				'uma_idx': pos[0],
				'tiempo': pos[1],
				'habilidades': self.habilidades_activadas[pos[0]]
			}
			for i, pos in posiciones
		]
		
		return datos_visual
	
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
		return all(prog >= self.distancia for prog in self.progreso.values())
	
	def get_progreso_actual(self) -> dict:
		# Retorna el progreso actual para visualización en tiempo real.
		return {
			'progreso': self.progreso,
			'tiempo': self.tiempo,
			'fase': self._get_fase_actual(),
			'habilidades': self.habilidades_activadas
		}
