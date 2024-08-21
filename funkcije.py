import re
import csv
import os.path

meseci = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

parent_path = r'C:\Users\hugot\Documents\FMF\1_letnik\UVP-projektna-naloga\podatkovna_baza'
parent_path_shallow = r'C:\Users\hugot\Documents\FMF\1_letnik\UVP-projektna-naloga'
    
def sirote_str(str_file):
    sirote = re.split(r'bgcolor', str_file)
    odvecno = int(sirote[-1].index('<span class="article_separator">&nbsp;</span>') - 25)
    sirote[-1] = sirote[-1][0: odvecno]
    del sirote[0]
    return sirote

def dekompozicija(snippet):
    vzorec = r'&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;([^<]+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)</td><td>&nbsp;(\d+)'
    razdelitev = re.search(vzorec, snippet)
    if razdelitev:
        ime = razdelitev.group(1)
        naziv = razdelitev.group(2)
        drzava = razdelitev.group(3)
        rating = razdelitev.group(4)
        st_iger = razdelitev.group(5)
        leto_rojstva = razdelitev.group(6)
    return ime, naziv, drzava, rating, st_iger, leto_rojstva

def date_extractor(html):
    vzorec = r'contentheading" width="100%">\n\s*Top 100 Players (\w+) (\d+)'
    datum = re.search(vzorec, html)
    leto = datum.group(2)
    mesec = meseci.index(datum.group(1)) + 1
    if mesec < 10:
        mesec = '0' + str(mesec)
    return f'{mesec}-{leto}'


#nespremenljive podatke kot so ime, naziv, ter leto rojstva shranimo v en seperate .csv, podatke, ki so odvisni od časa, kot so rating, trenutni cas ter državljanstvo pa v .csv 
#(drzavljanstvo je dejansko spremenljivo; pimer je Richard Rapoport, ki je prešel iz Madžarske v Romunsko šahovsko zvezo)

#Ustvarimo funkcijo, ki bo nespremenljive podatke o sahistu shranila v neko globalno .csv datoteko.
def splosna_evidenca(ime, leto_rojstva, obstojeci_sahisti):
    if not(ime in obstojeci_sahisti):
        obstojeci_sahisti.add(ime)
        with open(os.path.join(parent_path_shallow, 'sahisti'), 'a') as dat:
            pisalec = csv.writer(dat)
            pisalec.writerow([ime, leto_rojstva])
        with open(os.path.join(parent_path, str(ime)), 'w') as dat2:
            pass
#nimam najmanjše ideje zakaj ime dodaja v teh čudnih oklepajih??? - zato ker bi čene v .csv-ju bili trije podatki - prvo ime in priimek namreč loči vejica.

#Ustvarimo funkcijo, ki sprejme decomposed podatke o igralcu ter jih da v ustrezen .csv, oz ga ustvari ob primeru neobstoja.
def pisatelj_csvjev(ime ,naziv, drzava, rating, st_iger, datum):
    with open(os.path.join(parent_path, ime), 'a') as dat:
        pisalec = csv.writer(dat)
        pisalec.writerow([datum, drzava, naziv, rating, st_iger])