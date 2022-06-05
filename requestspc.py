import requests
from bs4 import BeautifulSoup
import csv
import datetime
# import os

# proxy = '127.0.0.1:8080'
# os.environ["http_proxy"] = proxy
# os.environ["HTTP_PROXY"] = proxy
# os.environ["https_proxy"] = proxy
# os.environ["HTTPS_PROXY"] = proxy
# os.environ["REQUESTS_CA_BUNDLE"] = 'certificate.pem'

user = input("entrez votre numéro parcoursup :\n")
password = input("entrez votre mot de passe :\n")

payload = {
	'ACTION' : '1',
	'g_cn_cod' : user,
	'g_cn_mot_pas':password
}

data = []
fieldNames = ["date","nom","position liste d'attente","nombre total en liste d'attente","nombre de place dans le groupe","ma position dans le classement","position du dernier candidat","position du dernier candidat en 2021"]

with requests.Session() as s:
	a = s.get('https://dossierappel.parcoursup.fr/Candidat/authentification?')

	soup = BeautifulSoup(a.content, features="lxml")
	payload['CSRFToken'] = soup.find(id="CSRFToken").get('value')


	p = s.post('https://dossierappel.parcoursup.fr/Candidat/authentification?', data=payload)

	r = s.get('https://dossierappel.parcoursup.fr/Candidat/admissions?ACTION=0')
	file = r.content
	
	soup = BeautifulSoup(file, features="lxml")
	tables = soup.find_all("table")
	enAttente = tables[1]
	choices = enAttente.tbody.find_all("tr")
	for c in choices:
		row = {}
		row["date"] = datetime.datetime.now()
		row["nom"] = c.find_all("td")[2].string.strip()
		try:
			positionListeAttente = c.find_all("td")[4].div.div.ul.li.div.ul.find_all("li")[0].span.string
			row["position liste d'attente"] = positionListeAttente
		except:
			pass

		try:
			nombreTotListeAttente = c.find_all("td")[4].div.div.ul.li.div.ul.find_all("li")[1].span.string
			row["nombre total en liste d'attente"] = nombreTotListeAttente
		except:
			pass

		try:
			nombrePlaceGroupe = c.find_all("td")[4].find(id="rang_cddt").find_all("ul")[0].li.span.string
			row["nombre de place dans le groupe"] = nombrePlaceGroupe
		except:
			pass

		try:
			positionClassement = c.find_all("td")[4].find(id="rang_cddt").find_all("ul")[1].find_all("li")[0].span.string
			row["ma position dans le classement"] = positionClassement
		except:
			pass

		try:
			lastCandidate = c.find_all("td")[4].find(id="rang_cddt").find_all("ul")[1].find_all("li")[1].span.string
			row["position du dernier candidat"] = lastCandidate
		except:
			pass

		try:
			lastCandidate2021 = c.find_all("td")[4].find(id="rang_cddt").find_all("ul")[1].find_all("li")[2].span.string
			row["position du dernier candidat en 2021"] = lastCandidate2021
		except:
			pass

		data.append(row)

	with open("data.csv", "a") as out:
		writer = csv.DictWriter(out, fieldnames=fieldNames)
		writer.writerows(data)