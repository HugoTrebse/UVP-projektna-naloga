import funkcije
import pandas as pd
import os
from statistics import mean

pot_plitka = os.getcwd()
pot_globoka =  os.path.join(pot_plitka, 'podatkovna_baza')
pot_sahisti = os.path.join(pot_plitka, 'sahisti')

def zdruzevalnik(lokacija_csv_1, lokacija_csv_2):
    csv_1_df = pd.read_csv(lokacija_csv_1)
    csv_2_df = pd.read_csv(lokacija_csv_2)
    zdruzen_df = pd.concat([csv_1_df, csv_2_df])
    zdruzen_df['pravi_datum'] = pd.to_datetime(zdruzen_df['datum'], format='%m-%Y')
    urejen_df = zdruzen_df.sort_values(by= 'pravi_datum')
    urejen_df = urejen_df.drop(columns = 'pravi_datum')
    return urejen_df

def popravljalnik(ekvivalence, ekvivalentna_imena):
    for ekvivalentna_imena in ekvivalence:
        prihodnje_ime = ekvivalentna_imena[0]
        #Naslednje vrstice na ustrezen način spremenijo sahisti.csv.
        sahisti_prebrano = pd.read_csv(pot_sahisti)
        indeksi_za_izbris = []
        for indeks, (ime, leto_rojstva) in sahisti_prebrano.iterrows():
            if ime in ekvivalentna_imena and ime != ekvivalentna_imena[0]:
                indeksi_za_izbris.append(indeks)
        sahisti_spremenjeno = sahisti_prebrano.drop(indeksi_za_izbris)
        sahisti_spremenjeno.to_csv(pot_sahisti, index=False)
        #naslednjih par vrstic dzruzi DataFrame ter jih pretvori v en .csv
        for ime in ekvivalentna_imena:
            if ime != prihodnje_ime:
                zdruzen_df = zdruzevalnik(funkcije.ime_v_pot(prihodnje_ime), funkcije.ime_v_pot(ime))
                zdruzen_df.to_csv(funkcije.ime_v_pot(prihodnje_ime), index=False)
                os.remove(funkcije.ime_v_pot(ime))

def pridobi_splosne_informacje():
    sahisti_prikaz_2 = []
    for ime_sahista, vrstica in pd.read_csv(pot_sahisti, index_col = 'Ime').iterrows():
        leto_rojstva = vrstica['Leto rojstva']
        prebrana_datoteka = pd.read_csv(funkcije.ime_v_pot(ime_sahista))
        trenutni_maksimum = 0
        drzava = None
        for indeks, vrstica in prebrana_datoteka.iterrows():
            trenutni_maksimum = max(trenutni_maksimum, vrstica['rating'])
            if indeks == 0:
                drzava = vrstica['drzava']
        sahisti_prikaz_2.append({'Ime': ime_sahista, 'Leto rojstva': leto_rojstva, 'Drzava': drzava, 'Najvišji rating': trenutni_maksimum})
    return sahisti_prikaz_2

#Napišimo funkcijo, ki vrne strukturo vsebujočo informacije o šahistih, ki so bili v top k-mestih.
def podatki_top_nekaj(k):
    podatki_sahistov_v_top_nekaj = {}
    sahisti = pd.read_csv(pot_sahisti, index_col= 'Ime')
    for ime, vrstica in sahisti.iterrows():
        if ime == 'Leto rojstva\'' or ime == 'Leto rojstva':
            pass
        else:
            podatki = pd.read_csv(funkcije.ime_v_pot(ime))
            for indeks, vrstica2 in podatki.iterrows():
                if vrstica2.iloc[3] <= k:
                    podatki_sahistov_v_top_nekaj[(ime, int(vrstica['Leto rojstva']))] = podatki
    return podatki_sahistov_v_top_nekaj
#funkcija vrne slovar, kjer nabor (ime, leto_rojstva) kaže na podatke dotičnega šahista, prebrane s programom pandas

#Ker nimamo podatkov o ratingu vsakega izmed šahistov za vsako starost, morda ker starosti še niso dosegli, morda ker pri določeni starosti niso bili med najboljšimi 100 šahisti,
#ali pa ker so to starost dosegli pred letom 2000, bomo do podatkov o povprečju prišli na naslednji način.
def obrezovalec(slovar):
    #ker v funkciji povprecje_v_populaciji(n) pridobivamo podatke za različne demografike bomo prej ali slej naleteli na demografiko, ki ne bo imela nobenega 73-letnika
    #(najstarejši šahist za katerega zajamemo podatke je Viktor Krochnoi pri rosnih 73 letih). Da bodo grafi, ki jih rišemo bolj reprezentativni bo ta funkcija izbrisala vse vnose slovarja.
    #ki imajo ničelne vrednosti
    return {kljuc : vrednost for kljuc, vrednost in slovar.items() if vrednost != 0}

#Funkcija sprejme populacijo (top n šahistov) ter za vse igralce v populaciji pridobi rating pri vseh moznih starostih.
#Nato pridobljene podatke povpreci, tako da vsoto podatkov o ELO ratingu za vsako starost deli s št. podatkov.
#Nato odstrani vse starosti, za katere podatkov nismo prejeli ter vrne slovar, kjer kljuci predstavljajo starost, vrednosti pa povprecni ELO.

