from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from routes.auth import auth
from routes.laboratorio import lab
from routes.usuario import usu
from routes.reserva import res
from routes.incidencia import inc
from routes.reportes import rep

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "umsa2026"
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(lab)
app.register_blueprint(usu)
app.register_blueprint(res)
app.register_blueprint(inc)
app.register_blueprint(rep)

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/laboratorios-ver")
def laboratorios_view():
    return render_template("laboratorios.html")

@app.route("/reservas-ver")
def reservas_view():
    return render_template("reservas.html")

@app.route("/incidencias-ver")
def incidencias_view():
    return render_template("incidencias.html")

@app.route("/usuarios-ver")
def usuarios_view():
    return render_template("usuarios.html")

@app.route("/reportes-ver")
def reportes_view():
    return render_template("reportes.html")

@app.route("/reportes-ver/reporte_1")
def reportes_1_view():
    return render_template("reporte1.html")

@app.route("/reportes-ver/reporte_2")
def reportes_2_view():
    return render_template("reporte2.html")

@app.route("/reportes-ver/reporte_3")
def reportes_3_view():
    return render_template("reporte3.html")

@app.route("/reportes-ver/reporte_4")
def reportes_4_view():
    return render_template("reporte4.html")

if __name__ == "__main__":
    app.run(debug=True)