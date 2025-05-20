TABLE_SCHEMA_ETTH = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data_inicio TEXT,
  data_fim TEXT,
  horas INTEGER,
  modelo TEXT,
  temperatura_modelo REAL,
  prompt TEXT,
  tipo_prompt TEXT CHECK(tipo_prompt IN ('ZS', 'FS', 'CoT','CoT+FS')),
  valores_exatos TEXT,
  valores_previstos TEXT,
  smape REAL,
  top_k INTEGER,
  max_tokens INTEGER,
  total_tokens_saida INTEGER,
  total_tokens_entrada INTEGER,
  total_tokens INTEGER  
)"""

TABLE_SCHEMA_DATASET = """
CREATE TABLE IF NOT EXISTS {table_name} (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome_dataset TEXT NOT NULL UNIQUE,
	coluna_data TEXT NOT NULL,
	coluna_valor TEXT NOT NULL
)"""