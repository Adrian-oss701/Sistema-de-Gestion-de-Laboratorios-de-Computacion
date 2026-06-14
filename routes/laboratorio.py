from flask import Blueprint, jsonify, request
from database import conectar
from routes.auth_roles import admin_required

lab = Blueprint("lab", __name__)

@lab.route("/laboratorios", methods=["GET"])
def listar():
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM laboratorio")
    datos = cur.fetchall()
    con.close()
    return jsonify(datos)

@lab.route("/laboratorios/disponibles", methods=["GET"])
def disponibles():
    """Consulta personalizada: laboratorios disponibles en una fecha"""
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"mensaje": "Parámetro 'fecha' requerido (YYYY-MM-DD)"}), 400

    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT * FROM laboratorio
        WHERE estado = 'DISPONIBLE'
        AND id NOT IN (
            SELECT laboratorio_id FROM reserva
            WHERE fecha = %s AND estado IN ('PENDIENTE', 'APROBADA')
        )
    """, (fecha,))
    datos = cur.fetchall()
    con.close()
    return jsonify(datos)

@lab.route("/laboratorios/<int:id>", methods=["GET"])
def obtener(id):
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM laboratorio WHERE id=%s", (id,))
    dato = cur.fetchone()
    con.close()
    if not dato:
        return jsonify({"mensaje": "Laboratorio no encontrado"}), 404
    return jsonify(dato)

@lab.route("/laboratorios", methods=["POST"])
@admin_required
def crear():
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO laboratorio(nombre, ubicacion, capacidad, estado) VALUES(%s,%s,%s,%s)",
        (datos["nombre"], datos["ubicacion"], datos["capacidad"], datos["estado"])
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Laboratorio creado"}), 201

@lab.route("/laboratorios/<int:id>", methods=["PUT"])
@admin_required
def actualizar(id):
    datos = request.get_json()
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE laboratorio SET nombre=%s, ubicacion=%s, capacidad=%s, estado=%s WHERE id=%s",
        (datos["nombre"], datos["ubicacion"], datos["capacidad"], datos["estado"], id)
    )
    con.commit()
    con.close()
    return jsonify({"mensaje": "Laboratorio actualizado"})

@lab.route("/laboratorios/<int:id>", methods=["DELETE"])
@admin_required
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM laboratorio WHERE id=%s", (id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Laboratorio eliminado"})