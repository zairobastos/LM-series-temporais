import streamlit as st
from src.model.metricas import Metricas
from src.view.grafico import Grafico
import ast

class Resultados:
	def __init__(self, val_exatos: list, val_previstos: str, qtd_tokens_prompt: int, qtd_tokens_resposta: int, tempo: float):
		"""
		Classe responsável por exibir os resultados.

		Args:
			val_exatos (list): Valores exatos.
			val_previstos (list): Valores previstos.
			qtd_tokens_prompt (int): Quantidade de tokens do prompt.
			qtd_tokens_resposta (int): Quantidade de tokens da resposta.
			tempo (float): Tempo de execução.
		"""
		self.val_exatos = val_exatos
		self.val_previstos = val_previstos
		self.qtd_tokens_prompt = qtd_tokens_prompt
		self.qtd_tokens_resposta = qtd_tokens_resposta
		self.tempo = tempo

	def exibir_resultados(self):
		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric(label='Tokens Prompt', value=self.qtd_tokens_prompt)
		with col2:
			st.metric(label='Tokens Resposta', value=self.qtd_tokens_resposta)
		with col3:
			st.metric(label='Tempo de Execução', value=f"{self.tempo:.2f} segundos")

		col4, col5, col6 = st.columns(3)
		with col4:
			print(self.val_previstos)
			print(type(self.val_previstos))
			smape = Metricas(y_pred=ast.literal_eval(self.val_previstos), y_true=self.val_exatos).smape()
			st.metric(label='SMAPE', value=smape)
		with col5:
			mae = Metricas(y_pred=ast.literal_eval(self.val_previstos), y_true=self.val_exatos).mae()
			st.metric(label='MAE', value=mae)
		with col6:
			rmse = Metricas(y_pred=ast.literal_eval(self.val_previstos), y_true=self.val_exatos).rmse()
			st.metric(label='RMSE', value=rmse)
		st.write('---')
		st.write('### Resultados')
		st.write("Valores Exatos")
		st.code(
			self.val_exatos,
			language='python',
			line_numbers=True,
		)
		st.write("Valores Previstos")
		st.code(
			self.val_previstos,
			language='python',
			line_numbers=True,
		)
		Grafico().grafico(self.val_exatos, self.val_previstos, smape)
		return smape, mae, rmse
