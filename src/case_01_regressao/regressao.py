# Importando bibliotecas
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Título para aplicação streamlit
st.title('Previsão Inicial de Custo para Franquia')

# Lendo dataset
df = pd.read_csv('slr12.csv', sep=';')

# Definindo variáveis features x target
X = df[['FrqAnual']]
y = df['CusInic']

# Instanciando modelo
modelo = LinearRegression().fit(X, y)

# Criando colunas para moldar página do streamlit
col1, col2 = st.columns(2)

# Configurando coluna 1 - Apresentando o dataframe
with col1:
    st.header('Dados')
    st.table(df.head(10))

# Configurando coluna 2 - Plotando gráfico de dispersão
with col2:
    st.header('Gráfico de Dispersão')
    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue')
    ax.plot(X, modelo.predict(X), color='red')
    st.pyplot(fig)

# Criação do input para usuário realizar previsão
st.header('Valor Anual da Franquia:')

# Definindo valor mínimo, máximo do input e step
novo_valor = st.number_input('Insira Novo Valor', min_value=1.0, max_value=999999.0, value=1500.0, step=0.01)

# Criando botão para processar valor inputado
processar = st.button('Processar')

# Aplicando regra para processamento
if processar:
    df_novo_valor = pd.DataFrame([[novo_valor]], columns=['FrqAnual'])
    previsao = modelo.predict(df_novo_valor)
    st.header(f'Previsão de Custo Inicial R$: {previsao[0]:.2f}')
