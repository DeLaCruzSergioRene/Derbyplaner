import random

# Motor de cálculos para la carrera: desgaste, habilidades, velocidad, terreno
class RaceEngine:
    
    # Desgaste de stats por fase de carrera (early/mid/late aumenta dificultad)
    FATIGA_BASE = {
        'early': {'velocidad': 1.4, 'stamina': 1.4, 'poder': 1.4},
        'mid': {'velocidad': 1.7, 'stamina': 1.8, 'poder': 1.9},
        'late': {'velocidad': 2.1, 'stamina': 2.2, 'poder': 2.4}
    }
    
    # Bonificadores por terreno si es preferido por la uma (0.8 = buen rendimiento y menor desgaste, 1.2 = mal rendimiento y mas desgaste)
    TERRENO_BONUS = {
        'pasto': 0.8,
        'tierra': 0.8
    }
    
    @staticmethod
    def calcular_desgaste(uma: dict, fase: str, terreno_carrera: str = None) -> dict:
        # Calcula desgaste según fase, inteligencia/poder (reducen) y compatibilidad de terreno
        # Se usa `.copy()` para no modificar la constante `FATIGA_BASE` global.
        fatiga = RaceEngine.FATIGA_BASE[fase].copy()
        inteligencia = uma['inteligencia']
        poder = uma['poder']
        terreno_favorito = uma['terreno']
        
        # Si no hay terreno de carrera especificado, asumir que es igual al favorito
        if terreno_carrera is None:
            terreno_carrera = terreno_favorito
        
        # Normalizar nombres de terreno para comparación
        terreno_fav_norm = terreno_favorito.lower().replace('á', 'a')
        terreno_carr_norm = terreno_carrera.lower().replace('á', 'a')
        
        # Calcular multiplicador de terreno usando TERRENO_BONUS
        terreno_multiplier = 1.0
        if terreno_fav_norm == terreno_carr_norm:
            terreno_multiplier = RaceEngine.TERRENO_BONUS.get(terreno_fav_norm, 1.0)
        else:
            # Si no coincide, penalty: 1.2x desgaste
            terreno_multiplier = 1.2
        
        # Reducción de desgaste: inteligencia (hasta 30%) + poder (hasta 40%)
        reduccion_inteligencia = min(0.3, inteligencia / 3333)
        reduccion_poder = min(0.4, poder / 2500)
        reduccion_total = min(1.0, reduccion_inteligencia + reduccion_poder)
        
        for stat in fatiga:
            desgaste = fatiga[stat] * (1 - reduccion_total)
            desgaste *= terreno_multiplier
            fatiga[stat] = max(0, int(desgaste))
        
        return fatiga
    
    @staticmethod
    def puede_activar_habilidad(tick: int, inteligencia: int) -> bool:
        # Determina si una habilidad puede activarse en este tick
        # Intervalo más corto: se puede activar cada 15-20 ticks
        # `intervalo` controla cada cuantos ticks se puede intentar activar.
        intervalo = max(15, 20 - inteligencia // 50)  # Con inteligencia 1000: max(15, 20-20) = 15

        # `probabilidad` es la probabilidad de activación (0.0-1.0).
        # A mayor inteligencia, mayor probabilidad (1000 => 1.0)
        probabilidad = min(1.0, inteligencia / 1000)
        
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
        # (se revisan palabras clave en el nombre de la habilidad).
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
        return (velocidad * 0.7 + stamina * 0.3) / 20
