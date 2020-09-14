import re
import pandas as pd

# Função que faz a busca de uma palavra dentro de uma string
def kmp(t, p):
	next = [0]
	j = 0
	for i in range(1, len(p)):
		while j > 0 and p[j] != p[i]:
			j = next[j - 1]
		if p[j] == p[i]:
			j += 1
		next.append(j)
	ans = []
	j = 0
	for i in range(len(t)):
		while j > 0 and t[i] != p[j]:
			j = next[j - 1]
		if t[i] == p[j]:
			j += 1
		if j == len(p):
			ans.append(i - (j - 1))
			j = next[j - 1]
	return ans

def consulta_genero(nome):
	"""
	Consulta o nome no DataFrame para verificar a distribuica de genero para
	esse nome no Brasil. Retorna uma tupla com o genero mais recorrente e a
	frequencia desse genero mais recorrente para aquele nome 
	"""
	dados = importa_dados_genero();
	if nome is not None:    
		try:
			query = dados.where(dados["first_name"] == nome.upper())

			genero = query["classification"].dropna().to_list()[0]

			# A base de dados possui uma coluna "ratio" com a frequencia do genero para
			# determinado nome. Porem os resultados nao estao normalizados e parecem
			# caoticos. Portanto, vamos usar outros dados da base para determinar isso
			if genero == "F":
				frequencia_genero = int(query["frequency_female"].dropna().to_list()[0])
			elif genero == "M":
				frequencia_genero = int(query["frequency_male"].dropna().to_list()[0])

			frequencia_total = int(query["frequency_total"].dropna().to_list()[0])
			frequencia = frequencia_genero / frequencia_total

			return genero

		except:
			genero = "None"
			return genero

	else:
		return "None"

def importa_dados_genero():
	"""
	Importa para um DataFrame a base de dados do CENSO 2010 com a distribuicao
	de genero para cada nome. O dataset consolidado foi encontrado no site do
	Brasil.io (https://brasil.io/dataset/genero-nomes/nomes/). Retorna esse DF
	"""
	dados = pd.read_csv("nomes.csv")

	return dados