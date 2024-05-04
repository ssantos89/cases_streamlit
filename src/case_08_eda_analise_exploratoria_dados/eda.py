# Importando bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Definindo título e nome da página
st.set_page_config(page_title='Análise Exploratória', layout='wide')
st.title('Despesas de Empenho da Rubrica Diárias do País')

# Carregando dados csv com cache_data
@st.cache_data
def load_data():
    dados = pd.read_csv('dados.csv', sep=';')
    dados['PROPORCAO'] = dados['VALOREMPENHO'] / dados['PIB']
    return dados


dados = load_data()

# Criando sidebar para controles
with st.sidebar:
    st.header('Configurações')
    top_n = st.number_input('Selecione o número de entradas para exibir', min_value=1, max_value=len(dados), value=10)

# Definindo tabulações
tab1, tab2, tab3 = st.tabs(['Visão Geral', 'Análises Detalhadas', 'Maiores Valores'])

with tab1:
    st.header('Resumo dos Dados')
    st.write(dados.describe())

with tab2:
    st.header('Distribução dos Dados')
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(dados, x='VALOREMPENHO', title='Histograma do Valor de Empenho')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(dados, x='VALOREMPENHO', title='Boxplot do Valor de Empenho')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.histogram(dados, x='PIB', title='Histograma do PIB')
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = px.box(dados, x='PIB', title='Boxplot do PIB')
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.header('Maiores Valores')
    col1, col2, col3 = st.columns(3)
    with col1:
         m_empenho = dados.nlargest(top_n, 'VALOREMPENHO')
         fig = px.bar(m_empenho, x='MUNICIPIO', y='VALOREMPENHO', title='Maiores Empenhos')
         st.plotly_chart(fig, use_container_width=True)

    with col2:
        m_pibs = dados.nlargest(top_n, 'PIB')
        fig2 = px.bar(m_pibs, x='MUNICIPIO', y='PIB', title='Maiores PIBs')
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        m_prop = dados.nlargest(top_n, 'PROPORCAO')
        fig3 = px.pie(m_prop, values='PROPORCAO', names='MUNICIPIO', title='Maiores Proporções ao PIB')
        st.plotly_chart(fig3, use_container_width=True)
