import random

# Motor de cálculos para la carrera: desgaste, habilidades, velocidad, terreno
class RaceEngine:
    
    # Desgaste de stats por fase de carrera (early/mid/late aumenta dificultad)
    FATIGA_BASE = {
        'early': {'velocidad': 0.05, 'stamina': 0.05, 'poder': 0.05},
        'mid': {'velocidad': 0.05, 'stamina': 0.1, 'poder': 0.05},
        'late': {'velocidad': 0.1, 'stamina': 0.1, 'poder': 0.1}
    }
    
    # Bonificadores por terreno (afectan especialmente el poder)
    TERRENO_BONUS = {
        'turf': 1.0,
        'dirt': 1.3,
        'synthetic': 1.1
    }
    
    @staticmethod
    def calcular_desgaste(uma: dict, fase: str) -> dict:
        # Calcula desgaste según fase, inteligencia (reduce hasta 70%) y terreno
        fatiga = RaceEngine.FATIGA_BASE[fase].copy()
        inteligencia = uma['inteligencia']
        terreno = uma['terreno']
        
        # Reducir desgaste según inteligencia (máximo 70% de reducción)
        reduccion_inteligencia = min(0.7, inteligencia / 1428.57)  # 1000 * 0.7 / 1000 = máx 70%
        
        for stat in fatiga:
            desgaste = fatiga[stat] * (1 - reduccion_inteligencia)
            
            # Terreno afecta poder
            if stat == 'poder':
                desgaste *= RaceEngine.TERRENO_BONUS.get(terreno, 1.0)
            
            fatiga[stat] = max(0, int(desgaste))
        
        return fatiga
    
    @staticmethod
    def puede_activar_habilidad(tick: int, inteligencia: int) -> bool:
        # Determina si una habilidad puede activarse en este tick. Solo se puede activar cada 50 ticks aproximadamente.
        
        # Intervalo base es 50 ticks
        intervalo = max(30, 50 - inteligencia // 50)  # Inteligencia reduce el intervalo
        
        # Probabilidad de activación en el momento correcto
        probabilidad = 0.3 + (inteligencia / 3333)  # Máx 0.6
        
        return (tick % intervalo == 0) and (random.random() < probabilidad)
    
    @staticmethod
    def aplicar_habilidad(uma: dict, habilidad_idx: int, fase: str) -> dict:
        # Aplica el bonus de una habilidad. Retorna los stats modificados.
        if not uma['habilidades'] or habilidad_idx >= len(uma['habilidades']):
            return uma.copy()
        
        stats_modificados = uma.copy()
        
        # Bonuses por tipo de habilidad y fase
        bonuses = {
            'velocidad': {'early': 40, 'mid': 50, 'late': 50},
            'stamina': {'early': 60, 'mid': 70, 'late': 80},
            'poder': {'early': 50, 'mid': 60, 'late': 70},
        }
        
        # Obtener nombre de habilidad
        habilidad = uma['habilidades'][habilidad_idx % len(uma['habilidades'])]
        
        # Mapear habilidad a tipo de stat basado en palabras clave
        tipo_stat = 'poder'  # default
        habilidad_lower = habilidad.lower()
        
        if any(palabra in habilidad_lower for palabra in ['veloc', 'speed', 'sprint', 'aceler', 'salida', 'boost']):
            tipo_stat = 'velocidad'
        elif any(palabra in habilidad_lower for palabra in ['stamina', 'resistencia', 'aire', 'segundo', 'defensa', 'recuper']):
            tipo_stat = 'stamina'
        elif any(palabra in habilidad_lower for palabra in ['salto', 'poder', 'arranc', 'empuje', 'fuerte', 'bruta']):
            tipo_stat = 'poder'
        
        bonus = bonuses.get(tipo_stat, {}).get(fase, 30)
        
        # Aplicar bonus al stat correspondiente
        stats_modificados[tipo_stat] = min(1000, stats_modificados[tipo_stat] + bonus)
        
        return stats_modificados
    
    @staticmethod
    def calcular_velocidad_fase(uma: dict) -> float:
        # Calcula velocidad base de la uma (progreso por tick). Basado en velocidad y stamina.
        velocidad = uma['velocidad']
        stamina = uma['stamina']
        
        # Velocidad base: velocidad contribuye más que stamina
        return (velocidad * 0.7 + stamina * 0.3) / 10  # Dividir entre 10 en lugar de 100
