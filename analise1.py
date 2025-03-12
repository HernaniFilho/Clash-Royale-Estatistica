import pandas as pd

# Carregar o CSV
df = pd.read_csv('20221108.csv', header=None)

# Definir as colunas a serem analisadas
colunas_a_analisar = [2, 13]  # Colunas dos IDs dos jogadores

# Dicionário para armazenar as contagens
contagens = {}

# Contagem das ocorrências em cada coluna especificada
for indice_coluna in colunas_a_analisar:
    if indice_coluna < len(df.columns):
        contagens_coluna = df.iloc[:, indice_coluna].value_counts()
        for valor, contagem in contagens_coluna.items():
            if valor in contagens:
                contagens[valor] += contagem
            else:
                contagens[valor] = contagem
    else:
        print(f"A coluna de índice {indice_coluna} não existe no DataFrame.")

# Criar o DataFrame de contagens
resultado_df = pd.DataFrame(list(contagens.items()), columns=['Valor', 'Contagem'])

# Ordenar o DataFrame pela contagem em ordem decrescente
resultado_df.sort_values(by='Contagem', ascending=False, inplace=True)

# Resetar o índice
resultado_df.reset_index(drop=True, inplace=True)

# Exibir as 10 primeiras entradas
print("Primeiras 10 entradas do DataFrame:")
print(resultado_df.head(10))

# Calcular as estatísticas
contagem_series = resultado_df['Contagem']

# Moda
moda = contagem_series.mode()[0]  # Moda (o valor mais frequente)

# Média
media = contagem_series.mean()

# Mediana
mediana = contagem_series.median()

# Três quartis (Q1, Q2 e Q3)
Q1 = contagem_series.quantile(0.25)
Q2 = contagem_series.quantile(0.5)  # Mediana é o Q2
Q3 = contagem_series.quantile(0.75)

# Variância
variancia = contagem_series.var()

# Desvio padrão
desvio_padrao = contagem_series.std()

# Exibir as estatísticas
print("\nEstatísticas das contagens:")
print(f"Moda: {moda}")
print(f"Média: {media:.2f}")
print(f"Mediana: {mediana}")
print(f"1º Quartil (Q1): {Q1}")
print(f"2º Quartil (Q2 - Mediana): {Q2}")
print(f"3º Quartil (Q3): {Q3}")
print(f"Variância: {variancia:.2f}")
print(f"Desvio Padrão: {desvio_padrao:.2f}")