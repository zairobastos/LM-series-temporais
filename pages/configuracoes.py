import streamlit as st
from dotenv import set_key
import os

ENV_PATH = ".env"

# Inicializa o estado se ainda não estiver definido
if "modo" not in st.session_state:
	st.session_state.modo = "lm"  # padrão: LM Studio
st.write("### API")
col1, col2 = st.columns(2)

with col1:
	if st.button(
		"LM Studio",
		help="Acesse o LM Studio para executar modelos de linguagem localmente.",
		use_container_width=True,
		type="primary",
	):
		st.session_state.modo = "lm"

with col2:
	if st.button(
		"OpenAI / Ollama",
		help="Acesse a API para executar modelos de linguagem remotamente.",
		use_container_width=True,
		type="primary",
	):
		st.session_state.modo = "api"

# Exibição condicional
if st.session_state.modo == "lm":
		st.write(
			"Você será redirecionado para o LM Studio. Caso não tenha o LM Studio instalado, "
			"você pode baixá-lo [aqui](https://lmstudio.ai)."
		)
		st.markdown("Cadastre seu modelo do LM Studio")
		modelo = st.text_input(
			"Modelo",
			help="Digite o nome do modelo que deseja utilizar no LM Studio.",
			placeholder="Ex: deepseek-r1"
		)
		salvar = st.button(
			"💾 Salvar Configurações",
			help="Clique para salvar as configurações.",
			type="primary",
		)

elif st.session_state.modo == "api":
	st.write(
		"Você será redirecionado para a API. Caso não tenha uma chave de API, "
		"você pode obter uma [aqui](https://platform.openai.com/signup)."
	)
	chave_api = st.text_input(
		"Chave da API",
		help="Digite a chave da API que deseja utilizar.",
		placeholder="Ex: sk-1234567890abcdef1234567890abcdef1234567890abcdef"
	)
	st.markdown("Cadastre seu modelo na API")
	modelo_api = st.text_input(
		"Modelo",
		help="Digite o nome do modelo que deseja utilizar na API.",
		placeholder="Ex: gpt-3.5-turbo"
	)
	salvar = st.button(
		"💾 Salvar Configurações",
		help="Clique para salvar as configurações.",
		type="primary",
	)
	if chave_api and modelo_api and salvar:
		key_name = f'{modelo_api}_key'.replace("-", "_").replace(".", "_")
		try:
			if not os.path.exists(ENV_PATH):
				with open(ENV_PATH, 'w') as f:
					f.write("")
			set_key(ENV_PATH, key_name,chave_api)
			st.toast(
				"Configurações salvas com sucesso! Você pode utilizar a API com o modelo selecionado.",
				icon="✅"
			)
		except Exception as e:
			st.toast(
			f"Erro ao salvar as configurações: {e}",
			icon="❌"
		)
	elif salvar  and (not chave_api or not modelo_api):
		st.toast(
			"Por favor, preencha todos os campos antes de salvar as configurações.",
			icon="⚠️"
		)

st.write("---")
st.write("### Prompt Personalizado")
prompt = st.text_area(
	"Prompt",
	help="Digite o prompt que deseja utilizar.",
	placeholder="Ex: Prever a demanda de produtos para os próximos 30 dias.",
	height=200
)
salvar_prompt = st.button(
	"💾 Salvar Prompt",
	help="Clique para salvar o prompt.",
	type="primary",
)