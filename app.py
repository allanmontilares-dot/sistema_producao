import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Beira Alta Sistema de Produção")

# =========================
# LEITURA
# =========================

base = pd.read_excel("base_produtos.xlsx", header=1)
estoque = pd.read_excel("estoque.xlsx")
pedido = pd.read_excel("pedido.xlsx")

# =========================
# LIMPEZA DE CHAVE
# =========================

def norm(df):
    df.columns = df.columns.str.strip()
    df["Cod. Cx"] = df["Cod. Cx"].astype(str).str.strip()
    return df

base = norm(base)
estoque = norm(estoque)
pedido = norm(pedido)

# =========================
# GARANTIR NUMÉRICO
# =========================

base["Média de Venda 2025"] = pd.to_numeric(base["Média de Venda 2025"], errors="coerce").fillna(0)
estoque["Saldo Estoque"] = pd.to_numeric(estoque["Saldo Estoque"], errors="coerce").fillna(0)
pedido["Pedido"] = pd.to_numeric(pedido["Pedido"], errors="coerce").fillna(0)

# =========================
# MERGE (PROCV LIMPO)
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
# CÁLCULOS (REGRA DE NEGÓCIO)
# =========================

base["Saldo Real"] = base["Saldo Estoque"] - base["Pedido"]

base["Saldo em dias"] = base.apply(
    lambda x: x["Saldo Real"] / x["Média de Venda 2025"]
    if x["Média de Venda 2025"] > 0 else 0,
    axis=1
)

base["Necessidade de P.A"] = (
    base["Média de Venda 2025"] - base["Saldo Real"]
)

base["Necessidade de P.A"] = base["Necessidade de P.A"].clip(lower=0)

# =========================
# PRODUÇÃO SUGERIDA (opcional mas útil)
# =========================

base["Produzir"] = base["Necessidade de P.A"]

# =========================
# ORDEM FINAL (SEM QUEBRAR COLUNA)
# =========================

ordem = [
    "Cod. Cx",
    "Descrição",
    "Média de Venda 2025",
    "Saldo Estoque",
    "Pedido",
    "Saldo Real",
    "Saldo em dias",
    "Necessidade de P.A",
    "Produzir"
]

ordem = [c for c in ordem if c in base.columns]
base = base[ordem]

# =========================
# OUTPUT
# =========================

st.dataframe(base, use_container_width=True)
