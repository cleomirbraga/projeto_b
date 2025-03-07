import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px 
import matplotlib.pyplot as plt

# Carregamento da base
df_total = pd.read_csv("df_total.csv")

st.set_page_config(layout="wide")

# Layout com colunas
col1, col2 = st.columns([1, 2])  # A largura da coluna da imagem é menor que a do conteúdo

with col1:
    # Logo Bemol
    st.image("logo.jpg", width=300)

with col2:
    # Título
    st.title("Dashboard - Produtos Financeiros")

    # Cartões de Medidas
    total_clientes = df_total["ID_PESSOA"].nunique()
    total_lojas = df_total["NUM_LOJA"].nunique()
    valor_total_transacoes = df_total["VALOR_TRANSACAO"].sum()
    total_cidades = df_total["CIDADE"].nunique()

    col2_1, col2_2, col2_3, col2_4 = st.columns(4)
    with col2_1:
        st.metric(label="Total de Clientes", value=f"{total_clientes:,}")
    with col2_2:
        st.metric(label="Total de Lojas", value=total_lojas)
    with col2_3:
        st.metric(label="Valor Total de Transações (R$)", value=f"{valor_total_transacoes:,.2f}")
    with col2_4:
        st.metric(label="Total de Cidades", value=total_cidades)

st.markdown("---")

# Paleta de cores Bemol
paleta_bemol = ["#2091CB", "#DD3836"]

# Ajustando colunas para gráficos e separadores
col3, col4, col5, col6, col7= st.columns([0.5, 0.05, 0.5, 0.05, 0.5])

# Gráfico de Rosca: Transações por Produto
with col3:
    transacoes_por_produto = (
        df_total.groupby("PRODUTO")["VALOR_TRANSACAO"]
        .sum()
        .reset_index()
        .rename(columns={"VALOR_TRANSACAO": "Valor Total"})
    )
    fig_pie = px.pie(
        transacoes_por_produto,
        values="Valor Total",
        names="PRODUTO",
        title="Produto x Transação",
        hole=0.30,
        color_discrete_sequence=paleta_bemol,
        height=400,
    )
    fig_pie.update_traces(textinfo="value", textfont_size=14) 
    fig_pie.update_layout(title={'x': 0.20}) 
    st.plotly_chart(fig_pie, use_container_width=True)

# Separador visual
with col4:
    st.markdown("<div style='border-left: 1px solid grey; height: 400px;'></div>", unsafe_allow_html=True)

# Gráfico de Barras: Localização x Produto
with col5:
    produtos_x_localizacao = (
        df_total.groupby(["LOCALIZAÇÃO", "PRODUTO"])["ID_PESSOA"]
        .nunique()
        .reset_index(name="QUANTIDADE")
    )
    fig_bar1 = px.bar(
        produtos_x_localizacao,
        x="PRODUTO",
        y="QUANTIDADE",
        color="LOCALIZAÇÃO",
        title="Localização x Produto",
        labels={"QUANTIDADE": "Número de Clientes", "PRODUTO": "Produto"},
        color_discrete_sequence=paleta_bemol,
        text_auto=True,
        height=400,  # Define a altura do gráfico
    )
    fig_bar1.update_layout(title={'x': 0.23})
    st.plotly_chart(fig_bar1, use_container_width=True)

# Separador visual
with col6:
    st.markdown("<div style='border-left: 1px solid grey; height: 400px;'></div>", unsafe_allow_html=True)

# Gráfico de Barras: Transações por Localização e Produto
with col7:
    produtos_x_localizacao2 = (
        df_total.groupby(["LOCALIZAÇÃO", "PRODUTO"])
        .size()
        .reset_index(name="QUANTIDADE")
    )
    fig_bar2 = px.bar(
        produtos_x_localizacao2,
        x="PRODUTO",
        y="QUANTIDADE",
        color="LOCALIZAÇÃO",
        title="Transações por Localização e Produto",
        labels={"QUANTIDADE": "Número de Transações", "PRODUTO": "Produto"},
        color_discrete_sequence=paleta_bemol,
        text_auto=True,
        height=400,  
    )
    fig_bar2.update_layout(title={'x': 0.18})
    st.plotly_chart(fig_bar2, use_container_width=True)

st.markdown("---")

col8, col9, col10 = st.columns([1, 0.05, 1])

