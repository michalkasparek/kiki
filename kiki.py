#!/usr/bin/env python
"""
Skript pomáhá hlídat stylistiku a gramatiku při editování českých textů určených širokému publiku.

__version__ = "0.1"
__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

import sys # umožní čtení argumentů z příkazové řádky
import re # umožní práci s regulérními výrazy
from markdown import markdown # umožní práci s markdownem
import nltk # umožní tokenizaci do vět

# Definice

ptydepe = ["absolutn\w{1,3}\s\wjistot\w+", "(?<!\w)během", "bitv\w+\so\s\w+", "bobřík\w{,3}", "brous\w+\szuby", "cel\w{1,3}\sřad\w{1,3}", "cel\w{,3}\sinterne\w{1,3}", "co se týče", "čas ukáže", "časovan\w+\sbomb\w+", "časov\w+\shorizont\w+", "člověčenství", "člověčin\w+", "dál\w?\sprohl\w+", "daňov\w+\spoplatní\w+", "(?<!\w)dedik\w+", "(?<!\w)diskur\w+", "\w{,2}dojde\sk\s\w+", "domác\w+\smazlíč\w+", "doslova", "\w{,2}došlo\sk\s\w+", "drtiv\w+\světšin\w+", "druhak", "\w*financov\w+", "finančn\w+\sprostředk\w+", "hlavní\w*\sprotagonist\w{1,4}", "jablk\w+\ssváru", "jak\w?\spo\smásle", "\w{,3}kontrover\w+", "kostliv\w+\sskřín\w+", "křišťálov\w+\skoul\w+", "lesbičk\w+", "kudy běží zajíc", "kultovn\w+", "kvituji", "kvitova\w+", "lidsk\w+\sfakto\w+", "manuálw\+\szručn\w+", "medvědí\sslužb\w+", "mráz po zádech", "muž\w+\szákona", "na dlouhou trať", "na kobereček", "na poli", "na půdě", "na pořadu dne", "na pravém místě", "na svém místě", "napříč spektrem", "narativ\w*", "následně", "nic snazšího", "nepřizpůsobiv\w+", "nervy v kýblu", "n\wž\w{1,2}\sna\skrk\w?", "o čem přemýšlet", "olej do ohně", "ostře kritiz\w+","ostr\w+ kritik\w+", "paradigm\w+", "part\w+\snadšenců", "platform\w+", "pod taktovkou", "pojďme", "posvě\w+", "prask\w+\sve\sšvech", "projekt\w{,3}", "prostě", "prý", "přehrš\w+", "rasov\w+\spodtext\w*", "realiz\w+", "s kůží na trh", "sněhov\w+\s\nadílk\w+", "státn\w+\skas\w{1,5}", "soubo\w+\stitánů", "svého času", "svým způsobem", "širok\w+\s\veřejnos\w+", "špičk\w{1,3}\sledovc+", "tah\w{,2}\sna\sbranku", "totiž", "třešničk\w+\sna\sdortu", "tuzemsk\w+", "údajně", "úheln\w+\sk\wmen\w*", "v neposlední řadě", "v podstatě", "v pravý čas", "v průběhu", "v rámci", "v současnosti", "větší\w* jak[^\w]", "víc\w*\sjak(?=\s)", "vlajkov\w+\slo\w{1,2}", "vlastně", "volnočasov\w+\saktivi\w+", "\w{,2}vykomuni\w+", "vymalováno", "z důvodu", "z našich daní", "z pochopitelných důvodů", "zainvestov\w+", "\w{,3}zajímav\w+", "zelen\w+ razítk\w+", "ztrá\w{1,4}\sna\sživotech", "želíz\w+\sv\sohni"]
typochyby = ["\.\.\.", "--", "\d{1,8}-?ti\w{,10}", "\d{1,12}x", "\"\w{1,}", "\w{1,}[\.,\?!]?\"", ",[^\W\d_]{1,12}", "\w{1,12}\'"]
kontextovky = ["[\s\S]{25}kvůli[\s\S]{44}", "[\s\S]{25}díky[^!,\.\w][\s\S]{44}", "[\s\S]{24}\sšanc[\s\S]{45}", "[\s\S]{24}\sČech[\s\S]{45}", "[\s\S]{25}Holandsk[\s\S]{41}", "[\s\S]{25}Holanďan[\s\S]{41}"]

# Načtení souboru

file = open(sys.argv[1], encoding="utf8") # otevře soubor volaný argumentem z příkazové řádky
content = file.read() # načte obsah souboru

# Konverze formátu

html = markdown(content) # převede markdown na html
plaintext = re.sub("<(/)?br(/)?>", "\n", html) # odstraní z html tag <br> a nahradí ho zalomením řádky
plaintext = re.sub("<[^>]*>", "", plaintext) # odstraní z html ostatní tagy
plaintextoneline = re.sub ("\n", " ", plaintext) # verze na jedné řádce, bude se hodit pro hledání kontextovek
titulek = plaintext.partition('\n')[0] # vybere první řádek jako titulek (pro výpis statistik)

# Počet slov a nejdelší slovo

slova = re.sub("https?:\/\/\S*", "", plaintext) # odstraní všechny url adresy
slova = re.sub("[,\.:;!?„“…'\"\']", "", slova) # vymaže interpunkci
slova = re.sub("(-|–|—)", " ", slova) # dlouhá-sousloví se nebudou počítat jako jedno slovo
slova = slova.split() # rozdělí předchystaný obsah na slova
pocetslov = len(slova) # počet slov v dokumentu
pocetznaku = len(plaintext) # počet znaků v dokumentu
ns = round(pocetznaku / 1800, 1) # vydělí počet znaků 1800 a zaokrouhlí na 1 desetinné místo
ns = str(ns) # převede počet normostran na string
ns = ns.replace(".", ",") # vymění anglickou desetinnou tečku za českou desetinnou čárku
minutycteni = round(pocetslov/200) # průměrný čtenář přečte za minutu 200 slov (zdroj: internet)
nejdelsislovo = max(slova, key=len) # najde nejdelší slovo
nejdelsislovodelka = len(nejdelsislovo) # počet znaků v nejdelším slově

# Nejdelší věta

sentences = re.sub("[„“]", "", plaintext) # odstraní uvozovky
sentences = re.sub("\s+\n", "\n", sentences) # odstraní mezery z konců odstavců
sentences = re.sub("(\w)\n", "\\1.\n", sentences) # doplní tečku za neohraničené odstavce (např. mezititulky)
sentences = nltk.sent_tokenize(sentences) # tokenizuje předchystaný obsah na věty
nejdelsiveta = max(sentences, key=len) # najde nejdelší větu
nejdelsivetaznaky = len(nejdelsiveta) # počet znaků v nejdelší větě
nejdelsivetaslova = len(nejdelsiveta.split()) # počet slov v nejdelší větě

# Slova za uvozovkami

citace = re.split("[,\?\!]“[^\n]", plaintext) # rozdělí dokument v místech, kde jdou po sobě čárka, otazník nebo vykřičník a uvozovky, a za nimi nenásleduje konec řádku
del citace[0] # smaže, co předchází konci první citace
slovapouvozovkach = [x.split()[0] for x in citace] # najde první slovo v každém řetězci
slovapouvozovkach = [re.sub("[\.,\?:;]", "", x) for x in slovapouvozovkach] # odstraní bordýlek

# Ošklivé fráze

nalezeneptydepe = [] # vytvoří prázdný seznam pro nalezené chyby
for ptydepe in ptydepe: # jedna chyba za druhou
	nalezenachyba = re.findall(ptydepe, plaintext, re.IGNORECASE) # vyhledá všechny výskyty chyb
	nalezeneptydepe.append(nalezenachyba) # každou nalezenou chybu doplní do seznamu

# Jedno slovo dvakrát po sobě

opakovani = re.findall("\\b(\\w+)\\s\\1\\b", plaintext, re.IGNORECASE) # vyhledá duplikáty
opakovani = [re.sub("(\\w+)", "\\1 \\1", x) for x in opakovani] # zduplikuje duplikáty (asi by to mělo jít i lepším regexem v předchozím řádku)

# Pojmy v uvozovkách

uvozovky = re.findall("„\\w+\\s*\\w*\\s*\\w*“", plaintext, re.IGNORECASE) # 1 až 3 slova mezi uvozovkami

# Typografické chyby

nalezenetypochyby = [] # vytvoří prázdný seznam pro nalezené chyby
for typochyby in typochyby: # jedna chyba za druhou
	nalezenatypochyba = re.findall(typochyby, plaintext, re.IGNORECASE) # vyhledá všechny výskyty chyb
	nalezenetypochyby.append(nalezenatypochyba) # každou nalezenou chybu doplní do seznamu

# Slova, u kterých je nutné pohlídat kontext

nalezenekontextovky = []
for kontextovky in kontextovky:
	nalezenakontextovka = re.findall(kontextovky, plaintextoneline, re.IGNORECASE)
	nalezenekontextovky.append(nalezenakontextovka)
				
# Úprava seznamů pro pěkný výstup

nalezeneptydepe = list(filter(None, nalezeneptydepe)) # vymaže prázdné subsety
nalezeneptydepe = sum(nalezeneptydepe, []) # spojí subsety do jednoho setu
	
nalezenetypochyby = list(filter(None, nalezenetypochyby)) # vymaže prázdné subsety
nalezenetypochyby = sum(nalezenetypochyby, []) # spojí subsety do jednoho setu

nalezenekontextovky = sum(nalezenekontextovky, []) # vymaže prázdné subsety

# Výpis

print ("*** KIKI POMÁHÁ S EDITOVÁNÍM {-_-} ***\n")
print (titulek, "\n- titulek:", len(titulek), "znaků s mezerami\n- dokument:", pocetznaku, "znaků s mezerami,", pocetslov, "slov,", ns, "NS,", minutycteni, "min čtení\n")
print ("Nejdelší slovo:\n- " + str(nejdelsislovo) + " (" + str(nejdelsislovodelka) + " znaků)\n")
if nejdelsivetaznaky > 160:
	print ("Nejdelší věta:\n- " + str(nejdelsiveta) + " ("+ str(nejdelsivetaslova) + " slov, " + str(nejdelsivetaznaky) + " znaků)\n")
if len(slovapouvozovkach)!= 0:
	print ("Pořadí slov po citacích:")
	print ("-", ", ".join(slovapouvozovkach), "\n")
if len(nalezeneptydepe) != 0:
	print ("Problematická slova a obraty:")
	print ("-", ", ".join(nalezeneptydepe), "\n")
if len(opakovani) != 0:
	print ("Zduplikovaná slova:")
	print ("-", ", ".join(opakovani), "\n")
if len(nalezenetypochyby) != 0:
	print ("Typografické chyby:")
	for x in nalezenetypochyby:
		print ("-", x)
	print ("Správná znaménka ke zkopírování: … „ “ ‚ ‘ ×\n")
if len(uvozovky) != 0:
	print ("Termity v uvozovkách:")
	print ("-", ", ".join(uvozovky), "\n")
if len(nalezenekontextovky) != 0:
	print ("Pohlídat význam:           ▼")
	for x in nalezenekontextovky:
		print ("-", x)
