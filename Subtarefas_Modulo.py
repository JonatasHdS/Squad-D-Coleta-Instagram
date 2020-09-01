import re
from geopy.geocoders import Nominatim
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

# Função que a partir dos dados de longitude e latitude busca a localização do post caso esteja disponivel
def localiza(lat, long):
	geolocator = Nominatim(user_agent="CDA UFMG")
	loc = str(lat)+", "+str(long)
	location = geolocator.reverse(loc, timeout=10)
	dados = []
	if location.raw["address"]:
		if "state" in location.raw["address"].keys():
			dados.append(location.raw["address"]["state"])
		else:
			dados.append("None")
		if "city" in location.raw["address"].keys():
			cidade = str(location.raw["address"]["city"])
			dados.append(cidade)
			cidade = cidade.replace(" ", "").replace("á", "a").replace("ã", "a").replace("â", "a").replace("é", "e").replace("ê", "e").replace("î", "i").replace("í", "i").replace("õ", "o").replace("ô", "o").replace("ó", "o")
			f = open("cidades.txt", "r")
			if kmp(f.readline(),cidade.lower()) != []:
				dados.append(True)
			else:
				dados.append(False)
		else:
			dados.append("None")
			dados.append("None")
		if "region" in location.raw["address"].keys():
			dados.append(location.raw["address"]["region"])
		else:
			dados.append("None")
	else:
		dados.append("None")
		dados.append("None")
		dados.append("None")
		dados.append("None")
	return dados


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
			print("Nome não encontrado na base!")
			genero = "None"
			return genero

	else:
		print("Conta comercial, impossivel fazer consulta")


def importa_dados_genero():
	"""
	Importa para um DataFrame a base de dados do CENSO 2010 com a distribuicao
	de genero para cada nome. O dataset consolidado foi encontrado no site do
	Brasil.io (https://brasil.io/dataset/genero-nomes/nomes/). Retorna esse DF
	"""
	dados = pd.read_csv("nomes.csv")

	return dados