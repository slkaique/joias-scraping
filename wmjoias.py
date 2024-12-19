import requests
from bs4 import BeautifulSoup
import pandas as pd

pagina = 1
produtos = []

# Função para pegar valores de uma página
def pegar_valores(url, produtos):
    # Fazendo a requisição à página
    response = requests.get(url)
    html_content = response.text

    # Analisando o HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrando todos os produtos e preços
    product_elements = soup.find_all('div', class_='product-details')  # Ajuste conforme necessário

    # Se não houver produtos, retorne False para indicar o fim das páginas
    if not product_elements:
        return False

    for product in product_elements:
        # Nome do produto
        nome = product.find('div', class_='product-name').h3.text.strip()

        # Preço a prazo
        preco_a_prazo = product.find('span', class_='price-currency-home')
        preco_a_prazo = preco_a_prazo.text.strip() if preco_a_prazo else "Não encontrado"

        # Preço à vista
        preco_a_vista = product.find('span', class_='preco-avista precoAvista')
        preco_a_vista = preco_a_vista.text.strip().replace('\n', '').replace('R$', '').strip() if preco_a_vista else "Não encontrado"

        # Armazenar no formato de dicionário
        produtos.append({
            "produto": nome,
            "preco_a_prazo": preco_a_prazo,
            "preco_a_vista": preco_a_vista,
        })

    return True

# Loop para iterar pelas páginas
while True:
    url = f'https://www.wmjoias.com.br/aliancas-de-casamento/ouro-amarelo-18k?pg={pagina}'
    sucesso = pegar_valores(url, produtos)
    if not sucesso:  # Para o loop se não houver mais produtos
        break
    pagina += 1

# Criando um DataFrame e salvando em CSV
df = pd.DataFrame(produtos)
df.to_csv('resultados.csv', index=False)

print("Dados salvos em 'resultados.csv'")
