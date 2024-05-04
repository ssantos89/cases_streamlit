# Importando bibliotecas
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score

# Definindo página no formato wide
st.set_page_config(
    page_title = 'Classificação de Veículos',
    layout = 'wide'
)

# Setando opção de cache de página
@st.cache_data

# Função dos encoders, modelo, acurácia e classificação
def load_data_and_model():
    # Lendo o dataset
    carros = pd.read_csv('car.csv', sep=',')

    # Atribuindo OrdinalEncoder a variável
    encoder = OrdinalEncoder()

    # Percorrendo dataframe e excluíndo coluna class (target)
    for col in carros.columns.drop('class'):

        # Atribuindo todas as features como categoricas
        carros[col] = carros[col].astype('category')

    # Aplicando Encoder em todas as colunas exceto 'class' (target)
    X_encoded = encoder.fit_transform(carros.drop('class', axis=1))

    # Aplicando a coluna target em categoricos
    y = carros['class'].astype('category').cat.codes

    # Dividindo dataframe em treino e teste em 70% / 30%
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42)

    # Instânciando modelo
    modelo = CategoricalNB()
    
    # Treinando com base de treino
    modelo.fit(X_train, y_train)

    # Avaliando previsão do modelo
    y_pred = modelo.predict(X_test)

    # Visualizando acurácia do quanto o modelo acertou no treino
    acuracia = accuracy_score(y_test, y_pred)

    return encoder, modelo, acuracia, carros

# Chamando função para execução
encoder, modelo, acuracia, carros = load_data_and_model()

# Definindo título para aplicação
st.title('Previsão de Qualidade de Veículo')

# Apresentando a acurácia do modelo
st.write(f'Acurácia do modelo: {acuracia:.2f}')


# Criando caixas de seleção para o usuário setar para encontrar a previsão
input_features = [
    st.selectbox('Preço', carros['buying'].unique()),
    st.selectbox('Manutenção', carros['maint'].unique()),
    st.selectbox('Portas', carros['doors'].unique()),
    st.selectbox('Capacidade de Passageiros', carros['persons'].unique()),
    st.selectbox('Porta Malas', carros['lug_boot'].unique()),
    st.selectbox('Segurança', carros['safety'].unique()),
    ]

# Criando o botão para processamento do modelo
if st.button('Processar'):
    # Passando um dataframe como input iniciar a previsão
    input_df = pd.DataFrame([input_features], columns=carros.columns.drop('class'))

    # Realizando transformação categoricas para o input_df
    input_encoded = encoder.transform(input_df)

    # Realizando previsão
    predict_encoded = modelo.predict(input_encoded)

    # Previsão com os dados transformados (legível para o usuário)
    previsao = carros['class'].astype('category').cat.categories[predict_encoded][0]
    
    # Apresentando resultado para o usuário
    st.header(f'Resultado da previsão: {previsao}')