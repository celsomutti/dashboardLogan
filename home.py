import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard",page_icon="./asserts/icon_Logan.png")
col5, col6 = st.columns(2)

with col5: 
    st.image("logo_Logan_188_138.png")

with col6: 
    st.write("# Dashboard")

btn = st.button("Clique aqui pra visualizar os dados")

@st.cache_data
def dataBuild():
    if "data" not in st.session_state:
        df_data= pd.read_csv("dados.csv", sep=";", index_col=False, dtype='unicode')
        st.session_state["data"] = df_data
        
dataBuild()

col1, col2, col3 = st.columns(3)
    
def showGraphicPieEntregas(df_data):
    df_data=df_data[(df_data['Situacao Entrega'] == "ENTREGA REALIZADA") | 
        (df_data['Situacao Entrega'] == "INSUCESSO DE ENTREGA") & 
        (df_data['Tipo Operacao'] == "ENTREGA")]
    fig = px.pie(df_data, values="Qtde Volumes", names='Situacao Entrega', title="Entregas",)
    st.plotly_chart(fig, theme=None)

def showGraphicPieReversas(df_data):
    df_data=df_data[(df_data['Situacao Entrega'] == "ENTREGA REALIZADA") | 
        (df_data['Situacao Entrega'] == "INSUCESSO DE ENTREGA") & 
        (df_data['Tipo Operacao'] == "REVERSA")]
    fig = px.pie(df_data, values="Qtde Volumes", names='Situacao Entrega', title="Reversas",)
    st.plotly_chart(fig, theme=None)

def showGraphicPieDevolucoes(df_data):
    df_data=df_data[(df_data['Situacao Entrega'] == "ENTREGA REALIZADA") | 
        (df_data['Situacao Entrega'] == "INSUCESSO DE ENTREGA") & 
        (df_data['Tipo Operacao'] == "DEVOLUÇÃO")]
    fig = px.pie(df_data, values="Qtde Volumes", names='Situacao Entrega', title="Devoluções",)
    st.plotly_chart(fig, theme=None)

def showGraphicBarPedidosEntregues(df_data):
    df_data=df_data[(df_data['Situacao Entrega'] == "ENTREGA REALIZADA") & 
        (df_data['Tipo Operacao'] == "ENTREGA")]
    df_data['Data Entrega'] = df_data['Data Entrega'].astype('datetime64[ns]')
    df_data['quantidade_itens'] = df_data["Qtde Volumes"].astype('int')
    df_data['mes_ano'] = df_data['Data Entrega'].map(lambda x: x.month)
    
    df_data = df_data.groupby(['mes_ano']).count().reset_index()

    #df_data.groupby(pd.Grouper(key="Data Entrega", freq="M")).count()
    st.write('Pedidos Processados')
    st.write(' ')
    st.bar_chart(data=df_data, x='mes_ano', y='quantidade_itens', x_label='Mês', y_label='Quantidade', stack=False)

def showGraphicBar(df_data):
    df_data=df_data[df_data['Ocorrencia'] != "REALIZADA"]
    df_data=df_data[df_data['Ocorrencia'] != "RETIRADO"]
    st.bar_chart(data=df_data, x="Ocorrencia", y="Qtde Volumes", stack=False, horizontal=True)

if btn:
    df = st.session_state["data"]
    with col1:
        showGraphicPieEntregas(df)
    with col2:
        showGraphicPieReversas(df)
    with col3:
        showGraphicPieDevolucoes(df)
    showGraphicBarPedidosEntregues(df)
        
    
    

