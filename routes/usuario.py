from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required
from routes.auth_roles import admin_required

usu = Blueprint("usu", __name__)

@usu.route("/usuarios", methods=["GET"])
@admin_required
def listar():
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT id, nombre, correo, rol FROM usuario")
    datos = cur.fetchall()
    con.close()
    return jsonify(datos)

@usu.route("/usuarios/<int:id>", methods=["GET"])
@admin_required
def obtener(id):
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT id, nombre, correo, rol FROM usuario WHERE id=%s", (id,))
    dato = cur.fetchone()
    con.close()
    if not dato:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    return jsonify(dato)

@usu.route("/usuarios", methods=["POST"])
@admin_required
def crear():
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO usuario(nombre, correo, password, rol) VALUES(%s,%s,%s,%s)",
        (datos["nombre"], datos["correo"], datos["password"], datos["rol"])
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Usuario creado"}), 201

@usu.route("/usuarios/<int:id>", methods=["PUT"])
@admin_required
def actualizar(id):
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE usuario SET nombre=%s, correo=%s, password=%s, rol=%s WHERE id=%s",
        (datos["nombre"], datos["correo"], datos["password"], datos["rol"], id)
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Usuario actualizado"})

@usu.route("/usuarios/<int:id>", methods=["DELETE"])
@admin_required
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Usuario eliminado"})