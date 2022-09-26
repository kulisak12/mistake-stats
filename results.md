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

Jak jsem zmínil na začátku, čas závodníka je určen i rychlostí běhu. Prvně tedy
musím rozlišit běžeckou ztrátu od ztráty způsobené chybou. Budu předpokládat, že
běžecká rychlost závodníka v poměru s ostatními je po celý závod stejná.
Tento předpoklad nutně nemusí platit, snadno se může stát, že někdo v úvodu
závodu přecení své síly a ke konci výrazně zpomalí. Bohužel, toto nejsem schopný
pouze na základě mezičasů odlišit od chyb.

Časy tedy normalizuji tak, aby celkový čas na celé trati byl pro každého
závodníka stejný. Tím se zbavím závislosti na rychlosti běhu.

Následně pro každého závodníka spočítám jeho ztrátu na postupu jako rozdíl jeho
času a nejlepšího dosaženého času. Pokud ztráta převyšuje určitou mez, prohlásím
to za chybu.

Otázkou zůstává, jak tuto mez určit. Mez nebude vždy stejná, protože v
orientačním běhu se závodní v různých disciplínách lišících se délkou. Ztráta 30
vteřin by v nejdelší disciplíně, na klasické trati, chybu nejspíše neznamenala,
zatímco ve sprintu se již jedná o hrubou chybu. Dává tedy smysl uvažovat ztrátu
v poměru k délce závodu.

Rozhodl jsem se zavést dvě třídy chyb:
- Malé chyby, u kterých ztráta na postupu převyšuje 1/50 délky závodu. To by
  podle oficiálních směrných časů v kategorii H21 znamenalo 14 s na sprintu, 42
  s na krátké trati a 90 s na klasické trati.
- Velké chyby, u kterých ztráta převyšuje 1/20 délky závodu, což odpovídá ztrátě
  36 s, 105 s, respektive 225 s.

Výše popsané zajišťuje soubor [course.py]().

### Dataset

Využívám data ze všech závodů, kterých jsem se kdy účastnil. Celkem se jedná o
83 závodů. O načtení se stará soubor [dataset.py]().

V některých statistikách průměruji všechny závodníky dohromady, v některých
uvažuji jen své výsledky.
