import numpy as np
from permetrics.regression import RegressionMetric
from scipy.stats import sem

class Metricas:
	def __init__(self, y_true, y_pred):
		self.y_true = y_true
		self.y_pred = y_pred

	def smape(self) -> float:
		"""Calcula o erro percentual absoluto médio simétrico (sMAPE).

		Returns:
			float: Erro percentual absoluto médio simétrico.
		"""
		y_true = np.array(self.y_true)
		y_pred = np.array(self.y_pred)

		evaluator = RegressionMetric(y_true, y_pred)
		smape = evaluator.SMAPE()
		smape_percent = smape*100
		return round(smape_percent, 2)*2
	
	def sem(self, erros: list[float]) -> float:
		"""Calcula o erro médio absoluto percentual (sEM).

		Parameters:
			erros (list[float]): Lista de erros absolutos percentuais.

		Returns:
			float: Erro médio absoluto percentual.
		"""
		erro = round(sem(erros),4)

		return erro

	def mae(self) -> float:
		"""Calcula o erro médio absoluto (MAE).
		Returns:
			float: Erro médio absoluto.
		"""
		y_true = np.array(self.y_true)
		y_pred = np.array(self.y_pred)
		mae = np.mean(np.abs(y_true - y_pred))
		return round(mae, 4)

	def rmse(self) -> float:
		"""Calcula a raiz do erro quadrático médio (RMSE).
		Returns:
			float: Raiz do erro quadrático médio.
		"""
		y_true = np.array(self.y_true)
		y_pred = np.array(self.y_pred)
		rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
		return round(rmse, 4)
