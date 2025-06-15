from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/api/ofertas", methods=["GET"])
def obter_ofertas():
    url = "https://portiatacadista.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    containers_classes = [
        "slide-offers-one",
        "slide-offers-two",
        "slide-offers-three",
        "slide-offers-four",
        "offers-products-low-one",
        "offers-products-low-two",
        "offers-products-low-three"
    ]

    ofertas = []

    for container_class in containers_classes:
        containers = soup.find_all("div", class_=container_class)
        for c in containers:
            produto = c.find("p", class_="slide-offers-item") or c.find("p", class_="offers-products-low-item")
            preco = c.find("p", class_="slide-offers-price") or c.find("p", class_="offers-products-low-price")

            if produto and preco:
                ofertas.append({
                    "produto": produto.get_text(strip=True),
                    "preco": preco.get_text(strip=True)
                })

    # Remover duplicatas
    vistos = set()
    ofertas_unicas = []
    for o in ofertas:
        if o["produto"] not in vistos:
            vistos.add(o["produto"])
            ofertas_unicas.append(o)

    return jsonify({
        "bot": "Porti Ofertas",
        "titulo": "Ofertas válidas: 13/06/2025 - 15/06/2025",
        "ofertas": ofertas_unicas
    })

if __name__ == "__main__":
    app.run(debug=True)
