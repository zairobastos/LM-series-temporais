import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
import pandas as pd
from src.view.header import Header
from src.view.dataset import Dataset
from src.model.dados_model import DadosModel

#
# Configuração da página
st.title("Previsão de Séries Temporais - Histórico")
