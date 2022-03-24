# Kiki

Skript pomáhá odhalovat stylistické nedostatky (českých) textů. Napsal jsem ho, aby mi asistoval při editování zpravodajských a publicistických článků, hodit se ale může i při finišování diplomky nebo románu.

Co přesně umí:

- Upozorňuje na klišé. Poradí si i s různými časy a tvary, neunikne mu _kostlivec ve skříni_ ani _kostlivci ve skříních_. U některých zastaralých, zavádějících nebo nekorektních termínů připojuje vysvětlení a alternativu (_globální oteplování_ → _změna klimatu_).
- Vypisuje slova následující po přímé řeči. Odhaluje tak opakování typu _prozradil – neprozradil – prozradil_.
- Hledá zduplikovaná slova (_jak řekl řekl_).
- Ukazuje termíny v uvozovkách (uvozovky jsou pro strašpytly).
- Vypichuje nejdelší větu (obvykle ji jde zkrátit) plus věty s nejvíce interpunkčními znaménky a nejvíce opakováním zájmen který/která/které.
- Upozorňuje na nevhodně použitá interpunkční znaménka.
- Zobrazuje úseky, ve kterých se objevují slova často používaná v nesprávném významu (_díky_, _Čechy_ nebo _Holandsko_).  
- Počítá základní statistiky, jako je rozsah a odhadovaná doba čtení.

Kiki pouze _pomáhá_, ale needituje. Soubor s textem otevírá jen pro čtení, nic v něm nemění. Neřeší, jestli ve švech praská divadlo, nebo sako. Staví vedle sebe jednoznačně odporné fráze i slova, která jsou ok, pokud se to s nimi nepřehání. Neřeší pravopis a překlepy – od toho tu jsou jiné nástroje.

## Použití

Ke spuštění skriptu potřebujete mít nainstalovaný Python, k němu ještě knihovny ```nltk``` a ```markdown``` (```pip install nltk``` a ```pip install markdown```).

Skript ```Kiki.py``` a složku se slovníky stáhněte, kam potřebujete.

V konzoli nebo terminálu použijte příkaz:

    .\kiki.py název_souboru_s_textem

nebo:

    python kiki.py název_souboru_s_textem
  
Kiki si rozumí s prostým textem (například vykopírovaným z Wordu nebo GDocs) i s markdownem.

Pokud chcete pohlídat frázi, kterou Kiki nezná, přidejte ji na samostatný řádek do nového souboru _ptydepe_pridej.txt_ ve složce _slovniky_. Podobně lze postupovat, když vám některé hledané fráze nevadí: vytvořte pro ně soubor _ptydepe_odeber.txt_. Jen pozor: frázi do něj musíte vložit přesně ve tvaru, v jakém se nachází v hlavním slovníku.

Samozřejmě můžete zasahovat i přímo do hlavních slovníků, to se ale po aktualizacích poprdíte.

## Co je nového

- 0.3: Hledání vět s nejvíce interpunkčními znaménky a nejvíckrát opakujích zájmeno „kter*“. Upozorňování na zastaralé nebo nekorektní fráze s vysvětlením. (25. 3. 2022)
- 0.2: Seznamy frází už se načítají ze samostatných souborů ve složce _slovniky_. Tamtéž lze do souborů _ptydepe_pridej.txt_ a _ptydepe_odeber.txt_ vložit vlastní řetězce a regulérní výrazy, které má Kiki extra hledat, nebo naopak ignorovat. (22. 2. 2022)

## Co je v plánu

- Průběžné rozšiřování seznamů frází.
- Další upozornění: nejednotný sloh, opakující se začátky odstavců aj.
- Podpora YAML záhlaví markdownových souborů.
- Refaktorování: zbavit se závislosti na knihovnách _nltk_ a _markdown_, napsat funkce volatelné z jiných skriptů.
- [možná] Podpora formátů OpenDocument a Docx.
- [možná] Spustitelný soubor pro Windows a macOS.

## Zdroje

Seznam nevhodných obratů je posbíraný dílem z osobní praxe, dílem z interních materiálů několika redakcí, mj. MFD, HN a Deníku. Velký dík kolegům a kolegyním za to, že se o ně podělili. Pomohla i [diplomová práce Heleny Palátové](https://is.muni.cz/th/pvfvs/floskule_bp.pdf).

Modul Not ok boomer čerpá mimo jiné z manuálu [Jak mluvit a psát o lidech s postižením](https://www.ochrance.cz/aktualne/lide-s-postizenim-maji-mit-respekt-kvuli-sobe-nikoli-kvuli-postizeni/) publikovaného kanceláří Veřejného ochránce práv.

## Věnování

Kiki jsem pojmenoval po své manželce [Kristýně](https://www.linkedin.com/in/krist%C3%BDna-ka%C5%A1p%C3%A1rkov%C3%A1-a733131ba/?originalSubdomain=cz), výjimečně pozorné a pečlivé editorce.

## Kontakt

[michal.kasparek@gmail.com](mailto:michal.kasparek@gmail.com)