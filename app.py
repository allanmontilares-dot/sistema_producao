import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("Beira Alta Sistema de Produção")

# =========================
# UPLOAD DOS ARQUIVOS
# =========================

st.sidebar.header("Atualizar arquivos")

estoque_file = st.sidebar.file_uploader("Upload Estoque.xlsx", type=["xlsx"])
pedido_file = st.sidebar.file_uploader("Upload Pedido.xlsx", type=["xlsx"])

# =========================
# BASE FIXA (do repositório)
# =========================

base = pd.read_excel("base_produtos.xlsx", header=1)

# =========================
# LER ESTOQUE
# =========================

if estoque_file:
    estoque = pd.read_excel(estoque_file)
else:
    estoque = pd.read_excel("estoque.xlsx")

# =========================
# LER PEDIDO
# =========================

if pedido_file:
    pedido = pd.read_excel(pedido_file)
else:
    pedido = pd.read_excel("pedido.xlsx")

# =========================
# LIMPEZA
# =========================

base.columns = base.columns.str.strip()
estoque.columns = estoque.columns.str.strip()
pedido.columns = pedido.columns.str.strip()

# =========================
# MERGE
# =========================

base = base.merge(
    estoque[["Cod. Cx", "Saldo Estoque"]],
    on="Cod. Cx",
    how="left"
)

base = base.merge(
    pedido[["Cod. Cx", "Pedido"]],
    on="Cod. Cx",
    how="left"
)

# =========================
# NULOS
# =========================

base["Saldo Estoque"] = base["Saldo Estoque"].fillna(0)
base["Pedido"] = base["Pedido"].fillna(0)

# =========================
# NUMÉRICO
# =========================

base["Média de Venda 2025"] = pd.to_numeric(
    base["Média de Venda 2025"], errors="coerce"
).fillna(0)

# =========================
# CÁLCULOS
# =========================

base["Saldo Real"] = base["Saldo Estoque"] - base["Pedido"]

base["Saldo em dias"] = base["Saldo Real"] / base["Média de Venda 2025"]

base["Necessidade de P.A"] = (
    base["Média de Venda 2025"] - base["Saldo Real"]
).clip(lower=0)

# =========================
# ORDEM
# =========================

ordem = [
    "Cod. Cx",
    "Descrição",
    "Média de Venda 2025",
    "Saldo Estoque",
    "Pedido",
    "Saldo Real",
    "Saldo em dias",
    "Necessidade de P.A"
]

ordem = [c for c in ordem if c in base.columns]
base = base[ordem]

# =========================
# MOSTRAR
# =========================

st.dataframe(base, use_container_width=True, hide_index=True)

# =========================
# DOWNLOAD
# =========================

st.download_button(
    "Baixar resultado",
    data=base.to_excel(index=False),
    file_name="resultado.xlsx"
)
