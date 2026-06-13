from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required
from routes.auth_roles import admin_required

inc = Blueprint("inc", __name__)

@inc.route("/incidencias", methods=["GET"])
@jwt_required()
def listar():
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT i.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
        FROM incidencia i
        JOIN usuario u ON i.usuario_id = u.id
        JOIN laboratorio l ON i.laboratorio_id = l.id
    """)
    datos = cur.fetchall()
    con.close()
    for d in datos:
        if d.get("fecha"):
            d["fecha"] = str(d["fecha"])
    return jsonify(datos)

@inc.route("/incidencias/<int:id>", methods=["GET"])
@jwt_required()
def obtener(id):
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM incidencia WHERE id=%s", (id,))
    dato = cur.fetchone()
    con.close()
    if not dato:
        return jsonify({"mensaje": "Incidencia no encontrada"}), 404
    if dato.get("fecha"):
        dato["fecha"] = str(dato["fecha"])
    return jsonify(dato)

@inc.route("/incidencias", methods=["POST"])
@jwt_required()
def crear():
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO incidencia(descripcion, prioridad, estado, usuario_id, laboratorio_id) VALUES(%s,%s,%s,%s,%s)",
        (datos["descripcion"], datos.get("prioridad", "MEDIA"),
         datos.get("estado", "ABIERTA"), datos["usuario_id"], datos["laboratorio_id"])
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Incidencia creada"}), 201

@inc.route("/incidencias/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar(id):
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE incidencia SET descripcion=%s, prioridad=%s, estado=%s, usuario_id=%s, laboratorio_id=%s WHERE id=%s",
        (datos["descripcion"], datos["prioridad"], datos["estado"],
         datos["usuario_id"], datos["laboratorio_id"], id)
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Incidencia actualizada"})

@inc.route("/incidencias/<int:id>", methods=["DELETE"])
@admin_required
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM incidencia WHERE id=%s", (id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Incidencia eliminada"})