def limpar_colunas(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\n", " ")
    return df
