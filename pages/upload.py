import streamlit as st
import pandas as pd
import os

st.write("### Faça o upload do seu arquivo CSV com os dados da série temporal.")
st.write("O arquivo deve conter uma coluna chamada 'date' com as datas e outra coluna com os valores a serem previstos.")
st.write("Exemplo de formato do arquivo CSV:")
st.code("""
date,value
2023-01-01,100
2023-01-02,110
2023-01-03,120
""", language='python', line_numbers=True)

st.write("## Upload do Arquivo")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

@st.dialog("Seleção de coluna")
def selecao_coluna(dataset, uploaded_file):
	lista_colunas = dataset.columns.tolist()
	data = st.selectbox("Selecione a coluna para a data:", lista_colunas)
	valor = st.selectbox("Selecione a coluna de valores:", lista_colunas)

	if data == valor:
		st.warning("As colunas devem ser diferentes.")

	if st.button("Confirmar"):
		st.session_state.selecao_coluna = {"data": data, "valor": valor}
		st.session_state.arquivo_selecionado = uploaded_file.name  # salva nome do arquivo

		# Salvar o arquivo na pasta 'data' somente após confirmar
		file_path = f"data/{uploaded_file.name}"
		if not os.path.isfile(file_path):
			df = dataset[[data,valor]]
			df.rename(columns={data: "date", valor: "value"}, inplace=True)
			df.to_csv(file_path, index=False)
			st.success(f"Arquivo salvo em '{file_path}'", icon="✅")
		else:
			st.warning(f"Arquivo já existe em '{file_path}'.", icon="⚠️")

		st.rerun()

if uploaded_file is not None:
	try:
		df = pd.read_csv(uploaded_file)
		st.toast("Arquivo carregado com sucesso!", icon="✅")

		# Verifica se é um novo arquivo para resetar seleção
		if (
			"arquivo_selecionado" in st.session_state
			and st.session_state.arquivo_selecionado != uploaded_file.name
		):
			st.session_state.pop("selecao_coluna", None)
			st.session_state.pop("arquivo_selecionado", None)

		if "selecao_coluna" not in st.session_state:
			selecao_coluna(df, uploaded_file)
		else:
			sel = st.session_state.selecao_coluna

	except Exception as e:
		st.error(f"Erro ao carregar o arquivo: {e}", icon="🚨")

		
# Diálogo de confirmação
@st.dialog(f"Exclusão do dataset")
def confirmar_remocao(dataset):
	opcao = st.radio(f'Deseja realmente excluir o {dataset}:', ("Sim", "Não"))
	if st.button("Confirmar Exclusão"):
		if opcao == "Sim":
			try:
				os.remove(f"data/{dataset}")
				st.success(f"Dataset '{dataset}' removido com sucesso!", icon="✅")
			except FileNotFoundError:
				st.error("Arquivo não encontrado.", icon="🚨")
			except Exception as e:
				st.error(f"Erro ao remover: {e}", icon="🚨")
		else:
			st.warning("Operação cancelada.", icon="⚠️")

# Sidebar
with st.sidebar:
	st.write("## Datasets Disponíveis")
	lista_datasets = os.listdir("data")
	if lista_datasets:
		for dataset in lista_datasets:
			st.write(f"📊 {dataset.upper()}")
		st.write("## Remover um dataset:")
		dataset_remover = st.selectbox("Escolha um dataset para remover:", lista_datasets if lista_datasets else ["Nenhum disponível"])
		if lista_datasets and st.button("Remover Dataset"):
			confirmar_remocao(dataset_remover)
	else:
		st.write("Nenhum dataset disponível.")

