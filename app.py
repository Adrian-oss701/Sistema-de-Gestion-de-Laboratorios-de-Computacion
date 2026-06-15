import pymysql
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)
from sistema_laboratorios.backend import config

app = Flask(__name__)

# Configuración del Sistema
app.config["JWT_SECRET_KEY"] = "umsa_programacion_web_iii"
app.config.from_object(config)

# =====================================================================
# ADAPTADOR DE CONEXIÓN PARA REEMPLAZAR FLASK_MYSQLDB EN WINDOWS
# =====================================================================
class MySQLAdaptador:
    def __init__(self, app=None):
        if app:
            self.config = app.config

    @property
    def connection(self):
        return pymysql.connect(
            host=self.config.get('MYSQL_HOST', 'localhost'),
            user=self.config.get('MYSQL_USER', 'root'),
            password=self.config.get('MYSQL_PASSWORD', ''),
            database=self.config.get('MYSQL_DB', ''),
            port=self.config.get('MYSQL_PORT', 3306),
            autocommit=True  # Hace commits automáticos para los INSERT/UPDATE
        )

# Tu variable sigue llamándose igual para no alterar tus endpoints
mysql = MySQLAdaptador(app)
jwt = JWTManager(app)


# =====================================================================
# RUTAS DE INTERFAZ GRÁFICA (HTML)
# =====================================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/laboratorios_html')
def laboratorios_page():
    return render_template('laboratorios.html')

@app.route('/reservas_html')
def reservas_page():
    return render_template('reservas.html')

@app.route('/incidencias')
def incidencias_page():
    return render_template('incidencias.html')


# =====================================================================
# ENDPOINTS DE LA API
# =====================================================================

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
    conn = mysql.connection
    cursor = conn.cursor()
    sql = 'SELECT * FROM laboratorios'
    cursor.execute(sql)
    data = cursor.fetchall()
    
    laboratorios = []
    for fila in data:
        laboratorios.append({
            "id": fila[0],
            "nombre": fila[1],
            "ubicacion": fila[2],
            "capacidad": fila[3],
            "estado": fila[4]
        })
    
    cursor.close()  
    conn.close()
    return jsonify(laboratorios)


@app.route('/api/laboratorios', methods=['POST'])
@jwt_required()
def crear_laboratorio():
    datos = request.get_json()
    
    nombre = datos.get("nombre")
    ubicacion = datos.get("ubicacion", "Sin ubicacion")
    capacidad = datos.get("capacidad")
    estado = datos.get("estado", "Disponible")

    conn = mysql.connection
    cursor = conn.cursor()
    sql = "INSERT INTO laboratorios (nombre, ubicacion, capacidad, estado) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nombre, ubicacion, capacidad, estado))
    
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Laboratorio creado correctamente",
        "laboratorio": {
            "id": nuevo_id,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "capacidad": capacidad,
            "estado": estado
        }
    }), 201


@app.route('/api/laboratorios/capacidad/<int:minima>')
def laboratorios_por_capacidad(minima):
    conn = mysql.connection
    cursor = conn.cursor()
    sql = 'SELECT * FROM laboratorios WHERE capacidad >= %s'
    cursor.execute(sql, (minima,))
    data = cursor.fetchall()
    
    resultado = []
    for fila in data:
        resultado.append({
            "id": fila[0],
            "nombre": fila[1],
            "ubicacion": fila[2],
            "capacidad": fila[3],
            "estado": fila[4]
        })
        
    cursor.close()
    conn.close()
    return jsonify(resultado)


@app.route('/api/admin')
@jwt_required()
def panel_admin():
    return jsonify({
        "mensaje": "Acceso autorizado"
    })


@app.route('/api/reservas', methods=['GET'])
def obtener_reservas():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = 'SELECT * FROM reservas'
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    reservas = []
    for fila in data:
        reservas.append({
            "id": fila[0],
            "id_laboratorio": fila[1],
            "id_usuario": fila[2],
            "fecha": str(fila[3]),
            "hora_ini": str(fila[4]),
            "hora_fin": str(fila[5]),
            "estado": fila[6]
        })
    return jsonify(reservas)


if __name__ == '__main__':
    app.run(debug=True)