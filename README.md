# Sistema de Gestión de Laboratorios de Computación
Herramientas
Utilizadas
Python 3
Flask
MySQL
Flask-JWT-Extended
HTML
CSS
JavaScript
Instalación
1. Clonar el repositorio
git clone <url-del-repositorio>
cd Sistema
2. Crear y activar un entorno virtual (opcional)
Windows
python -m venv env
env\Scripts\activate
Linux / macOS
python3 -m venv env
source env/bin/activate
3. Instalar dependencias
pip install -r requirements.txt
Configuración de Base de Datos
Crear una base de datos MySQL.
CREATE DATABASE gestion_laboratorios;
Importar el script SQL incluido en el proyecto:
gestion_laboratorios.sql
Configurar las credenciales de conexión en el archivo:
database.py
Ejecución del Proyecto

Iniciar el servidor Flask:

python app.py

El sistema estará disponible en:

http://localhost:5000
