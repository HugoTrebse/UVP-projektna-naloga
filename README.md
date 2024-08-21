# UVP projektna naloga
**Projektna naloga študenta Hugo Trebše za predmet Uvod v Programiranje.**

V okviru te projektne naloge bom zbral točke ELO top 100 Šahistov od leta 2000 do leta 2024 ter analiziral določene trende pristone v teh podatkih.

## Parametrizacija URL-jev
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

Sedaj lahko uspešno ustvarimo funkcijo, ki iz indeksa num pridobi mesec kategerga je bila objavljena tabela.

**TODO:**
- [x] Zajem podatkov ter kreacija ustreznega razreda
    - [x] Prenašanje ustreznih HMTL strani
    - [x] Parsing ter razporeditev v razrede
- [ ] Analiza podatkov, vključujoče:
  - Starost šahistov v odvisnosti od *peak* ratinga
  - Nihanje ratinga v odvisnosti od države/starosti
