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

    # Pega o título das ofertas
    titulo = soup.select_one('.container-slide-offers > h3')
    titulo_texto = titulo.get_text(strip=True) if titulo else "Ofertas"

    ofertas = []
    container = soup.select_one('.container-slide-offers .slide-offers')
    if container:
        # Busca as divs das ofertas (cada produto)
        divs_ofertas = container.find_all('div', recursive=False)  # só filhos diretos
        for div in divs_ofertas:
            nome = div.select_one('.slide-offers-item')
            preco = div.select_one('.slide-offers-price')
            if nome and preco:
                ofertas.append({
                    "produto": nome.get_text(strip=True),
                    "preco": preco.get_text(strip=True)
                })
            if len(ofertas) >= 10:
                break

    nome_bot = os.environ.get("NOME_BOT", "Porti Ofertas")

    return jsonify({
        "bot": nome_bot,
        "titulo": titulo_texto,
        "ofertas": ofertas
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
