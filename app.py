from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>Funcionando con normalidad</h1>"

if __name__ == '__main__':
    app.run(debug=True)