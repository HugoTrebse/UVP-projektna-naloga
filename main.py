import requests
import funkcije
import csv
import os

#To je spletna stran, iz katere bomo pridobivali podatke
izvorni_html = r'https://ratings.fide.com/toparc.phtml?cod='

starsevska_pot_plitka = os.getcwd()
starsevska_pot_globoka =  os.path.join(starsevska_pot_plitka, 'podatkovna_baza')

os.makedirs(starsevska_pot_globoka, exist_ok=True)

obstojeci_sahisti = set()

with open(os.path.join(starsevska_pot_plitka, 'sahisti'), 'w', newline='') as dat:
    pisalec = csv.writer(dat)
    pisalec.writerow(['Ime', 'Leto rojstva'])

for i in range(200):
    pridobljena_prosnja = requests.get(f'{izvorni_html}{797-4*i}')
    vsebina = pridobljena_prosnja.text
    posamezniki = funkcije.sirote(vsebina)
    date = funkcije.ekstrahiranje_datumov(vsebina)
    for posameznik in posamezniki:
        razcepljeno = funkcije.dekompozicija(posameznik)
        funkcije.splosna_evidenca(razcepljeno[0], razcepljeno[6], starsevska_pot_plitka, obstojeci_sahisti)
        funkcije.pisatelj_csvjev(razcepljeno, date, starsevska_pot_globoka)
