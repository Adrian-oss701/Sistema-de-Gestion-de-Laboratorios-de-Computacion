from flask import Blueprint, jsonify, request
from database import conectar
from routes.auth_roles import admin_required

rep = Blueprint("rep", __name__)


@rep.route("/reportes/reporte_1", methods=["GET"])
def listar():
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            l.id,
            l.nombre,
            l.ubicacion,
            l.capacidad,
            l.estado,
            COUNT(r.id) AS cantidad_reservas
        FROM laboratorio l
        LEFT JOIN reserva r
            ON l.id = r.laboratorio_id
        GROUP BY 
            l.id,
            l.nombre,
            l.ubicacion,
            l.capacidad,
            l.estado
        ORDER BY cantidad_reservas DESC
    """)

    datos = cur.fetchall()
    con.close()

    return jsonify(datos)

@rep.route("/reportes/reporte_2", methods=["GET"])
def reporte_2():
    con = conectar()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT
            l.id,
            l.nombre,
            l.ubicacion,
            l.capacidad,
            l.estado,
            COUNT(i.id) AS cantidad_incidencias
        FROM laboratorio l
        LEFT JOIN incidencia i
            ON l.id = i.laboratorio_id
        GROUP BY
            l.id,
            l.nombre,
            l.ubicacion,
            l.capacidad,
            l.estado
        ORDER BY cantidad_incidencias DESC
    """)
    datos = cur.fetchall()
    cur.close()
    con.close()

    return jsonify(datos)
@rep.route("/reportes/reporte_3", methods=["GET"])
def reporte_3():
    con = conectar()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT
            id,
            nombre,
            ubicacion,
            capacidad,
            estado
        FROM laboratorio
        WHERE estado = 'DISPONIBLE'
        ORDER BY id
    """)

    datos = cur.fetchall()

    cur.close()
    con.close()

    return jsonify(datos)


@rep.route("/reportes/reporte_4/<int:capacidad>", methods=["GET"])
def buscar_por_capacidad(capacidad):
    con = conectar()
    cur = con.cursor(dictionary=True)

    cur.execute("""
        SELECT *
        FROM laboratorio l
        WHERE l.capacidad = %s
     """, (capacidad,))

    datos = cur.fetchall()
    con.close()

    return jsonify(datos)