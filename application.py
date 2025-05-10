import os

from dotenv import load_dotenv
from flask import jsonify

from src import create_app

load_dotenv()

application = create_app()

@application.route("/")
def index():
    return jsonify({"response": "Prueba despliegue Blue/green"})

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
