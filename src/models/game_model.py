import random
from models.seleccion_model import UMAS
from models.creacion_model import HABILIDADES, get_uma_label

def generar_stats_aleatorios():
    # Genera stats aleatorios para una uma competidora.
    return {
        'velocidad': random.randint(200, 1000),
        'stamina': random.randint(200, 1000),
        'poder': random.randint(250, 1000),
        'inteligencia': random.randint(250, 1000),
    }

def generar_habilidades_aleatorias():
    # Genera entre 1 y 3 habilidades aleatorias.
    todas_habilidades = []
    for tipo in HABILIDADES.values():
        todas_habilidades.extend(tipo)
    
    cantidad = random.randint(1, 3)
    return random.sample(todas_habilidades, cantidad)

def generar_uma_competidora(uma_excluida: str):
    # Genera una uma competidora aleatoria (no puede ser la uma_excluida).
    umas_disponibles = [u for u in UMAS if u != uma_excluida]
    uma_img = random.choice(umas_disponibles)
    
    return {
        'uma': uma_img,
        'label': get_uma_label(uma_img),
        'velocidad': generar_stats_aleatorios()['velocidad'],
        'stamina': generar_stats_aleatorios()['stamina'],
        'poder': generar_stats_aleatorios()['poder'],
        'inteligencia': generar_stats_aleatorios()['inteligencia'],
        'terreno': random.choice(['Pasto', 'Tierra']),
        'habilidades': generar_habilidades_aleatorias(),
    }

def obtener_umas_competencia(uma_excluida: str, cantidad: int = 4):
    # Genera un número específico de umas competidoras únicas.
    umas_competidoras = []
    umas_generadas = set()
    
    while len(umas_competidoras) < cantidad:
        uma = generar_uma_competidora(uma_excluida)
        if uma['uma'] not in umas_generadas:
            umas_generadas.add(uma['uma'])
            umas_competidoras.append(uma)
    
    return umas_competidoras
