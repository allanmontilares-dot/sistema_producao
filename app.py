import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Sistema de Produção")

# =====================
# LEITURA DOS ARQUIVOS
# =====================

base = pd.read_excel("base_produtos.xlsx")
estoque = pd.read_excel("estoque.xlsx")
pedido = pd.read_excel("pedido.xlsx")

# =====================
# LIMPAR ESPAÇOS
# =====================

base.columns = base.columns.str.strip()
estoque.columns = estoque.columns.str.strip()
pedido.columns = pedido.columns.str.strip()

# =====================
# JUNTAR ESTOQUE
# =====================

base = base.merge(
    estoque[["Cod. Cx", "Saldo Estoque"]],
    on="Cod. Cx",
    how="left"
)

# =====================
# JUNTAR PEDIDOS
# =====================

base = base.merge(
    pedido[["Cod. Cx", "Pedido"]],
    on="Cod. Cx",
    how="left"
)

# =====================
# PREENCHER NULOS
# =====================

base["Saldo Estoque"] = base["Saldo Estoque"].fillna(0)
base["Pedido"] = base["Pedido"].fillna(0)

# =====================
# CALCULOS
# =====================

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

# =====================
# MOSTRAR
# =====================

st.dataframe(base, use_container_width=True)

# =====================
# DOWNLOAD
# =====================

arquivo_saida = "resultado.xlsx"

base.to_excel(arquivo_saida, index=False)

with open(arquivo_saida, "rb") as file:
    st.download_button(
        "Baixar Excel",
        file,
        file_name="resultado.xlsx"
    )
