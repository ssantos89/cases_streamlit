# Importando bibliotecas
import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from datetime import date
from io import StringIO

# Definindo configuração da página
st.set_page_config(page_title='Sistema de Análise e Previsão de Séries Temporais',
                   layout='wide')

# Definindo título para aplicação
st.title('Sistema de Análise e Previsão de Séries Temporais')

# Configurando sidebar para manipular os dados
with st.sidebar:
    # Realizando upload do arquivo tipo csv
    uploaded_file = st.file_uploader('Escolha o arquivo:', type=['csv'])

    # Aplicando decode utf-8
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))

        # Lendo csv que foi inputado sem cabeçalho
        data = pd.read_csv(stringio, header=None)

        # Definindo data início
        data_inicio = date(2000, 1, 1)

        # Definindo período da série
        periodo = st.date_input('Período Inicial da Série', data_inicio)

        # Período de previsão
        periodo_previsao = st.number_input('Informe quantos meses quer prever', min_value=1, max_value=48, value=12)

        # Botão de processar
        processar = st.button('Processar')

# Aplicando tratamento para garantir que usuário inseriu o csv
if uploaded_file is not None and processar:
    try:
        # Convertendo dados DataFrame para Series e definindo a frequencia como mês
        ts_data = pd.Series(data.iloc[:, 0].values, index=pd.date_range(start=periodo, periods=len(data), freq='M'))

        # Criando a decomposição com modelo additive
        decomposicao = seasonal_decompose(ts_data, model='additive')

        # Setando o plot para decomposicao
        fig_decomposicao = decomposicao.plot()

        # Configurando o tamanho do plot
        fig_decomposicao.set_size_inches(10, 8)

        # Definindo a previsão
        modelo = SARIMAX(ts_data, order=(2, 0, 0), seasonal_order=(0, 1, 1, 12))

        # Treinando o modelo
        modelo_fit = modelo.fit()

        # Realizando forecast (previsao)
        previsao = modelo_fit.forecast(steps=periodo_previsao)

        # Configurando plot da previsao
        fig_previsao, ax = plt.subplots(figsize=(10, 5))
        ax = ts_data.plot(ax=ax)
        previsao.plot(ax=ax, style='r--')

        # Definindo colunas para os plots (decomposição, previsão e dados originais)
        col1, col2, col3 = st.columns([3, 3, 1])

        # Coluna da decomposição
        with col1:
            st.write('Decomposição')
            st.pyplot(fig_decomposicao)

        # Coluna da decomposição
        with col2:
            st.write('Previsão')
            st.pyplot(fig_previsao)

        # Coluna dos dados originais
        with col3:
            st.write('Dados da Previsão')
            st.dataframe(previsao)

    except Exception as e:
        st.error(f'Erro ao processar os dados: {e}')