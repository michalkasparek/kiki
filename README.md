# Kiki

Skript pomáhá odhalovat stylistické a gramatické nedostatky (českých) textů. Napsal jsem ho, aby mi asistoval při editování zpravodajských a publicistických článků, hodit se ale může i při finišování diplomky nebo románu.

Co přesně umí:

- Upozorňuje na klišé. Poradí si i s různými časy a tvary, neunikne mu _kostlivec ve skříni_ ani _kostlivci ve skříních_.
- Vypisuje slova následující po přímé řeči. Odhaluje tak opakování typu _prozradil – neprozradil – prozradil_.
- Hledá zduplikovaná slova (_jak řekl řekl_).
- Ukazuje termíny v uvozovkách (uvozovky jsou pro strašpytly).
- Vypichuje nejdelší větu (obvykle ji jde zkrátit).
- Upozorňuje na nevhodně použitá interpunkční znaménka.
- Zobrazuje úseky, ve kterých se objevují slova často používaná v nesprávném významu (_díky_, _Čechy_ nebo _Holandsko_).  
- Počítá základní statistiky, jako je rozsah a odhadovaná doba čtení.

Kiki pouze _pomáhá_, ale needituje. Soubor s textem otevírá jen pro čtení, nic v něm nemění. Neřeší, jestli ve švech praská divadlo, nebo sako. Staví vedle sebe jednoznačně odporné fráze i slova, která jsou ok, pokud se to s nimi nepřehání. Neřeší pravopis a překlepy – od toho tu jsou jiné nástroje.

## Použití

Ke spuštění skriptu potřebujete mít nainstalovaný Python, k němu ještě knihovny _nltk_ a _markdown_.

V konzoli nebo terminálu použijte příkaz:

    .\kiki.py soubor_s_textem
  
Kiki si rozumí s prostým textem (například vykopírovaným z Wordu nebo GDocs) i s markdownem.

Pokud chcete pohlídat frázi, kterou Kiki nezná, přidejte ji na samostatný řádek do nového souboru _ptydepe_pridej.txt_ ve složce _slovniky_. Podobně lze postupovat, když vám některé hledané fráze nevadí: vytvořte pro ně soubor _ptydepe_odeber.txt_. Jen pozor: frázi do něj musíte vložit přesně ve tvaru, v jakém se nachází v hlavním slovníku.

Samozřejmě můžete zasahovat i přímo do hlavních slovníků, to se ale po aktualizacích poprdíte.

## Co je nového

- 0.2: Seznamy frází už se načítají ze samostatných souborů ve složce _slovniky_. Tamtéž lze do souborů _ptydepe_pridej.txt_ a _ptydepe_odeber.txt_ vložit vlastní řetězce a regulérní výrazy, které má Kiki extra hledat, nebo naopak ignorovat. (22. 2. 2022)

## Co je v plánu

- Průběžné rozšiřování seznamu klišé.
- Další upozornění: nejednotný sloh, nadužívání konkrétních spojek, opakující se začátky odstavců, edukativní prvek "not OK boomer" (globální oteplování → klimatická krize) aj.
- Podpora YAML záhlaví markdownových souborů.
- [možná] Podpora formátu OpenDocument.
- [možná] Spustitelný soubor pro Windows a macOS.

## Poděkování

Seznam nevhodných obratů je posbíraný dílem z osobní praxe, dílem z interních materiálů několika vydavatelství. Velký dík kolegům a kolegyním za to, že se o ně podělili.

Kiki jsem pojmenoval po své manželce Kristýně, výjimečně pozorné a pečlivé editorce.

## Kontakt

[michal.kasparek@gmail.com](mailto:michal.kasparek@gmail.com)