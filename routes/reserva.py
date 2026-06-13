from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required, get_jwt
from routes.auth_roles import admin_required

res = Blueprint("res", __name__)

@res.route("/reservas", methods=["GET"])
@jwt_required()
def listar():
    claims = get_jwt()
    con = conectar()
    cur = con.cursor(dictionary=True)
    # Admin ve todas; docente/estudiante solo las suyas
    if claims.get("rol") == "ADMIN":
        cur.execute("""
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
        """)
    else:
        from flask_jwt_extended import get_jwt_identity
        uid = get_jwt_identity()
        cur.execute("""
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
            WHERE r.usuario_id = %s
        """, (uid,))
    datos = cur.fetchall()
    con.close()
    # Convertir fechas a string
    for d in datos:
        if d.get("fecha"):
            d["fecha"] = str(d["fecha"])
        if d.get("hora_inicio"):
            d["hora_inicio"] = str(d["hora_inicio"])
        if d.get("hora_fin"):
            d["hora_fin"] = str(d["hora_fin"])
    return jsonify(datos)

@res.route("/reservas/por-fecha", methods=["GET"])
@jwt_required()
def por_fecha():
    """Consulta personalizada: reservas de una fecha específica"""
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"mensaje": "Parámetro 'fecha' requerido"}), 400
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
        FROM reserva r
        JOIN usuario u ON r.usuario_id = u.id
        JOIN laboratorio l ON r.laboratorio_id = l.id
        WHERE r.fecha = %s
    """, (fecha,))
    datos = cur.fetchall()
    con.close()
    for d in datos:
        d["fecha"] = str(d["fecha"])
        d["hora_inicio"] = str(d["hora_inicio"])
        d["hora_fin"] = str(d["hora_fin"])
    return jsonify(datos)

@res.route("/reservas/<int:id>", methods=["GET"])
@jwt_required()
def obtener(id):
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM reserva WHERE id=%s", (id,))
    dato = cur.fetchone()
    con.close()
    if not dato:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404
    dato["fecha"] = str(dato["fecha"])
    dato["hora_inicio"] = str(dato["hora_inicio"])
    dato["hora_fin"] = str(dato["hora_fin"])
    return jsonify(dato)

@res.route("/reservas", methods=["POST"])
@jwt_required()
def crear():
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO reserva(fecha, hora_inicio, hora_fin, motivo, estado, usuario_id, laboratorio_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",
        (datos["fecha"], datos["hora_inicio"], datos["hora_fin"],
         datos["motivo"], datos.get("estado", "PENDIENTE"),
         datos["usuario_id"], datos["laboratorio_id"])
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Reserva creada"}), 201

@res.route("/reservas/<int:id>", methods=["PUT"])
@admin_required
def actualizar(id):
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE reserva SET fecha=%s, hora_inicio=%s, hora_fin=%s, motivo=%s, estado=%s, usuario_id=%s, laboratorio_id=%s WHERE id=%s",
        (datos["fecha"], datos["hora_inicio"], datos["hora_fin"],
         datos["motivo"], datos["estado"], datos["usuario_id"],
         datos["laboratorio_id"], id)
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Reserva actualizada"})

@res.route("/reservas/<int:id>", methods=["DELETE"])
@admin_required
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM reserva WHERE id=%s", (id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Reserva eliminada"})