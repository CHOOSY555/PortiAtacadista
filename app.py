from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/ofertas", methods=["GET", "POST"])
def obter_ofertas():
    print("🟢 A rota /ofertas foi chamada!")

    # Só para testar se o deploy está atualizando corretamente:
    return jsonify({
        "status": "ok",
        "mensagem": "🚀 API atualizada em 15/06/2025 às 19h!",
        "dica": "Se está vendo isso, o deploy está funcionando.",
        "teste": True
    })

if __name__ == "__main__":
    app.run(debug=True)
