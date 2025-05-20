import streamlit as st

class Header:
	def __init__(self, dataset:str, modelo:str, data_inicio:str, data_fim:str, periodos:int, tipo_prompt: str):
		"""
		Classe responsável por criar o cabeçalho da aplicação.
		Esta classe é utilizada para definir os parâmetros de entrada do usuário, como o dataset, modelo, datas de início e fim,
		número de períodos e tipo de prompt.

		Args:
				dataset (str): Base de dados a ser utilizada. Ex: 'ETTH1', 'ETTH2'.
				modelo (str): Modelo a ser utilizado. Ex: 'deepseek-r1-distill-qwen-32b'.
				data_inicio (str): Data de início da previsão. Ex: '2016-07-01'.
				data_fim (str): Data de fim da previsão. Ex: '2016-07-02'.
				periodos (int): Número de períodos a serem previstos. Ex: 1.
				tipo_prompt (str): Tipo de prompt a ser utilizado. Ex: 'ZERO-SHOT', 'FEW-SHOT', 'COT', 'COT-FEW'.
		"""
		self.dataset = dataset
		self.modelo = modelo
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.periodos = periodos
		self.tipo_prompt = tipo_prompt

	def header(self):
		st.write("### Análise dos dados")

		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric(label="Base de Dados", value=self.dataset)
		with col2:
			st.metric(label="Modelo", value=self.modelo)
		with col3:
			st.metric(label="Tipo de Prompt", value=self.tipo_prompt)

		col4, col5, col6 = st.columns(3)
		with col4:
			st.metric(label="Data de Início", value=self.data_inicio)
		with col5:
			st.metric(label="Data de Fim", value=self.data_fim)
		with col6:
			st.metric(label="Períodos", value=self.periodos)
