from models.validaciones import (
    validar_no_vacio,
    validar_email,
    validar_contrasena,
    validar_caracteres,
    validar_longitud_nombre,
)

def validar_datos_registro(nombre, email, contraseña):
    ok, msg = validar_no_vacio(nombre, email, contraseña)
    if not ok:
        return False, msg
    ok, msg = validar_longitud_nombre(nombre)
    if not ok:
        return False, msg
    ok, msg = validar_caracteres(nombre)
    if not ok:
        return False, msg
    ok, msg = validar_email(email)
    if not ok:
        return False, msg
    ok, msg = validar_contrasena(contraseña)
    if not ok:
        return False, msg
    return True, ""

def validar_datos_sesion(email, contraseña):
    ok, msg = validar_no_vacio(email, contraseña)
    if not ok:
        return False, msg
    ok, msg = validar_email(email)
    if not ok:
        return False, msg
    return True, ""
