

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt



#manejo de roles
ADMINISTRADOR ="Administrador"
GENERAL = "General"


def rol_requerido(rol):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Verifica el token JWT
                verify_jwt_in_request()
                claims = get_jwt()
                rol_usuario = claims.get("rol")

                # Verifica si el rol existe
                if rol_usuario is None:
                    return {"message": "Acceso denegado: Rol no definido"}, 403
                
                # Verifica permisos
                if rol != rol_usuario:
                    return {"message": "Acceso denegado: Tu usuario no tiene los permisos necesarios para realizar esta acción"}, 403
                
                # Llama la función decorada
                return func(*args, **kwargs)
            except Exception as e:
                # Manejo de errores
                return {"error": str(e)}, 500
        return wrapper
    return decorator