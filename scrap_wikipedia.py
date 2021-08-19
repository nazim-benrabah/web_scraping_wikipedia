
import re
from requests import *
from re import *

from pathlib import *

from bs4 import BeautifulSoup as bs


####################################################################################################### QUESTION 1

url = 'https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population'



r = get(url)
soup = bs(r.text, features="lxml")

def stream_download(source_url, dest_file):
	r = get(source_url, stream=True)
	dest_file = Path(dest_file)
	with open(dest_file, "wb") as f:
		for chunk in r.iter_content(chunk_size=8192):
			if chunk:
				f.write(chunk)

stream_download(source_url=url, dest_file="exercice4.html")


html_tronqué_pays=str(soup).split('estimations faites en 2018')[0] ########tronquer le fichier html en deux partie et s'interesser à la premiere seulement où l'on trouve notre tableau 


####################################################################################################### QUESTION 2

html_tronqué_pays = bs(html_tronqué_pays, "html.parser") ######convertir le str en objet beautiful soup


html_tronqué_densité=str(html_tronqué_pays).split('</td></tr>\n<tr>\n<td align=')

references=[]

for p in html_tronqué_pays.find_all('td', {'align': 'left'}):
	references.append(str(p).split('href="')[-1].split('" title')[0])

rang=0

dic={}

url2='https://fr.wikipedia.org'
c=1

superficies=[]
population=[]

for ref in references:
	r = get(url2+ref)
	soup = bs(r.text, features="lxml")
	stream_download(source_url=url2+ref, dest_file=str(c)+'.html')
	try:
		superficies.append(bs(str(soup).split('Superficie totale</th>\n<td>')[1].split('<')[0].replace(u'\xa0', ' ').encode('utf-8'),"html.parser"))
	except Exception:
		superficies.append('Superficie introuvable')
	try:
		population.append(bs(str(soup).split('Population totale</a> <span style="font-weight:normal;">')[1].split('<td>')[1].split('<')[0].replace(u'\xa0', ' ').encode('utf-8'),"html.parser"))
	except Exception:
		population.append('Population Introuvable')
	c+=1


for p in html_tronqué_pays.find_all('td', {'align': 'left'}):
	rang+=1
	try:
		#print(p.find('span')['data-sort-value'])
		dic[str(p.find('span')['data-sort-value'])]=[]
		dic[str(p.find('span')['data-sort-value'])].append(str(rang))
		dic[str(p.find('span')['data-sort-value'])].append(html_tronqué_densité[rang-1].split('<td>')[-1].replace('\n',''))
		dic[str(p.find('span')['data-sort-value'])].append(str(superficies[rang-1]).replace('\n',''))
		dic[str(p.find('span')['data-sort-value'])].append(str(population[rang-1]).replace('\n',''))

		#print(rang)
		#print(html_tronqué_densité[rang-1].split('<td>')[-1])

	except Exception:
		print('')

dic['Zimbabwe'][1]=dic['Zimbabwe'][1].split('<')[0]


#print(dic)


a= input('Introduire le nom du pays\n')

try:
	print('Rang  = ',dic[a][0])
	print('Densite = ',dic[a][1])
	print('Superficie = ',dic[a][2])
	print('Population = ', dic[a][3])
except Exception:
	print("pays introuvable")




	
