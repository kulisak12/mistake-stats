# Chyby v orientačním běhu

Orientační běh kombinuje dvě dovednosti, rychlý běh a čtení mapy. Závodníci se
snaží zaběhnout vytyčnou trať co nejrychleji. Časové ztráty mohou pramenit z
obou těchto složek, jak z pomalého běhu, tak z chyb v orientaci.

V této práci se zaměřuji na ztráty způsobené chybami a hledám vzory v nich. Dále
se zaměřuji na historii svých vlastních chyb, ze které lze pozorovat průběžný
zisk zkušeností a vylepšení dovedností vedoucí k omezení chyb.

Zdrojové kódy jsou dostupné v [tomto repozitáři]().

## Data

Všechny oficiální závody konané v České republice jsou dohledatelné v systému
[ORIS](https://oris.orientacnisporty.cz/?sport=1). Tento systém poskytuje
[API](https://oris.orientacnisporty.cz/API), prostřednictvím kterého je možné
data ze závodů získat.

U většiny závodů jsou dostupné mezičasy, tedy informace, v jakém čase doběhl
jaký závodník na jakou kontrolu. Čas, který závodník strávil mezi dvěma
kontrolami, lze použít k analýze chyb. Pokud je závodníkův čas významně vyšší
než čas ostatních závodníků, dá se předpokládat, že na postupu na danou kontrolu
udělal chybu.

Stažení dat z ORISu zajišťuje soubor [oris.py](). Stažená data ukládá na disk,
aby se omezil počet požadavků na API.

### Zpracování

Stažené mezičasy je nutné trochu zpracovat. Někteří závodníci totiž závod
nemuseli dokončit, případně některou kontrolu mohli vynechat. Poté nejsou
dostupné informace o času, který strávili postupem na danou a následující
kontrolu. Pro jednoduchost tyto závodníky z dat plně odstraňuji.

Do dat přidávám pouze ty závody, které dokončili alespoň 3 závodníci. Pro 2
závodníky totiž nelze rozlišit přirozený rozptyl časů od chyb.

### Detekce chyb

Není nijak definováno, co chyba je a co není. Pokusil jsem se tedy vytvořit
systém, který dle mého rozumně odpovídá skutečnosti.

Předpokládám, že časy závodníků, kteří chybu neudělali, budou odpovídat
rozdělení s poměrně malým rozptylem. Časy, které jsou o několik směrodatných
odchylek pomalejší než nejrychlejší dosažený čas, poukazují na chybu. Zvolil
jsem nejlepší čas místo průměrného proto, že na těžké kontrole může chybu udělat
většina závodníků.

Jak jsem ovšem zmínil na začátku, čas závodníka je určen i rychlostí běhu. Musím
tedy rozlišit běžeckou ztrátu od ztráty způsobené chybou. Budu předpokládat, že
běžecká rychlost závodníka v porovnání s ostatními je po celý závod stejná.
Tento předpoklad nutně nemusí platit, snadno se může stát, že někdo v úvodu
závodu přecení své síly a ke konci výrazně zpomalí. Bohužel, toto nejsem schopný
pouze z mezičasů detekovat.

Časy tedy normalizuji tak, aby celkový čas na celé trati byl pro každého
závodníka stejný. Tím se zbavím závislosti na rychlosti běhu.

Ve výjimečných případech se ovšem může stát, že jinak pomalý závodník zaběhne
jeden z postupů nezvykle rychle, například proto, že kontrolu našel již dříve.
Normalizace časů způsobí, že by jeho mezičas byl výrazně lepší než ostatní časy.
Proto před hledáním nejlepšího času nejprve najdu outliers a příliš rychlé časy
budu ignorovat.

Výše popsané zajišťuje soubor [course.py]().

### Dataset

Využívám data ze všech závodů, kterých jsem se kdy účastnil. Celkem se jedná o
83 závodů. O načtení se stará soubor [dataset.py]().

V některých statistikách průměruji všechny závodníky dohromady, v některých
uvažuji jen své výsledky.

### Konstanty

V detekci chyb popsané výše musím určit dvě konstanty: hranici příliš rychlých
časů, které chci ignorovat, a hranici chyby. V obou případech chci použít
z-score.
