from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/ofertas')
def get_ofertas():
    url = 'https://portiatacadista.com.br/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ofertas = []

    for item in soup.select('.texto-info-produto'):
        texto = item.get_text(strip=True)
        if texto and len(ofertas) < 10:
            ofertas.append(texto)

    return jsonify(ofertas)

if __name__ == '__main__':
    app.run()