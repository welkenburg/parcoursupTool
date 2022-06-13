import requests
from bs4 import BeautifulSoup
import csv
import datetime
from tkinter import messagebox, Tk

# proxy for testing
#import proxy
#run_proxy()

def run(user, passwd, filename):
	# post request headers
	payload = {
		'ACTION' : '1',
		'g_cn_cod' : user,
		'g_cn_mot_pas':passwd
	}

	# csv table headers and data
	data = []
	fieldNames = ["date","nom","position liste d'attente","nombre total en liste d'attente","nombre de place dans le groupe","ma position dans le classement","position du dernier candidat","position du dernier candidat en 2021"]

	# open a new internet session and sending requests
	with requests.Session() as s:
		# get the login page to have the CSRFToken
		a = s.get('https://dossierappel.parcoursup.fr/Candidat/authentification?')

		# scrap the token
		soup = BeautifulSoup(a.content, features="lxml")
		payload['CSRFToken'] = soup.find(id="CSRFToken").get('value')

		# send creds to parcoursup
		p = s.post('https://dossierappel.parcoursup.fr/Candidat/authentification?', data=payload)

		# get back the choices
		r = s.get('https://dossierappel.parcoursup.fr/Candidat/admissions?ACTION=0')
		file = r.content

	try:
		# handle choices page as a html document
		soup = BeautifulSoup(file, features="lxml")
		tables = soup.find_all("table")
		enAttente = tables[1]
		choices = enAttente.tbody.find_all("tr")
	except:
		alert = getattr(messagebox, 'showerror')
		alert('Erreur','Mot de passe ou numéro non valide')
		return

	# for each choices, scrap the numbers
	for c in choices:
		row = {}
		row["date"] = datetime.datetime.now().strftime('%d/%m/%Y')
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
		
		# add numbers to row
		data.append(row)

	# write data to csv
	with open(filename, "a") as out:
		writer = csv.DictWriter(out, fieldnames=fieldNames)
		writer.writerows(data)

	success = getattr(messagebox, 'showinfo')
	success('Sucess','votre dossier parcoursup a bien été converti en tableau excel !')
	quit()