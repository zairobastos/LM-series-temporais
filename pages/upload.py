import streamlit as st
import pandas as pd

st.write("### Faça o upload do seu arquivo CSV com os dados da série temporal.")
st.write("O arquivo deve conter uma coluna chamada 'date' com as datas e outra coluna com os valores a serem previstos.")
st.write("Exemplo de formato do arquivo CSV:")
st.write("""
```
date,value
2023-01-01,100
2023-01-02,110
2023-01-03,120
```
""")
st.write("## Upload do Arquivo")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if uploaded_file is not None:
		# Lê o arquivo CSV
		try:
				df = pd.read_csv(uploaded_file)
				st.write("Arquivo carregado com sucesso!")
				st.write("Visualização dos dados:")
				st.dataframe(df.head())
		except Exception as e:
				st.error(f"Erro ao carregar o arquivo: {e}")