from flask import Flask, request, jsonify
from flask_cors import CORS
from pprint import pprint

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "API online"

@app.route("/inscricao_entrada", methods=["POST"])
def inscricao_entrada():
    if request.is_json:
        data = request.get_json()
        print("--- dados passados via api ---")
        pprint(data)
        print("-----------------------------")
        return jsonify({"message": "Dados recebidos com sucesso!"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
