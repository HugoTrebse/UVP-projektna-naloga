# UVP projektna naloga
**Projektna naloga študenta Hugo Trebše za predmet Uvod v Programiranje.**

V okviru te projektne naloge bom zbral podatke o ELO ratingu top 100 Šahistov od leta 2000 do leta 2024 ter analiziral nekatere prisotne trende.

## Navodila za uporabo
### Python ter git
Potreben pogoj za uspešno uporabo je nameščen Python ter git, po možnosti katero izmed novejših verzij.
### Nalaganje datotek
Da naložite vse potrebne datoteke za uporabo v ukazno vrstico napišite:
```console
git clone https://github.com/HugoTrebse/UVP-projektna-naloga.git
```
### Nameščanje knjižnjic
Potrebno je naložiti tudi nekaj knjižnjic. To storite v ukazni vrstici na naslednji način:
```console
pip install re requests csv os copy pandas matplotlib
```
### Uporaba programa:
Najprej se z ukazoma  ``` cd ``` ter ``` dir ``` orientirajte do mape, v kateri se nahajajo datoteke, ki smo jih naložili v prejšnjem koraku.
Nato poženite naslednji ukaz:
```console
python main.py
```
### Dostop do analize podatkov
Analiza zbranih podatkov se nahaja v datoteki ```analiza_podatkov.ipynb```.
Datoteko lahko odpremo z poljubnim programom, ki je namenjen branju Jupyter Notebooka. Če takega programa nimate nameščenega, pa vam priporoča, da si končno obliko datoteko ogledate kar na githubu na [naslednjem linku](https://github.com/HugoTrebse/UVP-projektna-naloga/blob/main/analiza_podatkov.ipynb).
## Izgled HTML kode spletišča https://ratings.fide.com/
Za dostop do informacij o točkah ELO (ter tudi nekaterih drugih podatkih) najboljših 100 šahistov med leti 2000 ter 2024, bomo uporabljali spletišče Mednarodne šahovske federacije (FIDE): https://ratings.fide.com/. 

Tipična URL povezava do tabele za dani mesec je oblike: https://ratings.fide.com/toparc.phtml?cod=1 ; kjer končnica cod=num parametrizira zaporedni vnos podatkov. Opaziomo, da v odvisnosti od num modulo 4 dobimo sledeče kategorije šahistov:

|   num    |  mod 4  |
| -------- | ------- |
|    1     | odprta kategorija   |
|    2     | ženska kategorija     |
|    3     | kategorija juniorjev   |
|    4     | kategorija juniork |

Za vrednost num=1 pa dobimo tabelo s podatki o najboljših 100 šahistih v odprti sekciji za mesec julij leta 2000, za vrednost num=5 dobimo tabelo s podatki o najboljših šahistih v odpri sekciji za mesec oktober leta 2000 ipd.

Z nekaj ročne analize (ter z pomočjo bisekcije) ugotovimo, da so med julijem leta 2000 (num=1) in julijem leta 2009 (num=145) tabelo objavljali vsake tri mesece (januar, april, julij ter oktober); nakar je prišlo do spremembe. Od septembra 2009 (num=149) do maja 2012 (num=213) pa so tabelo objavljali vsak drugi mesec (januar, marec, maj, julij, september, november), nato pa so prešli na trenutni sistem mesečnih objav tabel, ki velja od julija 2012 (num=217).

|   Pogostost    |  Trajanje  | num |
| -------- | ------- | --------- |
|    3x letno     |  julij 2000 - julij 2009  | 1 - 145 |
|    6x letno     | september 2009 - maj 2012 | 145 - 217|
|    12x letno    | julij 2012 - | 217  - |
