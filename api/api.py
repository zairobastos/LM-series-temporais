import lmstudio as lms 
import re
import time

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
		
	def resposta(self):
		"""
		Gera a resposta do modelo com base no prompt e temperatura definidos.

		Returns:
			str: Resposta do modelo.
		"""
		try:
			model = lms.llm(self.model)
			print(f"[INFO] Modelo: {model}")
			
			inicio = time.time()
			response_obj = model.respond(self.prompt, config={
				"temperature": self.temperature,
			})
			fim = time.time()

			# Verifica se o objeto tem o atributo `.text`
			response = response_obj.text if hasattr(response_obj, 'text') else str(response_obj)

			if 'deepseek-r1' in self.model:
				resultado = re.search(r'</think>\s*(.*)', response, re.DOTALL)
				if resultado:
					response = resultado.group(1).strip()

			print(response)
			qtd_tokens_prompt = response_obj.stats.prompt_tokens_count if hasattr(response_obj, "stats") else 0
			qtd_tokens_resposta = response_obj.stats.predicted_tokens_count if hasattr(response_obj, "stats") else 0
			print(f"[INFO] Tokens Prompt: {qtd_tokens_prompt} - Tokens Resposta: {qtd_tokens_resposta} - Tempo: {fim - inicio:.2f} segundos")
			return response, qtd_tokens_prompt, qtd_tokens_resposta, fim - inicio
		
		except Exception as e:
			print(f"[ERROR] Erro ao gerar resposta: {e}")
			return None, None, None, None