with col8:
    # Cálculo
    digital = df_total[df_total["PRODUTO"] == "RECARGA_DIGITAL"]["ID_PESSOA"].nunique()
    pre_pago = df_total[df_total["PRODUTO"] == "VALE_PRE_PAGO"]["ID_PESSOA"].nunique()
    digital_e_pre_pago = df_total[df_total["PRODUTO"].isin(["RECARGA_DIGITAL", "VALE_PRE_PAGO"])].groupby("ID_PESSOA")["PRODUTO"].nunique()
    digital_e_pre_pago = digital_e_pre_pago[digital_e_pre_pago > 1].count()

    # Dados para o gráfico
    produtos = ["Usam Recarga Digital", "Usam Vale Pré-Pago", "Ambos"]
    quantidades = [digital, pre_pago, digital_e_pre_pago]
    cores = ["#DD3836", "#2091CB", "#CDCDCD"]
    
    # Criando df do gráfico
    df_col8 = pd.DataFrame({
        "Produto": produtos,
        "Quantidade": quantidades
    })

    # Criando o gráfico de barras
    fig_bar3 = px.bar(
        df_col8,
        x="Produto",
        y="Quantidade",
        title="N° Clientes por Produto",
        labels={"Quantidade": "Número de Clientes", "Produto": "Tipo de Produto"},
        color="Produto",  # Define as cores com base na coluna Produto
        color_discrete_map={
            "Usam Recarga Digital": "#DD3836",  
            "Usam Vale Pré-Pago": "#2091CB",   
            "Ambos": "#CDCDCD",               
        },
        text_auto=True,
        height=400,  # Define a altura do gráfico
    )
    # Exibindo o gráfico no Streamlit
    fig_bar3.update_layout(title={'x': 0.30})
    st.plotly_chart(fig_bar3, use_container_width=True)

# Separador visual
with col9:
    st.markdown("<div style='border-left: 1px solid grey; height: 400px;'></div>", unsafe_allow_html=True)

with col10:
  # Cálculo
  somente_digital = df_total[~df_total["ID_PESSOA"].isin(df_total[df_total["PRODUTO"] == "VALE_PRE_PAGO"]["ID_PESSOA"])]["ID_PESSOA"].nunique()
  somente_pre = df_total[~df_total["ID_PESSOA"].isin(df_total[df_total["PRODUTO"] == "RECARGA_DIGITAL"]["ID_PESSOA"])]["ID_PESSOA"].nunique()

  # Dados para o gráfico
  dados = {
      "Produto": ["Recarga Digital", "Vale Pré-Pago"],
      "Quantidade": [somente_digital, somente_pre]
  } 
  df_grafico = pd.DataFrame(dados)

  # Criação do gráfico de barras horizontal
  fig = px.bar(
      df_grafico,
      y="Produto",
      x="Quantidade",
      orientation="h",  
      title="N° de Clientes que Utilizam Somente um dos Produto",
      labels={"Quantidade": "Número de Pessoas", "Produto": "Tipo de Produto"},
      color="Produto",
      color_discrete_sequence=["#DD3836", "#2091CB"], 
      text="Quantidade",  
      height=400  
  )

  # plotar
  fig.update_layout(title={'x': 0.20})
  st.plotly_chart(fig, use_container_width=True)  

st.markdown("---")

col11, col12, col13= st.columns([1, 0.05, 1])

with col11:
  # Nivel do Cliente x Produto - Contagem pelo ID_PESSOA
  cliente_x_produto = df_total.groupby(["PRODUTO", "NIVEL_CLIENTE"])["ID_PESSOA"].nunique().reset_index(name="QUANTIDADE")

  # Gráfico de Barras: Nível do Cliente x Produto
  fig_cliente_produto = px.bar(
      cliente_x_produto,
      x="NIVEL_CLIENTE",
      y="QUANTIDADE",
      color="PRODUTO",  # Diferencia as barras por produto
      barmode="group",  # Escolha entre "group" (agrupado) ou "stack" (empilhado)
      title="Nível do Cliente x Produto",
      labels={"QUANTIDADE": "Número de Clientes", "NIVEL_CLIENTE": "Nível do Cliente", "PRODUTO": "Produto"},
      color_discrete_sequence=["#DD3836", "#2091CB"],  
      text_auto=True,
      height=400  # Define a altura do gráfico
  )
  # Exibindo o gráfico no Streamlit
  fig_cliente_produto.update_layout(title={'x': 0.20})
  st.plotly_chart(fig_cliente_produto, use_container_width=True)

# Separador visual
with col12:
    st.markdown("<div style='border-left: 1px solid grey; height: 400px;'></div>", unsafe_allow_html=True)

with col13:
    # Nível do Cliente x Produto (n° transações) - Contagem pelo ID_PESSOA
    cliente_x_produto_transacoes = df_total.groupby(["PRODUTO", "NIVEL_CLIENTE"]).size().reset_index(name="QUANTIDADE")

    # Gráfico de Barras: Nível do Cliente x Produto
    fig_cliente_produto_transacoes = px.bar(
        cliente_x_produto_transacoes,
        x="NIVEL_CLIENTE",
        y="QUANTIDADE",
        color="PRODUTO",  
        barmode="group",  
        title="Nível do Cliente x Produto (N° de Transações)",
        labels={"QUANTIDADE": "Número de Transações", "NIVEL_CLIENTE": "Nível do Cliente", "PRODUTO": "Produto"},
        color_discrete_sequence=["#DD3836", "#2091CB"], 
        text_auto=True,
        height=400  
    )
    
    # Exibindo o gráfico no Streamlit
    fig_cliente_produto_transacoes.update_layout(title={'x': 0.20})  # Centraliza o título no gráfico
    st.plotly_chart(fig_cliente_produto_transacoes, use_container_width=True)


st.markdown("---")

# Rodapé
st.markdown("<p style='text-align: center; color: grey;'>Dashboard criado com Streamlit por Cleomir Braga | Dados: Bemol</p>", unsafe_allow_html=True)
