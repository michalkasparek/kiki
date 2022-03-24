#!/usr/bin/env python
"""
Skript upozorňuje na stylistické nedostatky (českých) textů.

__version__ = "0.3"
__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

import sys # čtení argumentů z příkazové řádky
import os # načítání souborů z podadresářů na různých platformách
import re # práce s regulérními výrazy
from markdown import markdown # práce s markdownem
import nltk # tokenizace do vět

# Načtení souboru s textem

try:
	dokument = open(sys.argv[1], mode="r", encoding="utf-8") # otevře soubor volaný argumentem z příkazové řádky
	obsah = dokument.read() # načte obsah souboru
except UnicodeDecodeError: 
	dokument = open(sys.argv[1], mode="r") # pro txt uložené v libre docs s jiným kódováním
	obsah = dokument.read()
except FileNotFoundError:
	print ("Soubor nenalezen.")
	quit()

# Načtení slovníků

ptydepe = open(os.path.join("slovniky", "ptydepe.txt"), "r", encoding="utf8") # otevře soubor se seznamem zakázaných výrazů
ptydepe = ptydepe.read().splitlines() # načte obsah souboru po řádcích jako seznam, bez přidávání \n na konec každé položky
notokboomervstup = open(os.path.join("slovniky", "notokboomer.txt"), "r", encoding="utf8")
notokboomervstup = notokboomervstup.read().splitlines()
notokboomer = {} # vytvoří prázdný slovník pro zastaralé obraty
for line in notokboomervstup:
	key = line.split(";")[0] # načte z každé řádky obsah před středníkem (regex s různými tvary spojení)
	value = line.split(";")[1] # a obsah za středníkem (vysvětlení, proč je spojení blbě)
	notokboomer[key] = value # přidá je do slovníku jako klíč a hodnotu
typochyby = open(os.path.join("slovniky", "typochyby.txt"), "r", encoding="utf8")
typochyby = typochyby.read().splitlines()
kontextovky = open(os.path.join("slovniky", "kontextovky.txt"), "r", encoding="utf8")
kontextovky = kontextovky.read().splitlines()

# Přidání a odebrání uživatelských slovníků

if os.path.exists(os.path.join("slovniky", "ptydepe_pridej.txt")):
	ptydepepridej = open(os.path.join("slovniky", "ptydepe_pridej.txt"), "r", encoding="utf8") # otevře soubor s výrazy, které hodlá uživatel(ka) extra hledat
	ptydepepridej = ptydepepridej.read().splitlines()
	ptydepe = ptydepe + ptydepepridej

if os.path.exists(os.path.join("slovniky", "ptydepe_odeber.txt")):
	ptydepeodeber = open(os.path.join("slovniky", "ptydepe_odeber.txt"), "r", encoding="utf8") # otevře soubor s výrazy, které uživatel(ka) hodlá tolerovat
	ptydepeodeber = ptydepeodeber.read().splitlines()
	ptydepe = [x for x in ptydepe if x not in ptydepeodeber]

# Konverze formátu

html = markdown(obsah) # převede markdown na html
plaintext = re.sub("<(/)?br(/)?>", "\n", html) # odstraní z html tag <br> a nahradí ho zalomením řádky
plaintext = re.sub("<[^>]*>", "", plaintext) # odstraní z html ostatní tagy
plaintextoneline = re.sub ("\n", " ", plaintext) # verze na jedné řádce, bude se hodit pro hledání kontextovek
titulek = plaintext.partition('\n')[0] # vybere první řádek jako titulek (pro výpis statistik)

# Počet slov a nejdelší slovo

slova = re.sub("(https?:\/\/\S*|www.\\S*)", "", plaintext) # odstraní všechny url adresy
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

# Rozdělení do vět

sentences = re.sub("[„“]", "", plaintext) # odstraní uvozovky
sentences = re.sub("\s+\n", "\n", sentences) # odstraní mezery z konců odstavců
sentences = re.sub("(\w)\n", "\\1.\n", sentences) # doplní tečku za neohraničené odstavce (např. mezititulky)
sentences = nltk.sent_tokenize(sentences) # tokenizuje předchystaný obsah na věty

# Nejdelší věta

nejdelsiveta = max(sentences, key=len) # najde nejdelší větu
nejdelsivetaznaky = len(nejdelsiveta) # počet znaků v nejdelší větě
nejdelsivetaslova = len(nejdelsiveta.split()) # počet slov v nejdelší větě

# Souvětí s nejvíce vztažnými zájmeny

vztaznazajmena = {} # vytvoří prázdný slovník
for x in sentences:
	pocetzajmen = x.count(" kter") + x.count(", jenž ") + x.count(", jež ") + x.count(", jehož") + x.count (", jemuž") + x.count(", jejímž") + x.count(", jejž") + x.count(", co ")
	vztaznazajmena[x] = pocetzajmen # přidá do slovníku větu a hodnotu
nejviczajmen = max(vztaznazajmena, key=vztaznazajmena.get) # vybere ze slovníku větu s nejvyšší hodnotou
pocetzajmen = max(vztaznazajmena.values()) # uloží do proměnné počet nalezených vztažných zájmen v rekordní větě

# Souvětí s nejvíce interpunkčními znaménky

carkyvevetach = {}
for x in sentences:
	carky = x.count(", ") + x.count("; ") + x.count(" – ") + x.count(" - ") + x.count(": ") + x.count("(") + x.count(")")
	carkyvevetach[x] = carky # přidá do slovníku větu a hodnotu
nejviccarek = max(carkyvevetach, key=carkyvevetach.get) # vybere ze slovníku větu s nejvyšší hodnotou
pocetcarek = max(carkyvevetach.values()) # uloží do proměnné počet který v nejdelší větě

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

# Not ok boomer

nalezeneboomerstiny = []
for key, value in notokboomer.items():
	nalezenaboomerstina = re.findall(key, plaintext, re.IGNORECASE)
	if nalezenaboomerstina:
		nalezeneboomerstiny.append(value)

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

print ("*** KIKI v 0.3 POMÁHÁ S EDITOVÁNÍM {-_-} ***\n")
print (titulek, "\n- titulek:", len(titulek), "znaků s mezerami\n- dokument:", pocetznaku, "znaků s mezerami,", pocetslov, "slov,", ns, "NS,", minutycteni, "min čtení")
print ("\nNejdelší slovo:\n- " + str(nejdelsislovo) + " (" + str(nejdelsislovodelka) + " znaků)")
print ("\nNejdelší věta:\n- " + str(nejdelsiveta) + " ("+ str(nejdelsivetaslova) + " slov, " + str(nejdelsivetaznaky) + " znaků)")
if pocetcarek > 3:
	print ("\nVěta s nejvíce interpunkčními znaménky:\n- " + str(nejviccarek) + " (" + str(pocetcarek) + "×)")
if pocetzajmen > 1:
	print ("\nVěta s nejvíce vztažnými zájmeny:\n- " + str(nejviczajmen) + " (" + str(pocetzajmen) + "×)")
if len(slovapouvozovkach) != 0:
	print ("\nPořadí slov po citacích:")
	print ("-", ", ".join(slovapouvozovkach))
if len(nalezeneptydepe) != 0:
	print ("\nZlá, ošklivá slůvka:")
	print ("-", ", ".join(nalezeneptydepe))
if len(nalezeneboomerstiny) != 0:
	print ("\nNot OK boomer:")
	for x in nalezeneboomerstiny:
		print ("-", x)
if len(nalezenekontextovky) != 0:
	print ("\nPohlídat význam:           ▼")
	for x in nalezenekontextovky:
		print ("-", x)
if len(opakovani) != 0:
	print ("\nZduplikovaná slova:")
	print ("-", ", ".join(opakovani))
if len(nalezenetypochyby) != 0:
	print ("\nTypografické chyby:")
	for x in nalezenetypochyby:
		print ("-", x)
	print ("Správná znaménka ke zkopírování: … „ “ ‚ ‘ ×")
if len(uvozovky) != 0:
	print ("\nTermity v uvozovkách:")
	print ("-", ", ".join(uvozovky))