import requests
from bs4 import BeautifulSoup

url = 'https://portiatacadista.com.br/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

ofertas = []

# Exemplo para ofertas em destaque (container-slide-offers)
slide_offers = soup.select('.container-slide-offers .slide-offers > div')
for offer in slide_offers:
    produto = offer.select_one('.slide-offers-item')
    preco = offer.select_one('.slide-offers-price')
    if produto and preco:
        ofertas.append({
            'produto': produto.text.strip(),
            'preco': preco.text.strip()
        })

# Exemplo para outra seção (container-offers-products-low)
low_offers = soup.select('.container-offers-products-low .offers-products-low > div')
for offer in low_offers:
    produto = offer.select_one('.offers-products-low-item')
    preco = offer.select_one('.offers-products-low-price')
    if produto and preco:
        ofertas.append({
            'produto': produto.text.strip(),
            'preco': preco.text.strip()
        })

print(f"Total ofertas encontradas: {len(ofertas)}")
for o in ofertas:
    print(f"{o['produto']} - {o['preco']}")
