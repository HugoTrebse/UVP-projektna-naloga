import requests
import funkcije
import csv
import os

pot_plitka = os.getcwd()
pot_globoka =  os.path.join(pot_plitka, 'podatkovna_baza')
pot_sahisti = os.path.join(pot_plitka, 'sahisti')

#To je spletna stran, iz katere bomo pridobivali podatke
izvnorni_fide_url = 'https://ratings.fide.com/toparc.phtml?cod='

os.makedirs(pot_globoka, exist_ok=True)


maksimalni_cod = funkcije.najvisji_cod(izvnorni_fide_url)

#Zgornja koda dobi najvišji dostopni indeks na spletišču https://ratings.fide.com/toparc.phtml?cod=indeks
#Če želite program pospešiti in vam ni v škodo pridobiti le podatke do Septembra 2024 pa se lahko poslužite znanega dejstva, da je Septembra 2024 maksimalni_cod = 801.
#Seveda bi lahko algoritem, ki pridobi indeks optimizirali; npr z uporabo binary searcha, ki bi iz trenutnega linearnega časa spremenil časovno zahtevnost
#na log_2(U), kjer je U zgornja meja za morebitni legalni indeks (tudi če imamo podatke o šahistih za vsak mesec zadnjih 100 let je U = 12000; log_2(U) = 13.55). 
#Slednje je seveda dosti hitrejše, a znan programerski pregovor pravi: 'Premature optimization is the root of all evil'.

#maksimalni_cod = 801

obstojeci_sahisti = set()

with open(pot_sahisti, 'w', newline='') as dat:
    pisalec = csv.writer(dat)
    pisalec.writerow(['Ime', 'Leto rojstva'])

for i in range(maksimalni_cod + 1):
    #Informacije o odprti kategoriji se nahajajo točno na URL-jih, v katerih je cod % 4 = 1.
    if i % 4 == 1:
        pridobljena_prosnja = requests.get(f'{izvnorni_fide_url}{i}')
        vsebina = pridobljena_prosnja.text
        posamezniki = funkcije.sirote(vsebina)
        date = funkcije.ekstrahiranje_datumov(vsebina)
        for posameznik in posamezniki:
            razcepljeno = funkcije.dekompozicija(posameznik)
            funkcije.splosna_evidenca(razcepljeno[0], razcepljeno[6], pot_plitka, obstojeci_sahisti)
            funkcije.pisatelj_csvjev(razcepljeno, date, pot_globoka)