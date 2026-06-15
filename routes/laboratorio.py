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
    """Consulta personalizada: laboratorios disponibles en una fecha y horario"""
    fecha = request.args.get("fecha")
    hora_inicio = request.args.get("hora_inicio")
    hora_fin = request.args.get("hora_fin")
    
    if not fecha:
        return jsonify({"mensaje": "Parámetro 'fecha' requerido (YYYY-MM-DD)"}), 400

    con = conectar()
    cur = con.cursor(dictionary=True)
    
    # Si se envían horas, filtrar por conflicto de horario
    if hora_inicio and hora_fin:
        cur.execute("""
            SELECT * FROM laboratorio
            WHERE estado = 'DISPONIBLE'
            AND id NOT IN (
                SELECT laboratorio_id FROM reserva
                WHERE fecha = %s 
                AND estado IN ('PENDIENTE', 'APROBADA')
                AND NOT (hora_fin <= %s OR hora_inicio >= %s)
            )
        """, (fecha, hora_inicio, hora_fin))
    else:
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

@lab.route("/laboratorios/<int:id>/horarios", methods=["GET"])
def horarios_disponibles(id):
    """Consulta horarios disponibles para un laboratorio específico en una fecha"""
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"mensaje": "Parámetro 'fecha' requerido"}), 400
    
    con = conectar()
    cur = con.cursor(dictionary=True)
    
    # Verificar si el laboratorio existe y está disponible
    cur.execute("SELECT * FROM laboratorio WHERE id=%s", (id,))
    lab_data = cur.fetchone()
    if not lab_data:
        con.close()
        return jsonify({"mensaje": "Laboratorio no encontrado"}), 404
    
    # Obtener reservas existentes para ese día y laboratorio
    cur.execute("""
        SELECT hora_inicio, hora_fin, estado 
        FROM reserva 
        WHERE laboratorio_id = %s AND fecha = %s AND estado IN ('PENDIENTE', 'APROBADA')
        ORDER BY hora_inicio
    """, (id, fecha))
    reservas = cur.fetchall()
    con.close()
    
    # Generar slots de 1 hora de 07:00 a 21:00
    slots = []
    for h in range(7, 21):
        inicio = f"{h:02d}:00"
        fin = f"{h+1:02d}:00"
        ocupado = False
        for r in reservas:
            r_inicio = str(r['hora_inicio'])[:5]
            r_fin = str(r['hora_fin'])[:5]
            # Si hay solapamiento
            if not (fin <= r_inicio or inicio >= r_fin):
                ocupado = True
                break
        slots.append({
            "hora_inicio": inicio,
            "hora_fin": fin,
            "disponible": not ocupado
        })
    
    return jsonify({
        "laboratorio": lab_data,
        "fecha": fecha,
        "slots": slots
    })

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


