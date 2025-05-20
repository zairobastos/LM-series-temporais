import streamlit as st

from src.model.dados_model import DadosModel

class Dataset:
	def __init__(self, dataset:str, data_inicio:str, data_fim:str, qtd_periodos:int):
		"""
		Classe responsável por manipular o dataset.

		Args:
			dataset (str): Dataset a ser manipulado.
			data_inicio (str): Data de início do dataset.
			data_fim (str): Data de fim do dataset.
			qtd_periodos (int): Quantidade de períodos a serem previstos.
		"""
		self.dataset = dataset
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.qtd_periodos = qtd_periodos*24

	def exibir_dados(self):
		dataset = DadosModel(dataset=self.dataset, data_inicio=self.data_inicio, data_fim=self.data_fim, qtd_periodos=self.qtd_periodos)
		df_selecionado, df_exatos = dataset.selecao_periodo()
		st.write("### Dados Selecionados")
		st.dataframe(df_selecionado, use_container_width=True)
		st.write("### Dados Exatos")
		st.dataframe(df_exatos, use_container_width=True)
