import requests
import funkcije
# funkcije uporabimo tako: funkcije.ime_funkcije_ki_jo_uporabimo
obstojeci_sahisti = set()


parent_html = r'https://ratings.fide.com/toparc.phtml?cod='

for i in range(199):
    r = requests.get(f'{parent_html}{797-4*i}')
    vsebina = r.text
    posamezniki = funkcije.sirote(vsebina)
    date = funkcije.date_extractor(vsebina)
    for posameznik in posamezniki:
        decomposed = funkcije.dekompozicija(posameznik)
        funkcije.splosna_evidenca(decomposed[0], decomposed[5], obstojeci_sahisti)
        funkcije.pisatelj_csvjev(decomposed, date)
