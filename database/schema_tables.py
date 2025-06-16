TABLE_SCHEMA_ETTH = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data_inicio TEXT,
  data_fim TEXT,
  periodos INTEGER,
  modelo TEXT,
  temperatura_modelo REAL,
  prompt TEXT,
  tipo_prompt TEXT CHECK(tipo_prompt IN ('ZERO_SHOT', 'FEW_SHOT', 'COT','COT_FEW')),
  valores_exatos TEXT,
  valores_previstos TEXT,
  smape REAL,
	mae REAL,
	rmse REAL,
  total_tokens_resposta INTEGER,
  total_tokens_prompt INTEGER,
  total_tokens INTEGER 
)"""