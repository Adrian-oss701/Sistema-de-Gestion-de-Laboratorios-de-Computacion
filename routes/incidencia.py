from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from routes.auth_roles import admin_required

inc = Blueprint("inc", __name__)

@inc.route("/incidencias", methods=["GET"])
@jwt_required()
def listar():
    claims = get_jwt()
    uid = get_jwt_identity()
    con = conectar()
    cur = con.cursor(dictionary=True)

    if claims.get("rol") == "ADMIN":
        cur.execute("""
            SELECT i.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM incidencia i
            JOIN usuario u ON i.usuario_id = u.id
            JOIN laboratorio l ON i.laboratorio_id = l.id
            ORDER BY i.id DESC
        """)
    else:
        cur.execute("""
            SELECT i.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM incidencia i
            JOIN usuario u ON i.usuario_id = u.id
            JOIN laboratorio l ON i.laboratorio_id = l.id
            WHERE i.usuario_id = %s
            ORDER BY i.id DESC
        """, (uid,))
        
    datos = cur.fetchall()
    con.close()
    for d in datos:
        if d.get("fecha"):
            d["fecha"] = str(d["fecha"])
    return jsonify(datos)

@inc.route("/incidencias/por-fecha", methods=["GET"])
@jwt_required()
def por_fecha():
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"mensaje": "Parámetro 'fecha' requerido"}), 400
        
    claims = get_jwt()
    uid = get_jwt_identity()
    con = conectar()
    cur = con.cursor(dictionary=True)

    if claims.get("rol") == "ADMIN":
        cur.execute("""
            SELECT i.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM incidencia i
            JOIN usuario u ON i.usuario_id = u.id
            JOIN laboratorio l ON i.laboratorio_id = l.id
            WHERE DATE(i.fecha) = %s
            ORDER BY i.id DESC
        """, (fecha,))
    else:
        cur.execute("""
            SELECT i.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM incidencia i
            JOIN usuario u ON i.usuario_id = u.id
            JOIN laboratorio l ON i.laboratorio_id = l.id
            WHERE DATE(i.fecha) = %s AND i.usuario_id = %s
            ORDER BY i.id DESC
        """, (fecha, uid))
        
    datos = cur.fetchall()
    con.close()
    for d in datos:
        if d.get("fecha"):
            d["fecha"] = str(d["fecha"])
    return jsonify(datos)

@inc.route("/incidencias", methods=["POST"])
@jwt_required()
def crear():
    datos = request.get_json()
    identity = get_jwt_identity()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO incidencia(descripcion, prioridad, estado, usuario_id, laboratorio_id) VALUES(%s,%s,%s,%s,%s)",
        (datos["descripcion"], datos.get("prioridad", "MEDIA"), "ABIERTA", identity, datos["laboratorio_id"])
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Incidencia reportada"}), 201

@inc.route("/incidencias/<int:id>", methods=["PUT"])
@admin_required
def actualizar(id):
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE incidencia SET descripcion=%s, prioridad=%s, estado=%s, laboratorio_id=%s WHERE id=%s",
        (datos["descripcion"], datos["prioridad"], datos["estado"], datos["laboratorio_id"], id)
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