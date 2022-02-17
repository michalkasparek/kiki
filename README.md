# Kiki

Skript kontroluje stylistiku a gramatiku českých textů. Není náhradou kontroly pravopisu, je jejím doplněním. Napsal jsem ho, aby mi pomáhal při editování zpravodajských a publicistických článků, ale hodit se může i při finišování diplomky nebo románu.

Co přesně umí:

- Upozorňuje na klišé. Poradí si i s různými časy a tvary, neunikne mu _kostlivec ve skříni_ ani _kostlivci ve skříních_.
- Najde nejdelší větu. Tu jde obvykle zkrátit.
- Vypisuje slova následující po přímé řeči. Odhaluje tak opakování typu _prozradil – neprozradil – prozradil_.
- Vypisuje zduplikovaná slova.
- Vypisuje termíny v uvozovkách.
- Upozorňuje na nevhodně použitá interpunkční znaménka.
- Vypisuje úseky, ve kterých se objevují slova často používaná v nevhodném významu: _díky_, _Čechy_ nebo _Holandsko_.  
- Počítá základní statistiky, jako je rozsah a odhadovaná doba čtení.

Kiki pouze _pomáhá_, ale needituje. Soubor otevírá jen pro čtení. Neřeší, jestli ve švech praská divadlo, nebo sako. Staví vedle sebe jednoznačně odporné fráze i slova, která jsou ok, pokud se to s nimi nepřehání.

## Použití

Skript pochopitelně vyžaduje nainstalovaný Python, k němu ještě knihovny _nltk_ a _markdown_.

V konzoli nebo příkazové řádce použijte příkaz:

    kiki.py soubor_s_textem
  
Kiki si rozumí s prostým textem (například vykopírovaným z Wordu nebo GDocs) i s markdownem.

## Co je v plánu (jaro 2022)

- Průběžné rozšiřování seznamu klišé.
- Další upozornění: nejednotný sloh, opakující se začátky odstavců, edukativní modul "not OK boomer" (globální oteplování → klimatická krize).
- Oddělení programu a vstupních dat, s možností definovat uživatelské seznamy frází (např. ve sportovní redakci).
- Podpora YAML záhlaví markdownových souborů.
- [možná] Podpora formátu OpenDocument.
- [možná] Spustitelný soubor pro Windows, případně Mac OS.

## Poděkování

Seznam nevhodných obratů je posbíraný dílem z osobní praxe, dílem z interních materiálů několika vydavatelství. Velký dík kolegům a kolegyním za to, že se o ně podělili.

## Chce se vám blít z nějakého klišé, které Kiki nezná?

Sem s ním: [michal.kasparek@gmail.com](mailto:michal.kasparek@gmail.com).
