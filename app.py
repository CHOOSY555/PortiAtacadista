from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API Porti Ofertas está rodando!"

@app.route('/ofertas')
def get_ofertas():
    url = 'https://portiatacadista.com.br/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Não foi possível acessar o site", "details": str(e)}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    ofertas = []
    # Esse seletor CSS captura os textos das ofertas (ajuste conforme a estrutura real do site)
    for item in soup.select('.texto-info-produto'):
        texto = item.get_text(strip=True)
        if texto and len(ofertas) < 10:
            ofertas.append(texto)

    nome_bot = os.environ.get("NOME_BOT", "Porti Ofertas")

    return jsonify({
        "bot": nome_bot,
        "ofertas": ofertas
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
