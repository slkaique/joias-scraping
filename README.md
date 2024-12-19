# Raspagem de Dados de um Site de Joias

Este projeto realiza a raspagem de dados de produtos de um site de joias. Ele coleta informações como nome do produto, preço a prazo e preço à vista, navegando automaticamente por todas as páginas do site.

## Objetivo
O objetivo principal deste script é construir uma base de dados em formato CSV contendo informações relevantes dos produtos listados no site, permitindo análises e usos futuros.

## Funcionalidades
- **Extração de informações detalhadas**:
  - Nome do produto.
  - Preço a prazo.
  - Preço à vista.
- **Navegação automática**:
  - O script percorre todas as páginas de produtos até que não haja mais itens disponíveis.
- **Exportação de dados**:
  - Os dados extraídos são salvos em um arquivo CSV para fácil manipulação.

## Tecnologias Utilizadas

### Bibliotecas Python
1. **requests**:
   - Utilizada para realizar requisições HTTP e obter o conteúdo HTML das páginas do site.
   - [Documentação oficial](https://docs.python-requests.org/)

2. **BeautifulSoup**:
   - Parte da biblioteca `bs4`, utilizada para analisar o HTML e localizar os elementos de interesse na página.
   - [Documentação oficial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

3. **pandas**:
   - Usada para estruturar os dados extraídos em forma de tabela e exportá-los para um arquivo CSV.
   - [Documentação oficial](https://pandas.pydata.org/)

### Estrutura do Script

#### Variáveis Principais
- `pagina`: Controla o número da página atual sendo processada.
- `produtos`: Lista onde os produtos extraídos são armazenados.

#### Função `pegar_valores`
Esta função é responsável por:
1. Fazer uma requisição HTTP à URL da página específica.
2. Analisar o HTML usando BeautifulSoup.
3. Encontrar os elementos HTML que contêm os detalhes do produto (nome, preço a prazo, preço à vista).
4. Adicionar essas informações em formato de dicionário à lista `produtos`.
5. Retornar `False` caso não haja produtos na página, indicando o fim da navegação.

#### Loop Principal (`while`)
- Incrementa o número da página em cada iteração.
- Para de executar automaticamente ao atingir uma página sem produtos.
- Garante que todas as páginas de produtos sejam processadas sem risco de loops infinitos.

#### Exportação de Dados
- Os dados armazenados na lista `produtos` são convertidos para um DataFrame do pandas e exportados para um arquivo CSV chamado `resultados.csv`.

### Código do Script
```python
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
    product_elements = soup.find_all('div', class_='product-details')

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
```

### Como Configurar e Executar o Script

#### 1. Criar um Ambiente Virtual
É recomendável usar um ambiente virtual para evitar conflitos de dependências:
- No Windows:
  ```bash
  python -m venv myenv
  myenv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  python3 -m venv myenv
  source myenv/bin/activate
  ```

#### 2. Instalar Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:
```bash
pip install requests beautifulsoup4 pandas
```

#### 3. Gerar o `requirements.txt`
Para facilitar a instalação das dependências em outro ambiente:
```bash
pip freeze > requirements.txt
```

#### 4. Instalar Dependências Usando o `requirements.txt`
Caso outra pessoa precise replicar o ambiente, basta usar:
```bash
pip install -r requirements.txt
```

#### 5. Executar o Script
Salve o código em um arquivo chamado, por exemplo, `raspagem.py`, e execute-o com:
```bash
python raspagem.py
```

### Resultados
Após a execução, o arquivo `resultados.csv` será gerado no mesmo diretório do script. Ele conterá as informações dos produtos extraídos.

### Observações
- **Conexão com a Internet**: Certifique-se de que está conectado à Internet durante a execução do script.
- **Mudanças no site**: Se a estrutura HTML do site for alterada, o script pode precisar de ajustes para localizar corretamente os elementos desejados.
- **Uso ético**: Certifique-se de que a raspagem de dados está em conformidade com os termos de uso do site.

### Licença
Este projeto é livre para uso e modificação. Utilize-o de forma responsável!

