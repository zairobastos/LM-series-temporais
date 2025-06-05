import pandas as pd


df_original = pd.read_excel('arquivos_RU.xlsx', sheet_name='Planilha1')


df_original.columns = df_original.columns.str.strip()


df_original['Data'] = pd.to_datetime(df_original['Data'], errors='coerce')
df_original['Comensais_almoço'] = pd.to_numeric(df_original['Comensais_almoço'], errors='coerce')
#df_original['Comensais_janta'] = pd.to_numeric(df_original['Comensais_janta'], errors='coerce')


df_original = df_original.dropna(subset=['Data'])


datas_completas = pd.date_range(start=df_original['Data'].min(), end=df_original['Data'].max(), freq='D')
df_completo = pd.DataFrame({'Data': datas_completas})


df_final = pd.merge(df_completo, df_original, on='Data', how='left')


df_final['Comensais_almoço'] = df_final['Comensais_almoço'].fillna(0).astype(int)
#df_final['Comensais_janta'] = df_final['Comensais_janta'].fillna(0).astype(int)

df_final['Data'] = df_final['Data'].dt.strftime('%d/%m/%Y')


df_final.to_csv('data/dataset_completo_formatado.csv', index=False)

print("✅ Dataset criado com sucesso!")
