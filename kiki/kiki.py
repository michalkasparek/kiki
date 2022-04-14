#!/usr/bin/env python
"""
Nástroj pro editor(k)y (českých) textů

__version__ = "0.4"
__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

import sys
import os
from kikiengine import Kiki
from kikiokno import okno

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

# Načtení uživatelských slovníků

if os.path.exists(os.path.join("slovniky", "ptydepe_pridej.txt")):
	ptydepepridej = open(os.path.join("slovniky", "ptydepe_pridej.txt"), "r", encoding="utf8")
	ptydepepridej = ptydepepridej.read().splitlines()
	ptydepe = ptydepe + ptydepepridej

if os.path.exists(os.path.join("slovniky", "ptydepe_odeber.txt")):
	ptydepeodeber = open(os.path.join("slovniky", "ptydepe_odeber.txt"), "r", encoding="utf8")
	ptydepeodeber = ptydepeodeber.read().splitlines()
	ptydepe = [x for x in ptydepe if x not in ptydepeodeber]

# Načtení souboru s textem

if len(sys.argv) == 1:

	okno(ptydepe, typochyby, kontextovky, **notokboomer)

else:

	try:
		dokument = open(sys.argv[1], mode="r", encoding="utf-8")
		obsah = dokument.read() 
	except UnicodeDecodeError: 
		dokument = open(sys.argv[1], mode="r") # pro txt uložené v libre docs s jiným kódováním
		obsah = dokument.read()
	except FileNotFoundError:
		print ("Soubor nenalezen.")
		quit()

	mujclanek = Kiki(obsah, ptydepe, typochyby, kontextovky, **notokboomer)

	print("Kiki * https://github.com/michalkasparek/kiki\n")
	print(mujclanek.kompletni_vypis)