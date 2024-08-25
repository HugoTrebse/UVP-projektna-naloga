import re
import csv
import os.path

meseci = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

parent_path = r'C:\Users\hugot\Documents\FMF\1_letnik\UVP-projektna-naloga\podatkovna_baza'
parent_path_shallow = r'C:\Users\hugot\Documents\FMF\1_letnik\UVP-projektna-naloga'

#Loči html kodo na podnize, ki vsebujejo relevantne podatke za enega šahista.
def sirote(str_file):
    sirote = re.split(r'bgcolor', str_file)
    if '<span class="article_separator">&nbsp;</span>' in str_file:
        odvecno = int(sirote[-1].index('<span class="article_separator">&nbsp;</span>') - 25)
    else:
        odvecno = -1
    sirote[-1] = sirote[-1][0: odvecno]
    del sirote[0]
    return sirote

#Iz niza, ki ga vrne funkcija sirote, izlušči podatke
def dekompozicija(snippet):
    vzorec = r'<td width=10>&nbsp;(\d+)</a></td><td>&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)'
    razdelitev = re.search(vzorec, snippet)
    if razdelitev:
        rank = razdelitev.group(1)
        ime = razdelitev.group(2)
        naziv = razdelitev.group(3)
        drzava = razdelitev.group(4)
        rating = razdelitev.group(5)
        st_iger = razdelitev.group(6)
        leto_rojstva = razdelitev.group(7)
    return ime, naziv, drzava, rank, rating, st_iger, leto_rojstva

#iz HMTL kode dobi datum
def date_extractor(html):
    vzorec = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
    datum = re.search(vzorec, html)
    leto = datum.group(2)
    mesec = meseci.index(datum.group(1)) + 1
    if mesec < 10:
        mesec = '0' + str(mesec)
    return f'{mesec}-{leto}'


#nespremenljive podatke kot so ime, naziv, ter leto rojstva shranimo v nek globalen .csv, podatke, ki so odvisni od časa, kot so rating, trenutni cas ter državljanstvo pa v .csv 
#(drzavljanstvo je dejansko spremenljivo; pimer je Richard Rapoport, ki je prešel iz Madžarske v Romunsko šahovsko zvezo)

#Ustvarimo funkcijo, ki bo nespremenljive podatke o sahistu shranila v neko globalno .csv datoteko.
def splosna_evidenca(ime, leto_rojstva, obstojeci_sahisti):
    if not(ime in obstojeci_sahisti):
        obstojeci_sahisti.add(ime)
        with open(os.path.join(parent_path_shallow, 'sahisti'), 'a', newline='') as dat:
            pisalec = csv.writer(dat)
            pisalec.writerow([ime, leto_rojstva])
        with open(os.path.join(parent_path, ime.replace(' ', '_')), 'w', newline='') as dat2:
            pisalec = csv.writer(dat2)
            pisalec.writerow(['datum', 'drzava', 'naziv', 'rank', 'rating', 'stevilo iger'])
# Zakaj so vnosi v .csv datoteke oblike "priimek, ime",leto? Če ne bi bil podatek str(priimek, ime) v .csv formatu v resnici dva podatka.

#Ustvarimo funkcijo, ki sprejme podatke o igralcu (kot jih vrne funkcija dekompozicija) ter jih da v ustrezen .csv, oz ga ustvari ob primeru neobstoja.
def pisatelj_csvjev(array, datum):
    with open(os.path.join(parent_path, array[0].replace(' ', '_')), 'a', newline='') as dat:
        pisalec = csv.writer(dat)
        pisalec.writerow([datum, array[2], array[1], array[3], array[4], array[5]])