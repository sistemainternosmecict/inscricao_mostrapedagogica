from flask import Flask, request, jsonify
from pprint import pprint

app = Flask(__name__)

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

def main():
    # The main function can be used to run the Flask app directly
    # For development, you might run `flask run` from the terminal
    # or use `app.run()`
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
