#!/usr/bin/env python
"""
Skript upozorňuje na stylistické nedostatky (českých) textů.

__version__ = "0.2.1"
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

file = open(sys.argv[1], encoding="utf8") # otevře soubor volaný argumentem z příkazové řádky
content = file.read() # načte obsah souboru

# Načtení slovníků

ptydepe = open(os.path.join("slovniky", "ptydepe.txt"), "r", encoding="utf8") # otevře soubor se seznamem zakázaných výrazů
ptydepe = ptydepe.read().splitlines() # načte obsah souboru po řádcích jako seznam, bez přidávání \n na konec každé položky
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

print ("*** KIKI v 0.2.1 POMÁHÁ S EDITOVÁNÍM {-_-} ***\n")
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