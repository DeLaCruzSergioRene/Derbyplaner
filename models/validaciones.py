import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validar_no_vacio(*campos):
    """Devuelve (True, '') si todos los campos no están vacíos."""
    for c in campos:
        if not c or not str(c).strip():
            return False, "Completa todos los campos"
    return True, ""

def validar_email(email: str):
    if not EMAIL_RE.match(email or ""):
        return False, "Correo inválido"
    return True, ""

def validar_contrasena(pw: str, minimo: int = 8):
    if not pw or len(pw) < minimo:
        return False, f"La contraseña debe tener al menos {minimo} caracteres"
    return True, ""

def validar_caracteres(nombre: str, permitido=r"^[\w\s\-áéíóúÁÉÍÓÚñÑ]+$"):
    if not re.match(permitido, nombre or ""):
        return False, "Caracteres no permitidos"
    return True, ""
