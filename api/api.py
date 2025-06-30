import lmstudio as lms 
import re
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

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

	def resposta_openai(self) -> tuple[str, int, int, float]:
		"""	Gera a resposta do modelo OpenAI com base no prompt e temperatura definidos.

		Returns:
				str, int, int, float:  Resposta do modelo, quantidade de tokens do prompt, quantidade de tokens da resposta e tempo de execução.
		"""
		print(f"[INFO] Usando modelo OpenAI: {self.model}")

		key_name = f'{self.model}_key'.replace("-", "_").replace(".", "_")
		base_url_name = f'{self.model}_base_url'.replace("-", "_").replace(".", "_")

		api_key = os.getenv(key_name)
		base_url = os.getenv(base_url_name)
		print(f"[INFO] Usando chave da API: {api_key}")

		client = OpenAI(
			api_key=api_key,
			base_url=base_url
		)

		try:
			inicio = time.time()
			response = client.chat.completions.create(
				model=self.model,
				messages=[{"role": "user", "content": self.prompt}],
				temperature=self.temperature,
			)
			fim = time.time()
			print(f"[INFO] Resposta: {response.choices[0].message.content}")
			qtd_tokens_prompt = response.usage.prompt_tokens
			qtd_tokens_resposta = response.usage.completion_tokens
			print(f"[INFO] Tokens Prompt: {qtd_tokens_prompt} - Tokens Resposta: {qtd_tokens_resposta} - Tempo: {fim - inicio:.2f} segundos")
			return response.choices[0].message.content, qtd_tokens_prompt, qtd_tokens_resposta, fim - inicio
		except Exception as e:
			print(f"[ERROR] Erro ao gerar resposta: {e}")
			return None, None, None, None
