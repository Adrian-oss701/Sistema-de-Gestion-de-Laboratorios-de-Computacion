from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from database import conectar

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    if not datos or not datos.get("correo") or not datos.get("password"):
        return jsonify({"mensaje": "Correo y password requeridos"}), 400

    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM usuario WHERE correo=%s AND password=%s",
        (datos["correo"], datos["password"])
    )
    usuario = cur.fetchone()
    con.close()

    if usuario:
        token = create_access_token(
            identity=str(usuario["id"]),
            additional_claims={
                "rol": usuario["rol"],
                "nombre": usuario["nombre"]
            }
        )
        return jsonify({
            "token": token,
            "rol": usuario["rol"],
            "nombre": usuario["nombre"]
        })

    return jsonify({"mensaje": "Credenciales incorrectas"}), 401