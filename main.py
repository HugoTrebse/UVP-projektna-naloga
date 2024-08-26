import requests
import funkcije
import csv
import os

obstojeci_sahisti = set()
parent_path_shallow = r'C:\Users\hugot\Documents\FMF\1_letnik\UVP-projektna-naloga'
parent_html = r'https://ratings.fide.com/toparc.phtml?cod='

with open(os.path.join(parent_path_shallow, 'sahisti'), 'w', newline='') as dat:
    pisalec = csv.writer(dat)
    pisalec.writerow(['Ime', 'Leto rojstva'])

for i in range(200):
    r = requests.get(f'{parent_html}{797-4*i}')
    vsebina = r.text
    posamezniki = funkcije.sirote(vsebina)
    date = funkcije.date_extractor(vsebina)
    for posameznik in posamezniki:
        decomposed = funkcije.dekompozicija(posameznik)
        funkcije.splosna_evidenca(decomposed[0], decomposed[6], obstojeci_sahisti)
        funkcije.pisatelj_csvjev(decomposed, date)
