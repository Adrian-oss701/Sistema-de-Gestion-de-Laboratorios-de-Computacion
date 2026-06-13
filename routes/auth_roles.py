import functools
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("rol") != "ADMIN":
            return jsonify({"mensaje": "Acceso denegado. Se requiere rol ADMIN"}), 403
        return fn(*args, **kwargs)
    return wrapper

def roles_required(*roles):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return jsonify({"mensaje": f"Acceso denegado. Roles permitidos: {', '.join(roles)}"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator