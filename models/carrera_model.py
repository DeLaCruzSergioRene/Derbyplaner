"""Model para manejar la creación de carreras.

Incluye constantes válidas y funciones utilitarias para construir
una carrera y generar un resumen basado en la configuración de
creación de la `uma`.
"""

from models.creacion_model import get_uma_label


# Opciones válidas para distancia y terreno. Usadas por el UI.
DISTANCIAS = ["1200m", "1400m", "1600m", "1800m", "2000m", "2200m", "2400m"]
TERRENOS = ["Pasto", "Tierra"]


def construir_carrera(nombre: str, distancia: int, terreno: str) -> dict:
    """Valida y construye una estructura de carrera lista para guardar.

    - Valida que el `nombre` no esté vacío.
    - Comprueba que `distancia` y `terreno` pertenezcan a las opciones.
    """
    if not nombre or not nombre.strip():
        raise ValueError("El nombre de la carrera no puede quedar vacío")
    if distancia not in DISTANCIAS:
        raise ValueError("Distancia inválida")
    if terreno not in TERRENOS:
        raise ValueError("Terreno inválido")

    return {
        'nombre': nombre.strip(),
        'distancia': distancia,
        'terreno': terreno,
    }


def resumen_creacion(config: dict) -> list:
    """Genera una lista de líneas para mostrar un mini-resumen.

    El resumen extrae campos relevantes de la configuración de creación
    y devuelve una lista de strings para mostrar en la UI.
    """
    if not config:
        return []

    habilidades = config.get('habilidades', [])
    return [
        f"Terreno preferido: {config.get('terreno', 'N/A')}",
        f"Velocidad: {config.get('velocidad', 'N/A')}",
        f"Stamina: {config.get('stamina', 'N/A')}",
        f"Poder: {config.get('poder', 'N/A')}",
        f"Inteligencia: {config.get('inteligencia', 'N/A')}",
        f"Habilidades: {', '.join(habilidades) if habilidades else 'Sin habilidades seleccionadas'}",
    ]


def obtener_nombre_uma(uma_img: str) -> str:
    # Reutiliza el helper del model de creación para obtener la etiqueta.
    return get_uma_label(uma_img)
