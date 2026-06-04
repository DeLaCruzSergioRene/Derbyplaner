import flet as ft
from models.game_model import obtener_umas_competencia
from models.creacion_model import get_uma_label

def preparar_datos_juego(page: ft.Page):
    """
    Prepara los datos necesarios para la vista del juego.
    Retorna un dict con:
    - uma_seleccionada: dict con la uma elegida por el jugador
    - umas_competidoras: list de 4 umas generadas aleatoriamente
    - carrera: dict con info de la carrera
    """
    creacion = page.current_user.get('creacion', {})
    uma_seleccionada_img = creacion.get('uma', 'Air_Grove.png')
    
    # Preparar datos de la uma seleccionada
    uma_seleccionada = {
        'uma': uma_seleccionada_img,
        'label': get_uma_label(uma_seleccionada_img),
        'velocidad': creacion.get('velocidad', 0),
        'stamina': creacion.get('stamina', 0),
        'poder': creacion.get('poder', 0),
        'inteligencia': creacion.get('inteligencia', 0),
        'terreno': creacion.get('terreno', 'Pasto'),
        'habilidades': creacion.get('habilidades', []),
    }
    
    # Generar umas competidoras
    umas_competidoras = obtener_umas_competencia(uma_seleccionada_img, cantidad=4)
    
    carrera = page.current_user.get('carrera', {})
    
    return {
        'uma_seleccionada': uma_seleccionada,
        'umas_competidoras': umas_competidoras,
        'carrera': carrera,
    }
