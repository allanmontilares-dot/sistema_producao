import streamlit as st
import os

st.title("Teste de Arquivos")

arquivos = os.listdir()

st.write(arquivos)
