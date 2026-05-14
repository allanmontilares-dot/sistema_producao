import streamlit as st
import pandas as pd

st.title("Teste de Colunas")

base = pd.read_excel("base_produtos.xlsx")
estoque = pd.read_excel("estoque.xlsx")
pedido = pd.read_excel("pedido.xlsx")

st.write("COLUNAS BASE:")
st.write(base.columns.tolist())

st.write("COLUNAS ESTOQUE:")
st.write(estoque.columns.tolist())

st.write("COLUNAS PEDIDO:")
st.write(pedido.columns.tolist())
