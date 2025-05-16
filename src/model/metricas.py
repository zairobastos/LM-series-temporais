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
