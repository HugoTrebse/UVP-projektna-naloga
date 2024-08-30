import re
import csv
import os
import requests

pot_plitka = os.getcwd()
pot_globoka =  os.path.join(pot_plitka, 'podatkovna_baza')
pot_sahisti = os.path.join(pot_plitka, 'sahisti')
meseci_ang = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#Loči html kodo na podnize, ki vsebujejo relevantne podatke za enega šahista.
#Ako ni bilo jasno iz konteksta je ime funkcije tako, ker iz družine šahistov izlušči informacije o posamezniku.
def sirote(html_datoteka):
    sirote = re.split(r'bgcolor', html_datoteka)
    if '<span class="article_separator">&nbsp;</span>' in html_datoteka:
        odvecno = int(sirote[-1].index('<span class="article_separator">&nbsp;</span>') - 25)
    else:
        odvecno = -1
    sirote[-1] = sirote[-1][0: odvecno]
    del sirote[0]
    return sirote

#Iz niza, ki ga vrne funkcija sirote, izlušči podatke o posameznem šahistu.
def dekompozicija(delcek):
    vzorec = r'<td width=10>&nbsp;(\d+)</a></td><td>&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)'
    razdelitev = re.search(vzorec, delcek)
    if razdelitev:
        rang = razdelitev.group(1)
        ime = razdelitev.group(2).replace('.','')
        #Morda se sprašujete zakaj je zgornji .replace potreben. Odgovor je, da če dopustimo pike v imenih, pride do težav pri analizi z programom pandas, 
        #saj program smatra piko kot delimiter, tudi če delimiterje manualno nastavimo zgolj na vejice. Sicer pa ne pride do izgube informacij, saj se imena kot so
        #'Adhiban, B.' zgolj spremenijo v 'Adhiban, B'.
        naziv = razdelitev.group(3)
        drzava = razdelitev.group(4)
        rating = razdelitev.group(5)
        st_iger = razdelitev.group(6)
        leto_rojstva = razdelitev.group(7)
    return ime, naziv, drzava, rang, rating, st_iger, leto_rojstva

#iz HMTL kode dobi datum
def ekstrahiranje_datumov(html):
    try:
        vzorec = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
        datum = re.search(vzorec, html)
        leto = datum.group(2)
        mesec = meseci_ang.index(datum.group(1)) + 1
        if mesec < 10:
            mesec = '0' + str(mesec)
        return f'{mesec}-{leto}'
    except:
        return None

#Nespremenljive podatke kot sta ime ter leto rojstva shranimo v sahisti.csv, podatke, ki so odvisni od časa, kot so datum, naziv, rating, ter državljanstvo pa v .csv 
#(drzavljanstvo je dejansko spremenljivo; pimer je Richard Rapport, ki je prešel iz Madžarske v Romunsko šahovsko zvezo).

#Ustvarimo funkcijo, ki bo nespremenljive podatke o sahistu shranila v neko globalno .csv datoteko.
def splosna_evidenca(ime, leto_rojstva, starsevska_pot_plitka, obstojeci_sahisti):
    if not(ime in obstojeci_sahisti):
        obstojeci_sahisti.add(ime)
        with open(os.path.join(starsevska_pot_plitka, 'sahisti'), 'a', newline='') as dat:
            pisalec = csv.writer(dat)
            pisalec.writerow([ime, leto_rojstva])
        with open(os.path.join(os.path.join(starsevska_pot_plitka, 'podatkovna_baza'), ime.replace(' ', '_')), 'w', newline='') as dat2:
            pisalec = csv.writer(dat2)
            pisalec.writerow(['datum', 'drzava', 'naziv', 'rang', 'rating', 'stevilo iger'])
            #Nadobudnim slovenistom dajem v vednost, da je rating slovenska beseda, ki jo lahko najdemo v SSKJ.
#Zakaj so vnosi v .csv datoteke oblike "priimek, ime",leto ? Če ne, bi bil podatek str(priimek, ime) v .csv formatu v resnici dva podatka.

#Ustvarimo funkcijo, ki sprejme podatke o igralcu (kot jih vrne funkcija dekompozicija) ter jih zapiše v ustrezen .csv.
def pisatelj_csvjev(array, datum, starsevska_pot_globoka):
    with open(os.path.join(starsevska_pot_globoka, array[0].replace(' ', '_')), 'a', newline='') as dat:
        pisalec = csv.writer(dat)
        pisalec.writerow([datum, array[2], array[1], array[3], array[4], array[5]])

#Z nekaj preizkušanja ugotovimo, da so nekateri url-ji oblike 'https://ratings.fide.com/toparc.phtml?cod=int' za naravna števila int obstoječi, a prazni.
#Zato na sledeč način ugorovimo kateri so uporabni za naše namene (neželene spletne strani ne vsebujejo niza 'Top 100 players').
def legalna_FIDE_spletna_stran(url):
    try:
        odziv = requests.get(url)
        html_vsebina = odziv.text
        vzorec = r"Top\s*100\s*Players"
        if re.search(vzorec, html_vsebina):
            return True
        else:
            return False
    except:
        return False


def najvisji_cod(url_prefix):
    cod = 1
    while True:
        url = f'{url_prefix}{cod}'
        if legalna_FIDE_spletna_stran(url):
            cod += 4
        else:
            break
    return cod - 4

#Ustvarimo linearno urejenost na datumih (za potrebe analize)
def datum_v_float(datum):
    mesec = int(datum[0:2])
    leto = int(datum[3:])
    veckratnik = 0.08
    return leto + mesec * veckratnik

def float_v_datum(float):
    leto = int(float)
    mesec = round((float - leto) * 12.5)
    # 12.5 je veckratnik tukaj, saj je 0.08 * 12.5 = 1
    return f'{mesec}-{leto}'

#Za potrebe analize ustvarimo funkcijo, ki sprejme ime sahista ter datum v formatu 'mm-yyyy' ter vrne njegovo starost ob tem casu
#Starost bo stevilo s plavajoco vejico, ker nimamo podatkov o rojstnem mesecu ter dnevu sahistov bomo privzeli, da so vsi rojeni 1-1-leto_rojstva
def starost(ime_sahista, datum):
    lokacija = os.getcwd()
    with open(os.path.join(lokacija, 'sahisti'), 'r') as dat:
        prebrana_datoteka = csv.reader(dat)
        for vrstica in prebrana_datoteka:
            if vrstica[0] == ime_sahista:
                return datum_v_float(datum) - vrstica[1]
            
#Za potrebe krajšanja v analiza_podatkov.py uvedemo naslednjo funkcijo:
def ime_v_pot(ime):
    return os.path.join(pot_globoka, ime.replace(' ', '_'))