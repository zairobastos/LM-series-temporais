import streamlit as st
import os
from datetime import date
import plotly.graph_objects as go

class Grafico:
	def amostragem(self,dados_prompt: list):
		st.write('### Gráfico Série Temporal - Prompt')
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=list(range(len(dados_prompt))), y=dados_prompt, mode='lines', name='Série Temporal'))
		fig.update_layout(
			title='Série Temporal - Prompt',
			xaxis_title='Períodos',
			yaxis_title='Valores',
			showlegend=True,
		)
		st.plotly_chart(fig, use_container_width=True)
		st.write('---')