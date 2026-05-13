# Criar o arquivo app.py
with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd

st.title("Meu Sistema de Produção")

# Upload das planilhas
estoque_file = st.file_uploader("Escolha a planilha de Estoque", type=["xlsx","csv"])
pedido_file = st.file_uploader("Escolha a planilha de Pedidos", type=["xlsx","csv"])
insumo_file = st.file_uploader("Escolha a planilha de Insumos", type=["xlsx","csv"])

# Exibir dados carregados
if estoque_file is not None:
    st.subheader("Estoque")
    estoque_df = pd.read_excel(estoque_file)
    st.dataframe(estoque_df)

if pedido_file is not None:
    st.subheader("Pedidos")
    pedido_df = pd.read_excel(pedido_file)
    st.dataframe(pedido_df)

if insumo_file is not None:
    st.subheader("Insumos")
    insumo_df = pd.read_excel(insumo_file)
    st.dataframe(insumo_df)
""")