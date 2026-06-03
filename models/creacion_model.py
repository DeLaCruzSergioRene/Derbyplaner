# Modelo de datos y utilidades para la creación de una 'uma'. Este módulo contiene constantes y helpers ligeros usados por la vista/controlador de creación. 
# Habilidades agrupadas por tipo. Fácil de extender con nuevas entradas.
HABILIDADES = {
    "Velocidad": ["Sprint Boost", "Aceleración", "Velocidad Máxima", "Salida Rápida"],
    "Poder": ["Arrancada Fuerte", "Salto Poderoso", "Empuje Final", "Resistencia Bruta"],
    "Recuperación": ["Segundo Aire", "Resistencia", "Recuperación", "Defensa"],
}


def get_uma_label(filename: str) -> str:
    # Convierte el nombre de archivo en una etiqueta legible. Ejemplo: 'Air_Grove.png' -> 'Air Grove'
    return filename.replace("_", " ").replace(".png", "")

def obtener_habilidades_seleccionadas(seleccion: dict) -> list:
    # Devuelve la lista de habilidades seleccionadas desde los checkboxes. `seleccion` es un dict con nombre->Checkbox; se examina `.value`.
    return [habilidad for habilidad, cb in seleccion.items() if cb.value]


def construir_configuracion(uma_img: str, velocidad: int, stamina: int, poder: int, inteligencia: int, terreno: str, habilidades: list, max_habilidades: int = 3) -> dict:
    # Construye y valida la configuración final de la creación. Lanza `ValueError` si se excede el máximo de habilidades permitidas.
    if len(habilidades) > max_habilidades:
        raise ValueError(f"Solo puedes seleccionar hasta {max_habilidades} habilidades")

    return {
        'uma': uma_img,
        'velocidad': velocidad,
        'stamina': stamina,
        'poder': poder,
        'inteligencia': inteligencia,
        'terreno': terreno,
        'habilidades': habilidades,
    }
