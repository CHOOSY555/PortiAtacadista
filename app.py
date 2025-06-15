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
    # Vamos buscar elementos que podem conter as ofertas dentro do container
    container = soup.select_one('.container-slide-offers')
    if container:
        # exemplo: buscar textos dentro de elementos filhos, como divs ou spans
        for oferta_item in container.select('p, span, div'):
            texto = oferta_item.get_text(strip=True)
            if texto and len(ofertas) < 10:
                ofertas.append(texto)

    nome_bot = os.environ.get("NOME_BOT", "Porti Ofertas")

    return jsonify({
        "bot": nome_bot,
        "titulo": titulo_texto,
        "ofertas": ofertas
    })
