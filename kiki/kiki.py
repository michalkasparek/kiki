#!/usr/bin/env python
"""
Nástroj pro editor(k)y (českých) textů

__version__ = "0.6"
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

with open(os.path.join("slovniky", "ptydepe.txt"), "r", encoding="utf-8") as ptydepe:
	ptydepe = ptydepe.read().splitlines()
with open(os.path.join("slovniky", "notokboomer.txt"), "r", encoding="utf-8") as notokboomer_vstup:
	notokboomer_vstup = notokboomer_vstup.read().splitlines()
	notokboomer = {}
	for line in notokboomer_vstup:
		key = line.split(";")[0] # načte z každé řádky obsah před středníkem (regex s různými tvary spojení)
		value = line.split(";")[1] # a obsah za středníkem (vysvětlení, proč je spojení blbě)
		notokboomer[key] = value
with open(os.path.join("slovniky", "typochyby.txt"), "r", encoding="utf-8") as typochyby:
	typochyby = typochyby.read().splitlines()
with open(os.path.join("slovniky", "kontextovky.txt"), "r", encoding="utf-8") as kontextovky:
	kontextovky = kontextovky.read().splitlines()
with open(os.path.join("slovniky", "dublety.txt"), "r", encoding="utf-8") as dublety_vstup:
	dublety_vstup = dublety_vstup.read().splitlines()
	dublety = []
	for line in dublety_vstup:
		dublety.append([line.split(";")[0], line.split(";")[1]])

# Načtení uživatelských slovníků

if os.path.exists(os.path.join("slovniky", "ptydepe_pridej.txt")):
	with open(os.path.join("slovniky", "ptydepe_pridej.txt"), "r", encoding="utf-8") as ptydepepridej:
		ptydepepridej = ptydepepridej.read().splitlines()
		ptydepe = ptydepe + ptydepepridej

if os.path.exists(os.path.join("slovniky", "ptydepe_odeber.txt")):
	with open(os.path.join("slovniky", "ptydepe_odeber.txt"), "r", encoding="utf-8") as ptydepeodeber:
		ptydepeodeber = ptydepeodeber.read().splitlines()
		ptydepe = [x for x in ptydepe if x not in ptydepeodeber]

# A do práce!

if len(sys.argv) == 1: # spuštění bez argumentu = Kiki v okně

	okno(ptydepe, typochyby, kontextovky, dublety, **notokboomer)

else: # spuštění s argumentem = Kiki v terminálu

	try:
		with open(sys.argv[1], mode="r", encoding="utf-8") as dokument:
			obsah = dokument.read() 
	except UnicodeDecodeError: 
		with open(sys.argv[1], mode="r") as dokument: # pro txt uložené v libre docs s jiným kódováním
			obsah = dokument.read()
	except FileNotFoundError:
		print ("Kiki nenašla soubor.")
		quit()

	mujclanek = Kiki(obsah, ptydepe, typochyby, kontextovky, dublety, **notokboomer)

	print("Kiki pomáhá editovat * github.com/michalkasparek/kiki\n")
	print(mujclanek.kompletni_vypis)