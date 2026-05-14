import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("Beira Alta Sistema de Produção")

# =========================
# FUNÇÃO DE LIMPEZA
# =========================

def limpar_colunas(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\n", " ")
    return df

# =========================
# UPLOAD OU ARQUIVO LOCAL
# =========================

st.sidebar.header("Atualizar arquivos")

estoque_file = st.sidebar.file_uploader("Upload Estoque.xlsx", type=["xlsx"])
pedido_file = st.sidebar.file_uploader("Upload Pedido.xlsx", type=["xlsx"])

# =========================
# BASE FIXA
# =========================

base = pd.read_excel("base_produtos.xlsx", header=1)
base = limpar_colunas(base)

# =========================
# ESTOQUE
# =========================

if estoque_file:
    estoque = pd.read_excel(estoque_file)
else:
    estoque = pd.read_excel("estoque.xlsx")

estoque = limpar_colunas(estoque)

# =========================
# PEDIDO
# =========================

if pedido_file:
    pedido = pd.read_excel(pedido_file)
else:
    pedido = pd.read_excel("pedido.xlsx")

pedido = limpar_colunas(pedido)

# =========================
# VALIDAÇÃO DE COLUNAS
# =========================

if "Cod. Cx" not in estoque.columns:
    st.error("Erro: coluna 'Cod. Cx' não encontrada no estoque.xlsx")
    st.stop()

if "Saldo Estoque" not in estoque.columns:
    st.error("Erro: coluna 'Saldo Estoque' não encontrada no estoque.xlsx")
    st.stop()

if "Cod. Cx" not in pedido.columns:
    st.error("Erro: coluna 'Cod. Cx' não encontrada no pedido.xlsx")
    st.stop()

if "Pedido" not in pedido.columns:
    st.error("Erro: coluna 'Pedido' não encontrada no pedido.xlsx")
    st.stop()

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
# GARANTIR COLUNAS
# =========================

if "Saldo Estoque" not in base.columns:
    base["Saldo Estoque"] = 0

if "Pedido" not in base.columns:
    base["Pedido"] = 0

# =========================
# PREENCHER NULOS
# =========================

base["Saldo Estoque"] = base["Saldo Estoque"].fillna(0)
base["Pedido"] = base["Pedido"].fillna(0)

# =========================
# NUMÉRICO
# =========================

base["Média de Venda 2025"] = pd.to_numeric(
    base["Média de Venda 2025"],
    errors="coerce"
).fillna(0)

base["Saldo Estoque"] = pd.to_numeric(
    base["Saldo Estoque"],
    errors="coerce"
).fillna(0)

base["Pedido"] = pd.to_numeric(
    base["Pedido"],
    errors="coerce"
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
# ORDEM DAS COLUNAS
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
    "Produzir",
    "Data produção",
    "Ordem",
    "Linha",
    "Lote",
    "QTD CX",
    "Necessidade S.A",
    "Volume",
    "Saldo após produção",
    "Saldo em dias após produção",
    "nº",
    "CURVA",
    "ESTOQUE CURVA ABC"
]

ordem = [c for c in ordem if c in base.columns]
base = base[ordem]

# =========================
# FORMATAR TABELA
# =========================

colunas_formatar = [
    "Média de Venda 2025",
    "Saldo Estoque",
    "Pedido",
    "Saldo Real",
    "Necessidade de P.A",
    "QTD CX",
    "Necessidade S.A",
    "Volume",
    "Saldo após produção",
    "ESTOQUE CURVA ABC"
]

for col in colunas_formatar:
    if col in base.columns:
        base[col] = (
            pd.to_numeric(base[col], errors="coerce")
            .fillna(0)
            .round(0)
            .astype(int)
            .map(lambda x: f"{x:,}".replace(",", "."))
        )

# =========================
# DIAS
# =========================

if "Saldo em dias" in base.columns:
    base["Saldo em dias"] = base["Saldo em dias"].round(1)

if "Saldo em dias após produção" in base.columns:
    base["Saldo em dias após produção"] = base["Saldo em dias após produção"].round(1)

# =========================
# EXIBIÇÃO
# =========================

st.dataframe(base, use_container_width=True, hide_index=True)

# =========================
# DOWNLOAD
# =========================

from io import BytesIO

output = BytesIO()

base.to_excel(output, index=False, engine="openpyxl")
output.seek(0)

st.download_button(
    "Baixar resultado",
    data=output,
    file_name="resultado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
