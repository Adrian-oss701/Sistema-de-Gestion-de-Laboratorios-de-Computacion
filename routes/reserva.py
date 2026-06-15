import traceback
from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from routes.auth_roles import admin_required

res = Blueprint("res", __name__)

def formatear_hora(hora_str):
    if hora_str and len(hora_str) == 5:
        return f"{hora_str}:00"
    return hora_str

@res.route("/laboratorios/<int:id>/horarios", methods=["GET"])
def ver_horarios(id):
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"mensaje": "Fecha requerida"}), 400

    bloques = [
        {"hora_inicio": "07:00", "hora_fin": "08:30"},
        {"hora_inicio": "08:30", "hora_fin": "10:00"},
        {"hora_inicio": "10:30", "hora_fin": "12:00"},
        {"hora_inicio": "12:00", "hora_fin": "13:30"},
        {"hora_inicio": "14:00", "hora_fin": "15:30"},
        {"hora_inicio": "15:30", "hora_fin": "17:00"},
        {"hora_inicio": "17:30", "hora_fin": "19:00"},
        {"hora_inicio": "19:00", "hora_fin": "20:30"}
    ]

    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT hora_inicio, hora_fin FROM reserva 
        WHERE laboratorio_id = %s AND fecha = %s AND estado IN ('PENDIENTE', 'APROBADA')
    """, (id, fecha))
    ocupados = cur.fetchall()
    con.close()

    horas_ocupadas = [(str(o["hora_inicio"])[:5], str(o["hora_fin"])[:5]) for o in ocupados]
    slots = []
    for b in bloques:
        slots.append({
            "hora_inicio": b["hora_inicio"],
            "hora_fin": b["hora_fin"],
            "disponible": (b["hora_inicio"], b["hora_fin"]) not in horas_ocupadas
        })

    return jsonify({"slots": slots})

@res.route("/reservas", methods=["GET"])
@jwt_required()
def listar():
    claims = get_jwt()
    uid = get_jwt_identity()
    con = conectar()
    cur = con.cursor(dictionary=True)
    
    if claims.get("rol") == "ADMIN":
        cur.execute("""
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
            ORDER BY r.fecha DESC, r.hora_inicio DESC
        """)
    else:
        cur.execute("""
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha DESC, r.hora_inicio DESC
        """, (uid,))
        
    datos = cur.fetchall()
    con.close()
    
    for d in datos:
        if d.get("fecha"): d["fecha"] = str(d["fecha"])
        if d.get("hora_inicio"): d["hora_inicio"] = str(d["hora_inicio"])[:5]
        if d.get("hora_fin"): d["hora_fin"] = str(d["hora_fin"])[:5]
    return jsonify(datos)

@res.route("/reservas/por-fecha", methods=["GET"])
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
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
            WHERE r.fecha = %s
            ORDER BY r.hora_inicio ASC
        """, (fecha,))
    else:
        cur.execute("""
            SELECT r.*, u.nombre as usuario_nombre, l.nombre as laboratorio_nombre
            FROM reserva r
            JOIN usuario u ON r.usuario_id = u.id
            JOIN laboratorio l ON r.laboratorio_id = l.id
            WHERE r.fecha = %s AND r.usuario_id = %s
            ORDER BY r.hora_inicio ASC
        """, (fecha, uid))
        
    datos = cur.fetchall()
    con.close()
    
    for d in datos:
        d["fecha"] = str(d["fecha"])
        d["hora_inicio"] = str(d["hora_inicio"])[:5]
        d["hora_fin"] = str(d["hora_fin"])[:5]
    return jsonify(datos)

@res.route("/reservas", methods=["POST"])
@jwt_required()
def crear():
    datos = request.get_json()
    identity = get_jwt_identity()
    hora_inicio = formatear_hora(datos.get("hora_inicio"))
    hora_fin = formatear_hora(datos.get("hora_fin"))

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO reserva(fecha, hora_inicio, hora_fin, motivo, estado, usuario_id, laboratorio_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (datos.get("fecha"), hora_inicio, hora_fin, datos.get("motivo"), "PENDIENTE", identity, datos.get("laboratorio_id"))
        )
        con.commit()
        con.close()
        return jsonify({"mensaje": "Reserva solicitada"}), 201
    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@res.route("/reservas/<int:id>", methods=["PUT"])
@admin_required
def actualizar(id):
    datos = request.get_json()
    hora_inicio = formatear_hora(datos.get("hora_inicio"))
    hora_fin = formatear_hora(datos.get("hora_fin"))
    
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(
            "UPDATE reserva SET fecha=%s, hora_inicio=%s, hora_fin=%s, motivo=%s, estado=%s, laboratorio_id=%s WHERE id=%s",
            (datos.get("fecha"), hora_inicio, hora_fin, datos.get("motivo"), datos.get("estado"), datos.get("laboratorio_id"), id)
        )
        con.commit()
        con.close()
        return jsonify({"mensaje": "Reserva actualizada"})
    except Exception as e:
        return jsonify({"mensaje": "Error interno al actualizar"}), 500

@res.route("/reservas/<int:id>", methods=["DELETE"])
@admin_required
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM reserva WHERE id=%s", (id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Reserva eliminada"})