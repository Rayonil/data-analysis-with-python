# Web Scraping: Maiores Empresas dos EUA por Receita (Wikipedia)
# ======================================================
# Importação das bibliotecas
# ======================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# 1. URL alvo
# ======================================================
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

# ======================================================
# 2. Requisição com verificação de status
# ======================================================
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Erro ao acessar a página: {response.status_code}")

# ======================================================
# 3. Parse HTML
# ======================================================
soup = BeautifulSoup(response.text, 'html.parser')

# ======================================================
# 4. Encontrar a tabela correta (com 'wikitable sortable')
# ======================================================
tables = soup.find_all('table', class_='wikitable sortable')
target_table = tables[0]  # normalmente a primeira contém as informações principais

# ======================================================
# 5. Extrair títulos
# ======================================================
headers = [th.text.strip() for th in target_table.find_all('th')]

# ======================================================
# 6. Inicializar DataFrame
# ====================================================== 
df = pd.DataFrame(columns=headers)

# ======================================================
# 7. Extrair dados da tabela
# ======================================================
for row in target_table.find_all('tr')[1:]:
    cells = row.find_all('td')
    values = [cell.text.strip() for cell in cells]
    if values:
        df.loc[len(df)] = values

# Exibir primeiros registros
print(df.head())

# ======================================================
# 8. Salvar os dados em um arquivo CSV
# ======================================================
df.to_csv(r'data\Companies.csv', index = False)