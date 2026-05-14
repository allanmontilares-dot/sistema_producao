import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Sistema de Produção")

# =========================
# LEITURA DOS ARQUIVOS
# =========================

base = pd.read_excel("base_produtos.xlsx", header=1)
estoque = pd.read_excel("estoque.xlsx")
pedido = pd.read_excel("pedido.xlsx")

# =========================
# LIMPAR ESPAÇOS
# =========================

base.columns = base.columns.str.strip()
estoque.columns = estoque.columns.str.strip()
pedido.columns = pedido.columns.str.strip()

# =========================
# REMOVER COLUNAS ANTIGAS
# =========================

colunas_remover = [
    "Saldo Estoque",
    "Pedido",
    "Saldo Real",
    "Saldo em dias",
    "Necessidade de P.A"
]

for coluna in colunas_remover:
    if coluna in base.columns:
        base = base.drop(columns=[coluna])

# =========================
# MERGE ESTOQUE
# =========================

base = base.merge(
    estoque[["Cod. Cx", "Saldo Estoque"]],
    on="Cod. Cx",
    how="left"
)

# =========================
# MERGE PEDIDO
# =========================

base = base.merge(
    pedido[["Cod. Cx", "Pedido"]],
    on="Cod. Cx",
    how="left"
)

# =========================
# PREENCHER NULOS
# =========================

base["Saldo Estoque"] = base["Saldo Estoque"].fillna(0)
base["Pedido"] = base["Pedido"].fillna(0)

# =========================
# CONVERTER PARA NUMÉRICO
# =========================

colunas_numericas = [
    "Média de Venda 2025",
    "Saldo Estoque",
    "Pedido"
]

for coluna in colunas_numericas:
    base[coluna] = pd.to_numeric(
        base[coluna],
        errors="coerce"
    ).fillna(0)

# =========================
# CÁLCULOS
# =========================

base["Saldo Real"] = (
    base["Saldo Estoque"] - base["Pedido"]
)

base["Saldo em dias"] = (
    base["Saldo Real"] / base["Média de Venda 2025"]
)

base["Necessidade de P.A"] = (
    base["Média de Venda 2025"] - base["Saldo Real"]
)

base["Necessidade de P.A"] = (
    base["Necessidade de P.A"].clip(lower=0)
)

# =========================
# ORGANIZAR COLUNAS
# =========================

ordem_colunas = [
    "Cod. Cx",
    "Descrição",

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

# mantém apenas colunas existentes
ordem_colunas = [
    col for col in ordem_colunas
    if col in base.columns
]

base = base[ordem_colunas]

# =========================
# FORMATAR NÚMEROS
# =========================

colunas_formatadas = [
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

for coluna in colunas_formatadas:
    if coluna in base.columns:
        base[coluna] = (
    pd.to_numeric(base[coluna], errors="coerce")
    .fillna(0)
    .round(0)
    .astype(int)
    .map(lambda x: f"{x:,}".replace(",", "."))
)

# =========================
# FORMATAR DIAS
# =========================

if "Saldo em dias" in base.columns:
    base["Saldo em dias"] = (
        base["Saldo em dias"]
        .round(1)
    )

if "Saldo em dias após produção" in base.columns:
    base["Saldo em dias após produção"] = (
        base["Saldo em dias após produção"]
        .round(1)
    )

# =========================
# MOSTRAR TABELA
# =========================

st.dataframe(
    base,
    use_container_width=True,
    hide_index=True
)

# =========================
# DOWNLOAD EXCEL
# =========================

arquivo_saida = "resultado.xlsx"

base.to_excel(arquivo_saida, index=False)

with open(arquivo_saida, "rb") as file:
    st.download_button(
        label="Baixar Excel",
        data=file,
        file_name="resultado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
