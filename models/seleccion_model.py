# Datos y utilidades para la pantalla de selección.
# - `UMAS` es una lista de nombres de archivo (strings) que representan las imágenes
#   disponibles en `assets/umamusumes/`.
# - Esta lista se itera para generar la UI; es un simple contenedor de identificadores.
# Lista de imágenes (identificadores) disponibles en la selección.
UMAS = [
    "Air_Grove.png", "El_Condor_Pasa.png", "Daiwa_Scarlet.png", "GoldShip.png",
    "Grass_Wonder.png", "Kitasan_Black.png", "Manhattan_Cafe.png", "Mejiro_Bright.png",
    "Mejiro_Dober.png", "Mejiro_McQueen.png", "Narita_Brian.png", "Oguri_Cap.png",
    "Silence_Suzuka.png", "Special_Week.png", "Señorita_CB.png", "Still_In_Love.png",
    "Sweep_Tosho.png", "Symboli_Rudolf.png", "Tokai_Teio.png", "Vodka.png"
]

def get_uma_label(filename: str) -> str:
    # Convierte el nombre de archivo en una etiqueta legible para mostrar. Mantiene la UI separada de los nombres de archivo reales.
    return filename.replace("_", " ").replace(".png", "")
