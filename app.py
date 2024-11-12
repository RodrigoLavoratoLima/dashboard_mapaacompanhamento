from database import main  # Importa a função main do módulo database
import pandas as pd
import numpy as np
import streamlit as st
import time

st.set_page_config(layout='wide')
# Exibe o logo e o título
st.logo("Media/CPTM_(Logo).svg.png")  # Para exibir a imagem, use st.image em vez de st.logo
st.title("MAPA DE ACOMPANHAMENTO")

def tabela_falhas():
    # Obtenha o DataFrame de `main`
    df = {}
    df = main()  # Certifique-se de que main() retorna um DataFrame

    column_configs = {
        'DESCRIÇÃO DA ABERTURA': {
            'help': "Descrição de abertura da falha",
            'width': 401,
        }
    }
    return df

def filtros_tabela(df):
    st.sidebar.title('Filtros do Mapa de Acompanhamento')
    with st.sidebar.expander('Série de Trens'):
        serie = st.multiselect(
            'Selecione a Série',
            df['FROTA'].unique()
        )
        if len(serie) > 0:
            df_filtrado = df[df['FROTA'].isin(serie)]
        else:
            df_filtrado = df
    return df_filtrado

def indicadores():
    st.title("Second page")
    
st.divider()
left, right = st.columns(2)
left.text(f'Atualizar a base de dados')
left.caption(f'Clique no botão atualizar para iniciar o processo de download da base de dados via CSICOM')
if right.button("Atualizar", icon="🖕", use_container_width=True):
    with st.spinner('Aguarde...'):
        time.sleep(5)
    st.success("Done!")
st.divider()

aba1, aba2, aba3 = st.tabs(['Tabela de Falhas 📋', 'Indicadores 📊', 'Reincidências 📈'])
with aba1:
    df = tabela_falhas()
    df_mod = filtros_tabela(df)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Total de Falhas: ', df_mod['OSM'].count())
    with coluna2:
        st.metric('Total de Ocorrências: ', df_mod['OCORRÊNCIA'].count())
    st.dataframe(df_mod, hide_index=True)
with aba2:
    indicadores()
with aba3:
    st.title("Reincidencias")
