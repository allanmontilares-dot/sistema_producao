# Criar o arquivo app.py
with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Beira Alta Sistema de Produção")

# Ler arquivos
base = pd.read_excel("base_produtos.xlsx")
estoque = pd.read_excel("estoque.xlsx")
pedidos = pd.read_excel("pedidos.xlsx")

# Juntar tabelas
df = base.merge(estoque, on="Cod. Cx", how="left")
df = df.merge(pedidos, on="Cod. Cx", how="left")

# Preencher vazios
df["Saldo Estoque"] = df["Saldo Estoque"].fillna(0)
df["Pedido"] = df["Pedido"].fillna(0)

# Calcular saldo real
df["Saldo Real"] = df["Saldo Estoque"] - df["Pedido"]

# Mostrar tabela
st.dataframe(df, use_container_width=True)
""")
