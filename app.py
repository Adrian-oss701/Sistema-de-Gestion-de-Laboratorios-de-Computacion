from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/laboratorios')
def laboratorios():
    return render_template('laboratorios.html')

@app.route('/reservas')
def reservas():
    return render_template('reservas.html')

@app.route('/incidencias')
def incidencias():
    return render_template('incidencias.html')

if __name__ == '__main__':
    app.run(debug=True)