import lmstudio as lms 
import re

class API:
	def __init__(self, model: str, prompt: str, temperature: float):
		"""
		Classe responsável por manipular a API do modelo.

		Args:
			model (str): Modelo a ser utilizado.
			prompt (str): Prompt a ser utilizado.
			temperature (float): Temperatura do modelo.
		"""
		self.model = model
		self.prompt = prompt
		self.temperature = temperature
		self.llm = lms.llm(self.model)
		
	def resposta(self):
		"""
		Gera a resposta do modelo com base no prompt e temperatura definidos.

		Returns:
			str: Resposta do modelo.
		"""
		try:
			response = self.llm.respond(self.prompt, config={
				"temperature": self.temperature,
			})
			if 'deepseek' in self.model:
				response = re.search(r'</think>\s*(.*)', response, re.DOTALL)
				if response:
					response = response.group(1).strip()
					return response
				else:
					print("[ERROR] Resposta não encontrada no formato esperado.")
				return None
		except Exception as e:
			print(f"[ERROR] Erro ao gerar resposta: {e}")
			return None