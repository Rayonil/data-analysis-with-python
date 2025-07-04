# Data Cleaning

# ======================================================
# Importação das bibliotecas
# ======================================================
import pandas as pd

# ======================================================
# 1. Carregamento dos dados
# ======================================================
df = pd.read_excel('data/Customer Call List.xlsx')

# ======================================================
# 2. Remoção de dados redundantes e colunas desnecessárias
# ======================================================
df = df.drop_duplicates()  # Remove linhas duplicadas
df = df.drop(columns="Not_Useful_Column")  # Remove coluna irrelevante

# ======================================================
# 3. Limpeza da coluna "Last_Name"
# ======================================================
# Remove todos os caracteres que não sejam letras (ex: pontuação, números, etc.)
df['Last_Name'] = df['Last_Name'].str.replace(r'[^a-zA-Z]', '', regex=True)

### r'[^a-zA-Z]': expressão regular que seleciona qualquer caractere que não seja uma letra (maiúscula ou minúscula).

### '': substitui esses caracteres indesejados por nada, ou seja, remove.

### regex=True: garante que o pandas interprete a string como expressão regular.

# ======================================================
# 4. Limpeza e formatação da coluna "Phone_Number"
# ======================================================
# Remove qualquer caractere que não seja letra ou número
df['Phone_Number'] = df['Phone_Number'].str.replace(r'[^a-zA-Z0-9]', '', regex=True)

### Neste caso r'[^a-zA-Z0-9]': expressão regular que seleciona qualquer caractere que não seja uma letra (maiúscula, minúscula ou número).

# Garante que todos os números estão em formato string
df['Phone_Number'] = df['Phone_Number'].astype(str)

# Aplica formatação padrão: 123-456-7890
df['Phone_Number'] = df['Phone_Number'].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

# Substitui entradas inválidas como "nan--", "Na--", etc., por string vazia
df['Phone_Number'] = df['Phone_Number'].replace(r'(?i)^na.*--$', '', regex=True)

### Neste caso r'(?i)^na.*--$': expressão que significa:

	### (?i): ignora maiúsculas/minúsculas (case insensitive).
	### ^na: começa com "na", "Na", "nA", etc.
	### .*--$: seguido de qualquer coisa que termine com --.

# ======================================================
# 5. Separação da coluna de endereço em três colunas
# ======================================================
# Divide o campo 'Address' em 'Street_Address', 'State' e 'Zip_Code'
df[["Street_Address", "State", "Zip_Code"]] = df['Address'].str.split(',', n=2, expand=True)

# ======================================================
# 6. Padronização das colunas booleanas (Yes/No → Y/N)
# ======================================================
df["Do_Not_Contact"] = df["Do_Not_Contact"].replace({'Yes': 'Y', 'No': 'N'})
df["Paying Customer"] = df["Paying Customer"].replace({'Yes': 'Y', 'No': 'N'})

# ======================================================
# 7. Tratamento de valores ausentes
# ======================================================
# Converte valores como "N/a", "na", "NA" em valores nulos reconhecidos
df = df.replace(['N/a', 'n/a', 'NA', 'na'], pd.NA).fillna('')

# Substitui valores vazios nas colunas de interesse por "N"
df[["Paying Customer", "Do_Not_Contact"]] = df[["Paying Customer", "Do_Not_Contact"]].replace('', 'N')

# ======================================================
# 8. Filtragem de dados
# ======================================================
# Remove clientes que não devem ser contatados (Do_Not_Contact = 'Y')
df = df[df["Do_Not_Contact"] != 'Y']

# Remove registros sem número de telefone válido
df = df[df["Phone_Number"] != '']

# ======================================================
# 9. Reset do índice final
# ======================================================
df = df.reset_index(drop=True)

# ======================================================
# 10. Visualização final (opcional)
# ======================================================
print(df)