def kalkulator_povprecja(slovar):
    povprecje = {i: 0 for i in range(15, 74)}
    for starost in slovar:
        vsota = sum(slovar[starost])
        dolzina = len(slovar[starost])
        if dolzina != 0:
            povprecje[starost] = round(vsota / dolzina, 2)
        else:
            pass
    return obrezovalec(povprecje)

def povprecje_v_populaciji(n):
    kolekcija_elo_pri_dani_starosti = {i: [] for i in range(15, 74)}
    for sahist, leto_rojstva in podatki_top_nekaj(n):
        sahistov_record = pd.read_csv(funkcije.ime_v_pot(sahist), index_col = 'datum')
        for datum, vrstica in sahistov_record.iterrows():
            leto = int(datum[3::])
            if leto - leto_rojstva >= 15 and leto - leto_rojstva <= 73:
                kolekcija_elo_pri_dani_starosti[leto - leto_rojstva].append(vrstica['rating'])

    return kalkulator_povprecja(kolekcija_elo_pri_dani_starosti)

#Funkcija vrne par velikostni_ekstrem (seznam) ter najvisji (int), kjer je najvisji enak najvisjemu ratingu, ki ga v povprecju dosezejo sahisti
#iz populacije top n, ter je velikostni_ekstrem seznam starosti, pri katerih ta maksimum dosezejo.
def maksimum_v_povprecju_populacije(informacije, n):
    velikostni_ekstrem = []
    najvisji = max(list(povprecje_v_populaciji(n).values()))
    for starost, rating_pri_starosti in informacije.items():
        if rating_pri_starosti == najvisji:
            velikostni_ekstrem.append(starost)
    return velikostni_ekstrem, int(najvisji)

def dodajalec(slovar, kljuc, vrednost):
    if kljuc in slovar:
        slovar[kljuc] += vrednost
    else:
        slovar[kljuc] = vrednost

#Ker se zdi pravično, da bi zbrani podatki o deležih šahistov iz posamezne države, odražali 'prisotnost' te države na lestvici top 100 posežemo po naslednjem načrtu.
#Za vsakega šahista preverimo vsako vrstico v njegovem .csvju ter poglejmo za katero državo igra tedaj, nato pa te podatke zbrali v slovar.

#zelel bi se info o tem kaj je največja država in ker delež informacij prispeva
def drzave_splosne_informacije():
    drzave = {}
    pogostost_drzav = {}
    sahisti_prebrano = pd.read_csv(pot_sahisti, index_col = 'Ime')
    for ime_sahista, leto_rojstva in sahisti_prebrano.iterrows():
        prebrana_datoteka = pd.read_csv(funkcije.ime_v_pot(ime_sahista))
        stevec_drzav = prebrana_datoteka['drzava'].value_counts()
        for drzava, stevec in stevec_drzav.items():
            dodajalec(pogostost_drzav, drzava, stevec)
            drzave[drzava] = []
    trenutni_zmagovalec = (' ', 0)
    stevilo_podatkov =  0
    for drzava, pogostost in pogostost_drzav.items():
        stevilo_podatkov += pogostost
        if pogostost > trenutni_zmagovalec[1]:
            trenutni_zmagovalec = (drzava, pogostost)
    meja = int(stevilo_podatkov * 0.02)
    return pogostost_drzav, drzave, stevilo_podatkov, meja, trenutni_zmagovalec

def pogostost_drzav_nad_mejo(pogostost_drzav, meja):
    drzave_nad_mejo = set()
    pogostost_drzav_nad_mejo = {'preostalo': 0}
    for drzava, pogostost in pogostost_drzav.items():
        if pogostost >= meja:
            dodajalec(pogostost_drzav_nad_mejo, drzava, pogostost)
            drzave_nad_mejo.add(drzava)
        elif pogostost < meja:
            pogostost_drzav_nad_mejo['preostalo'] += pogostost
    return pogostost_drzav_nad_mejo, drzave_nad_mejo

def ustvarjalec_drzav(slovar):
    sahisti_prebrano = pd.read_csv(pot_sahisti, index_col = 'Ime')
    for ime_sahista, leto_rojstva in sahisti_prebrano.iterrows():
        prebrana_datoteka = pd.read_csv(funkcije.ime_v_pot(ime_sahista))
        for indeks, vrstica in prebrana_datoteka.iterrows():
            slovar[vrstica['drzava']].append(vrstica['rating'])
    return slovar

def eksplozija(pogostost_drzav_nad_mejo, najproduktivnejsa_drzava):
    eksplozija = []
    for drzava, st_podatkov in pogostost_drzav_nad_mejo.items():
        if drzava == najproduktivnejsa_drzava[0]:
            eksplozija.append(0.1)
        else:
            eksplozija.append(0)
    return eksplozija

def ustvarjalec_maksimumom_drzav(slovar):
    maksimumi_drzave = {}
    for drzava, ratingi in slovar.items():
        maksimumi_drzave[drzava] = max(ratingi)
    return maksimumi_drzave

def informacije_o_mnozici_drzav(mnozica_drzav, informacije):
    informacije_o_mnozici = {}
    for drzava, info in informacije.items():
        if drzava in mnozica_drzav:
            informacije_o_mnozici[drzava] = info
    return informacije_o_mnozici

