from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/api/ofertas", methods=["GET", "POST"])
def obter_ofertas():
    # seu código
    # Você pode usar request.json se quiser parâmetros da Alexa, mas não obrigatório
    url = "https://portiatacadista.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    ofertas = []

    # Coletar do slider principal
    slide_container = soup.select_one(".slide-offers")
    if slide_container:
        for item in slide_container.find_all("div", recursive=False):
            produto_tag = item.find("p", class_="slide-offers-item")
            preco_tag = item.find("p", class_="slide-offers-price")
            if produto_tag and preco_tag:
                ofertas.append({
                    "produto": produto_tag.get_text(strip=True),
                    "preco": preco_tag.get_text(strip=True)
                })

    # Coletar da lista de produtos adicionais
    low_container = soup.select_one(".offers-products-low")
    if low_container:
        for item in low_container.find_all("div", recursive=False):
            produto_tag = item.find("p", class_="offers-products-low-item")
            preco_tag = item.find("p", class_="offers-products-low-price")
            if produto_tag and preco_tag:
                ofertas.append({
                    "produto": produto_tag.get_text(strip=True),
                    "preco": preco_tag.get_text(strip=True)
                })

    # Remover duplicatas por nome do produto
    vistos = set()
    ofertas_unicas = []
    for o in ofertas:
        if o["produto"] not in vistos:
            vistos.add(o["produto"])
            ofertas_unicas.append(o)

    return jsonify({
        "bot": "Porti Ofertass",
        "titulo": "Ofertas válidas: 13/06/2025 - 15/06/2025",
        "ofertas": ofertas_unicas
    })


if __name__ == "__main__":
    app.run(debug=True)
