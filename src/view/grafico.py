import streamlit as st
import os
from datetime import date
import plotly.graph_objects as go
import ast

class Grafico:
	def amostragem(self,dados_prompt: list):
		st.write('### Gráfico Série Temporal - Prompt')
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=list(range(len(dados_prompt))), y=dados_prompt, mode='lines', name='Série Temporal'))
		fig.update_layout(
			title='Série Temporal - Prompt',
			xaxis_title='Períodos',
			yaxis_title='Valores',
			colorway=['#1f77b4'],
			showlegend=True,
		)
		st.plotly_chart(fig, use_container_width=True)
		st.write('---')

	def grafico(self, dados_reais: list, dados_previstos:list, smape: float):
		dados_previstos = ast.literal_eval(dados_previstos)
		st.write('### Gráfico Série Temporal - Previsão')
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=list(range(len(dados_reais))), y=dados_reais, mode='lines', name='Valores Reais'))
		fig.add_trace(go.Scatter(x=list(range(len(dados_previstos))), y=dados_previstos, mode='lines', name='Valores Previsto'))
		fig.update_layout(
			title=f'Série Temporal - Previsão / SMAPE = {smape}',
			xaxis_title='Períodos',
			yaxis_title='Valores',
			colorway=['#1f77b4', '#ff7f0e'],
			showlegend=True,
			height=600
		)
		st.plotly_chart(fig, use_container_width=True)