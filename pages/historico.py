import streamlit as st
from database.crud_database import Crud
import os
from src.view.grafico import Grafico

with st.sidebar:
	st.write(" ### 🔍 Parâmetros da Busca")

	lista_datasets = os.listdir('data')

	dataset = st.selectbox('Base de Dados', lista_datasets)

	confirma = st.button(label='Visualizar Previsões', help='Clique para gerar a análise de dados',type='primary', use_container_width=True)
	

if confirma:
	dados = Crud().select(
		table=dataset[:-4]
	)
	c=1
	for dado in dados:
		val_exatos = list(map(float, dado[8].strip('[]').split(',')))
		val_previstos = dado[9]
		smape = dado[10]
		Grafico().grafico(
			dados_previstos=val_previstos,
			dados_reais=val_exatos,
			smape=smape,
			key=c
		)
		st.markdown(
			"""
			<style>
				.full-width-table {
					width: 100%;
					border-collapse: collapse;
				}
				.full-width-table th, .full-width-table td {
					padding: 8px;
					text-align: left;
					font-size: 18px;
				}
				.full-width-table th {
					text-align: center;
					background-color: #333;
					color: #fff;
				}
				.centered {
					text-align: center;
					background-color: #333;
					color: #fff;
					font-weight: bold;
				}
				.full-width-table tr:nth-child(even) {
					background-color: #444;
				}
				.full-width-table tr:nth-child(odd) {
					background-color: #666;
				}
				.full-width-table td {
					color: #fff;
					font-weight: bold;
				}
			</style>
			""",
			unsafe_allow_html=True
			)

		st.markdown(
			f"""
			<table class="full-width-table">
				<thead>
					<tr>
						<th colspan="2" class="centered">Parâmetros do Prompt</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Data de início</td>
						<td>{str(dado[1])}</td>
					</tr>
					<tr>
						<td>Data de término</td>
						<td>{str(dado[2])}</td>
					</tr>
					<tr>
						<td>Períodos</td>
						<td>{int(dado[3])}</td>
					</tr>
					<tr>
						<td>Tipo do Prompt</td>
						<td>{str(dado[7])}</td>
					</tr>
					<tr>
						<th colspan="2" class="centered">Parâmetros da API</th>
					</tr>
					<tr>
						<td>Modelo</td>
						<td>{str(dado[4])}</td>
					</tr>
					<tr>
						<td>Temperatura da Resposta</td>
						<td>{str(dado[5])}</td>
					</tr>
					<tr>
						<td>Quantidade de Tokens do Prompt</td>
						<td>{str(dado[12])}</td>
					</tr>
					<tr>
						<td>Quantidade de tokens da Resposta</td>
						<td>{str(dado[11])}</td>
					</tr>
					<tr>
						<td>Total de Tokens</td>
						<td>{str(dado[13])}</td>
					</tr>
					<tr>
						<th colspan="2" class="centered">Resultados da Consulta</th>
					</tr>
					<tr>
						<td>SMAPE</td>
						<td>{dado[10]}</td>
					</tr>
					<tr>
						<td>Valores Previstos</td>
						<td>{dado[9]}</td>
					</tr>
				</tbody>
			</table>
		""",
		unsafe_allow_html=True)
		st.write("### Prompt")
		st.code(dado[6], language='python', line_numbers=True)
		c+=1
		st.write('---')
		

