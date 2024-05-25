import streamlit as st
import pandas as pd

# Exemplo de DataFrame
data = {
    'id': [1, 2, 3],
    'info': [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 35}]
}
df = pd.DataFrame(data)

# Exibir a coluna 'info'
st.write(df['info'])

# Expandir a coluna 'info' em colunas separadas
df_expanded = pd.json_normalize(df['info'])
df_combined = df.join(df_expanded)

st.write(df_expanded)

st.write(df_combined)

# Acessar o campo 'name' de cada dicionário na coluna 'info'
df['name'] = df['info'].apply(lambda x: x['name'])

st.write(df)
