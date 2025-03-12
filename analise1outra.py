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

# Filtrar para retirar aqueles que só jogaram uma vez no dia
contagem_series = contagem_series[contagem_series > 2]


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
print("\nEstatísticas das contagens sem aqueles que jogaram 2 ou menos partidas:")
print(f"Moda: {moda}")
print(f"Média: {media:.2f}")
print(f"Mediana: {mediana}")
print(f"1º Quartil (Q1): {Q1}")
print(f"2º Quartil (Q2 - Mediana): {Q2}")
print(f"3º Quartil (Q3): {Q3}")
print(f"Variância: {variancia:.2f}")
print(f"Desvio Padrão: {desvio_padrao:.2f}")

#----------------------------------------------------------------------------------- Grafico Barras
import matplotlib.pyplot as plt

# Contar quantas vezes cada número de jogos ocorreu
jogos_feitos = contagem_series.value_counts().sort_index()

# Criar gráfico de barras corretamente
plt.bar(jogos_feitos.index, jogos_feitos.values, color='blue')

plt.xlabel("Jogos por dia")
plt.ylabel("Quantidade de jogadores")
plt.title("Distribuição da quantidade de jogos por jogador em um dia")

plt.xticks(jogos_feitos.index)  # Ajustar rótulos do eixo X para os valores corretos

plt.show()
# ---------------------------------------------------------------------- Grafico Boxplot
import matplotlib.pyplot as plt

# Criar o Boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(contagem_series.values, vert=True, patch_artist=True)

# Configurações do Gráfico
plt.title("Distribuição de Jogos por Dia (Boxplot)")
plt.ylabel("Quantidade de Jogos")
plt.grid(True)

# Exibir o Gráfico
plt.show()
#------------------------------------------------------------------ Novo DataFrame com trofeus e partidas
# Ordenar pelo jogador e pela data (se necessário)
df_sorted = df.sort_values(by=[2, 0], ascending=[True, True])

# Filtrar a última ocorrência de cada jogador (baseado na data)
df_last_occurence = df_sorted.groupby(2).last().reset_index()


# Fazer o merge entre df e resultado_df
df_merged = df_last_occurence[[2, 3]].merge(resultado_df, left_on=2, right_on='Valor', how='right')

# Renomear colunas para melhor entendimento
df_merged.rename(columns={2: 'ID_Jogador', 3: 'Trofeus', 'Contagem': 'Qtd_Jogos'}, inplace=True)

# Selecionar as colunas desejadas
df_final = df_merged[['ID_Jogador', 'Trofeus', 'Qtd_Jogos']]

# Exibir o resultado
#print(df_final)

# Remover linhas onde a coluna 'Trofeus' for NaN
df_final_cleaned = df_final.dropna(subset=['Trofeus'])

# Exibir o resultado
print(df_final_cleaned)
#--------------------------------------------------------------------------------- Grafico dispersão
import scipy.stats as stats
# Agrupar pela quantidade de jogos e calcular a média de troféus para cada grupo
df_grouped = df_final_cleaned.groupby('Qtd_Jogos').agg({'Trofeus': 'mean'}).reset_index()

# Plotando o gráfico
plt.figure(figsize=(10, 6))

# Gráfico de barras
plt.scatter(df_grouped['Qtd_Jogos'], df_grouped['Trofeus'], color='red')

# Calcular a regressão linear
slope, intercept, r_value, p_value, std_err = stats.linregress(df_grouped['Qtd_Jogos'], df_grouped['Trofeus'])

# Criar a linha de regressão
regression_line = slope * df_grouped['Qtd_Jogos'] + intercept

# Plotar a linha de regressão
plt.plot(df_grouped['Qtd_Jogos'], regression_line, color='black', label='Regressão Linear')

# Definir os rótulos e o título
plt.xlabel("Quantidade de Jogos Feitos")
plt.ylabel("Média de Troféus")
plt.title("Média de Troféus por Quantidade de Jogos Feitos")

# Exibir o gráfico
plt.show()

#-------------------------------------------------------