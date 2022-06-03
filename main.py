from bs4 import BeautifulSoup
import csv
import datetime
import webbrowser

file = ""
with open("pc.html", "r") as pc:
	lines = pc.readlines()
	for i in lines:
		file += i

data = []
fieldNames = ["date","nom","position liste d'attente","nombre total en liste d'attente","nombre de place dans le groupe","ma position dans le classement","position du dernier candidat","position du dernier candidat en 2021"]

soup = BeautifulSoup(file)
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

k = ""
while not(k.lower() in ["oui", "non"]):
	k = input("Votre fichier .csv est prêt, si vous voulez, nous pouvons aussi créer une page html pour un meilleur rendu et l'ouvrir dans votre navigateur préféré :) [Oui/Non] ")

if k == "oui":
	with open("data.html", "w") as html:

		start = """
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<script src=\"https://cdn.tailwindcss.com\"></script>
		<section class=\"text-gray-600 body-font\">
  <div class=\"container px-5 py-24 mx-auto\">
    <div class=\"flex flex-col text-center w-full mb-20\">
      <h1 class=\"sm:text-4xl text-3xl font-medium title-font mb-2 text-gray-900\">parcoursupTool</h1>
      <p class=\"lg:w-2/3 mx-auto leading-relaxed text-base\">Vous inquetez pas, jvais me taper une annee blanche jsens :')</p>
    </div>
    <div class=\"lg:w-2/3 w-full mx-auto overflow-auto\">
      <table class=\"table-auto w-full text-left whitespace-no-wrap\">
        <thead>
          <tr>
            <th class=\"px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl\">Formation</th>
            <th class=\"px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100\">Place en file Attente</th>
            <th class=\"px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100\">Classement</th>
            <th class=\"px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100\">Classement dernier en 2021</th>
            <th class=\"px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100\">Nb Places</th>
          </tr>
        </thead>
        <tbody>"""

		d = ""
		for i in data:
			d += f"<tr><td class=\"px-4 py-3\">{i['nom']}</td><td class=\"px-4 py-3\">" + str(i['position liste d\'attente']) +" / " + str(i['nombre total en liste d\'attente']) + f"</td><td class=\"px-4 py-3\">{i['ma position dans le classement']}</td><td class=\"px-4 py-3\">"+ ("N/A" if not("position du dernier candidat en 2021" in i) else i['position du dernier candidat en 2021']) + f"</td><td class=\"px-4 py-3\">{i['nombre de place dans le groupe']}</td></tr>"
          
		end = """
		</tbody>
      </table>
    </div>
  </div>
</section>"""
		html.write(start + d + end)
		html.close()
	webbrowser.open('data.html')



