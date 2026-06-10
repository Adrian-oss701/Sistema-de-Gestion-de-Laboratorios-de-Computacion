from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "umsa_programacion_web_iii"

jwt = JWTManager(app)

laboratorios = [
    {
        "id": 1,
        "nombre": "Laboratorio Redes",
        "capacidad": 30
    },
    {
        "id": 2,
        "nombre": "Laboratorio Programacion",
        "capacidad": 25
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/laboratorios')
def laboratorios_page():
    return render_template('laboratorios.html')

@app.route('/reservas')
def reservas_page():
    return render_template('reservas.html')

@app.route('/incidencias')
def incidencias_page():
    return render_template('incidencias.html')

@app.route('/api/login', methods=['POST'])
def login():

    datos = request.get_json()

    usuario = datos.get("usuario")
    password = datos.get("password")

    if usuario == "admin" and password == "1234":

        token = create_access_token(identity=usuario)

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token
        })

    return jsonify({
        "mensaje": "Credenciales incorrectas"
    }), 401

@app.route('/api/laboratorios', methods=['GET'])
def obtener_laboratorios():

    return jsonify(laboratorios)

@app.route('/api/laboratorios', methods=['POST'])
@jwt_required()
def crear_laboratorio():

    datos = request.get_json()

    nuevo = {
        "id": len(laboratorios) + 1,
        "nombre": datos.get("nombre"),
        "capacidad": datos.get("capacidad")
    }

    laboratorios.append(nuevo)

    return jsonify({
        "mensaje": "Laboratorio creado correctamente",
        "laboratorio": nuevo
    }), 201

@app.route('/api/laboratorios/capacidad/<int:minima>')
def laboratorios_por_capacidad(minima):

    resultado = [
        lab for lab in laboratorios
        if lab["capacidad"] >= minima
    ]

    return jsonify(resultado)

@app.route('/api/admin')
@jwt_required()
def panel_admin():

    return jsonify({
        "mensaje": "Acceso autorizado"
    })

if __name__ == '__main__':
    app.run(debug=True)