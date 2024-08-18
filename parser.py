import re
import requests
import csv

meseci = ['Januar', 'Februar', 'Marec', 'April', 'Maj', 'Junij', 'Julij', 'Avgust', 'September', 'Oktober', 'November', 'December']


obstojeci_sahisti = set()

#funkciji sirote_txt ter sirote_str sprejmeta html kodo ter iz družine podatkov o posameznem igralcu ustvarita seznam podatkov, vnosi katerega vsebujejo podatke o posameznem šahistu

def sirote_txt(txt_file):
#opomba za prihodnje - input txt_file, ki je ime datoteke, ki jo želimo osirotiti, more biti nujno STRING, ki vsebuje ime datoteke.
    with open(txt_file,'r') as dat:
        prebran_html = dat.read()
        sirote = re.split(r'bgcolor', prebran_html)
        odvecno = int(sirote[-1].index('<span class="article_separator">&nbsp;</span>') - 25)
        sirote[-1] = sirote[-1][0: odvecno]
        return sirote
    
def sirote_str(str_file):
    sirote = re.split(r'bgcolor', str_file)
    odvecno = int(sirote[-1].index('<span class="article_separator">&nbsp;</span>') - 25)
    sirote[-1] = sirote[-1][0: odvecno]
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

trenutno = requests.get('https://ratings.fide.com/toparc.phtml?cod=797')
vsebina = trenutno.text 

magnus = '=#ffffff><td width=10>&nbsp;1</a></td><td>&nbsp;Carlsen, Magnus</td><td>&nbsp;g</td><td>&nbsp;NOR</td><td>&nbsp;2832</td><td>&nbsp;0</td><td>&nbsp;1990</td></tr><tr'

print(dekompozicija(sirote_str(vsebina)[1]))


#shranjevanje podatkov: v .csv datoteko. Ime datoteke bo prvoime_prvipriimek, posamezna vrstica je indeksirana po mesecu ter letu, v vrstici je še rating in nacionalnost
#Za date of birth, naziv, ter popolne podatke o imenu (morebitno drugo ime ter drugi priimek) bomo pa shranili v data type sahist, ali pa v en massive seznam, katerega vnosi so slovarji 
#(al pa drug .csv)


#nespremenljive podatke kot so ime, naziv, ter leto rojstva shranimo v senam, podatke, ki so odvisni od časa, kot so rating, trenutni cas ter državljanstvo pa v .csv 
#(drzavljanstvo je dejansko spremenljivo; pimer je Richard Rapoport, ki je prešel iz Madžarske v Romunsko šahovsko zvezo)

