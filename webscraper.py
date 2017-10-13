import requests as req
from bs4 import BeautifulSoup as soup 

length = 5

	# spezifiziere meine url
my_url ='https://www.stilinberlin.de/tag/berlins-best'
#my_url = 'https://www.stilinberlin.de/tag/berlins-best/page/5'
#my_url = 'https://www.stilinberlin.de/category/food'
#my_url = 'https://www.stilinberlin.de/category/food/page/83'

# und das ganze will ich als csv Datei ausgeben also hier noch definieren
# erstmal den Dateinamen.. kann alles aber auch angepasst durchgeführt werden
filename = "artikel.csv"
# # f ist standardabkürzung für Dateiaktionen... "w" heißt er soll schreiben
f = open(filename, "w")
# # csv Dateien werden durch die Headers formatiert also hier angeben... \n heißt immer eine neue Zeile
headers = "Titel; Autor; Datum; Beschreibung; Link\n"
# # befehl dass er schreiben soll
f.write(headers)


while length > 4:
	# lese die url ein durch requests aka req und speichere sie in page_html
	page_html = req.get(my_url)

	# ich rufe die Funktion soup aka BeautifulSoup aus dem Packet bs4 auf und das dient dazu die html Datei zu zergliedern. 
	# Speicher das in page_soup und gebe an welcher Parser benutzt werden soll. hier lxml
	# der Grund warum ich page_html.content angebe ist weil ich vorher mit requests eine Kopie gespeichert habe und mich
	# jetzt entscheiden muss was ich alles weitergeben möchte. mit content gebe ich die komplette Seite weiter
	page_soup = soup(page_html.content, "lxml")

	#hier definiere ich dass durch alle article mit dem class Namen post durchgegangen wird und in articles gespeichert
	articles = page_soup.findAll("article", {"class": "post"})

	# length = 5
	# while length > 4:

	# # jetzt sage ich gehe alles einzeln durch für jeden article den du gefunden hast und speichere die Information in den
	# # Variablen titel etc was ich suche ist im html weiter vernestelt also gehe ich mehrere divs und a Tags runter...
	for article in articles:
		try:
			# hier hangel ich mich direkt an der html entlang
			titel = article.div.next_sibling.next_sibling.header.h1.a.text
			print(titel)
		except:
			pass

		try:
			# hier sage ich finde alle a Tags mit der Eigenschaft rel  = author
		 	autor_container = article.findAll("a", {"rel": "author"})
		 	autor = autor_container[0].text
		 	print(autor)
		except:
			pass

		try:
		 	datum_container = article.findAll("span", {"class": "date"})
		 	datum = datum_container[0].text
		 	print(datum)
		except:
			pass

		try:
			# Das hier ist gut weil das p-Tag das einzige ist ohne Angabe einer Klasse und weil 
			# next.sibling nicht funktionert und die Hierarchie nicht richtig eingehalten wird
			p_container = article.findAll("p", class_ = "")
			p_text = p_container[0].text
			print(p_text)
		except:
			pass

		try:
			#hier hangel ich mich entlang aber wenn ich zum a Tag komme will ich das href auslesen
			link = article.div.a.get("href")
			print(link)
		except:
			pass

		# aufruf zum schreiben, einzelne Beiträge sollen abgetrennt werden und wenn ich im product_name ein Komma finde soll
		# dieses ersetzt werden durch |. 
		f.write(titel + ";" + autor + ";" + datum + ";" + p_text + ";" + link + ";" + "\n")

		# Finde die nächste Seite. Ich könne es auch so machen dass ich direkt nach einem a Tag schaue mit dem String Older Posts
	try:
		next_page = page_soup.findAll("div", {"class" : "next"})
		next_page_link = next_page[0].a.get("href")		
		length = len(next_page_link)
		my_url = next_page_link
	except:
		length = 0
		print("Laenge nach Except: " + str(length))
		pass

f.close()