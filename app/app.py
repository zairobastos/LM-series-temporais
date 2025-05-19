import streamlit as st
from st_pages import Page, show_pages, add_page_title
from datetime import date
import json

from src.views.transporte.description_transporte_streamlit import DescriptionTransporte
from src.views.transporte.estatisticas_transporte_streamlit import EstatisticasTransporte
from src.views.transporte.prompts_transporte_streamlit import PromptsTransporte

from src.views.mercado.description_mercado_streamlit import DescriptionMercado
from src.views.mercado.estatisticas_mercado_streamlit import EstatisticasMercado
from src.views.mercado.prompts_mercado_streamlit import PromptsMercado


from src.views.streamlit.api_streamlit import Api
from src.views.streamlit.grafico import Grafico
from database.crud_database import Crud


# App title
st.set_page_config(page_title="Previsão de Séries Temporais", page_icon=":bus:", layout="wide")

show_pages(
    [
        Page("app.py","Home","🏠"),
        Page("./pages/historico.py","Histórico","📜"),
    ]
)
# Replicate Credentials
with st.sidebar:
    st.write('### Parâmetros da Buscas')
    tipo = st.selectbox('Preveja', ['Transportes', 'Mercado'])
    if tipo == 'Transportes':
        st.write('#### Transportes')
        linhas_onibus = st.selectbox('Linhas de ônibus', [52, 41, 51, 24, 45, 76, 42, 26, 375, 28, 72, 711, 74, 43, 815, 372, 15, 38, 366, 29])
        
        data_max = date(2018, 8, 1)
        data_min = date(2018, 1, 1)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2018, 3, 1))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2018, 6, 4))
        
        horas = st.slider(label='Horas', min_value=24, max_value=168, value=168, step=24)
        num_prompt = st.slider(label='Prompt', min_value=1, max_value=3, value=1, step=1)

    else:
        st.write('#### Mercado')
        produto = st.selectbox('Produtos', [550, 3124, 4022, 10146, 11686, 16766, 20213, 21869, 37082, 44516, 46756, 47289, 47319, 52740, 52849, 53419, 96560, 103893, 410861, 1001587])
        
        data_min = date(2017, 1, 2)
        data_max = date(2019, 4, 30)
        data_inicio = st.date_input(label='Data de início', max_value=data_max, min_value=data_min, value=date(2017, 1, 2))
        data_fim = st.date_input(label='Data de término', max_value=data_max, min_value=data_min, value=date(2019, 1, 2))

        dias = st.slider(label='Dias', min_value=1, max_value=7, value=60, step=1)
        num_prompt = st.slider(label='Prompt', min_value=1, max_value=3, value=1, step=1)

    modelo, temperatura, candidatos = Api().run()

    confirma = st.button(label='Gerar Análise', key='gerar_analise', help='Clique para gerar a análise de dados',type='primary', use_container_width=True)



if confirma:
    if tipo == 'Transportes':
        dataset, passageiros, exatos, df_exato = DescriptionTransporte(data_inicio, data_fim, linhas_onibus).description_transporte()
        result_prompt = PromptsTransporte(dataset, passageiros, exatos, data_inicio, data_fim, linhas_onibus, df_exato, horas).prompt_view()
        previsao, hora, exato, tokens, smape = EstatisticasTransporte(modelo, result_prompt, temperatura, candidatos, horas, exatos).estatisticas()
        Grafico(previsao, exato).grafico()
        data_inicio = str(data_inicio)
        data_fim = str(data_fim)

        valores_exatos_str = json.dumps(exatos)
        valores_previstos_str = json.dumps(previsao)

        database = Crud().insert(
            table='transporte', 
            linha=linhas_onibus, 
            data_inicio=str(data_inicio), 
            data_fim=str(data_fim), 
            horas=horas, 
            modelo=modelo, 
            temperatura=temperatura, 
            candidatos=candidatos, 
            prompt=result_prompt, 
            valores_exatos=valores_exatos_str, 
            valores_previstos=valores_previstos_str, 
            smape=smape, 
            tempo=hora, 
            tokens=tokens,
            num_prompt=num_prompt
        )

    else:
        df_mercado, dados_prompt, dados_exatos, df_exatos = DescriptionMercado(data_inicio, data_fim, produto).description_mercado()
        prompt = PromptsMercado(dataset=df_mercado, exatos=dados_exatos, dados_prompt=dados_prompt, produto=produto, df_exato=df_exatos, dias=dias).prompt_view()
        previsao, hora, exato, tokens,smape = EstatisticasMercado(modelo, prompt, temperatura, candidatos, dias, dados_exatos[:dias]).estatisticas()
        Grafico(previsao, exato, "varejo").grafico()

        data_inicio = str(data_inicio)
        data_fim = str(data_fim)

        valores_exatos_str = json.dumps(exato)
        valores_previstos_str = json.dumps(previsao)

        database = Crud().insert(
            table='mercado', 
            produto=produto, 
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            dias=dias, 
            modelo=modelo, 
            temperatura=temperatura, 
            candidatos=candidatos, 
            prompt=prompt, 
            valores_exatos=valores_exatos_str, 
            valores_previstos=valores_previstos_str, 
            smape=smape, 
            tempo=hora, 
            tokens=tokens
        )

    if database:
        st.success('Dados inseridos com sucesso!', icon='✅')
    else:
        st.error('Erro ao inserir dados!', icon='❌')
else:
    st.write('## Confirme a escolha dos parâmetros para gerar a análise.')
    st.image("icons/undraw_search_re_x5gq.svg", width=500)