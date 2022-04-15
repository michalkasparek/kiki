#!/usr/bin/env python
"""
Nástroj pro editor(k)y (českých) textů

__version__ = "0.4.1"
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

with open(os.path.join("slovniky", "ptydepe.txt"), "r", encoding="utf8") as ptydepe:
	ptydepe = ptydepe.read().splitlines()
with open(os.path.join("slovniky", "notokboomer.txt"), "r", encoding="utf8") as notokboomer_vstup:
	notokboomer_vstup = notokboomer_vstup.read().splitlines()
	notokboomer = {} # vytvoří prázdný slovník pro zastaralé obraty
	for line in notokboomer_vstup:
		key = line.split(";")[0] # načte z každé řádky obsah před středníkem (regex s různými tvary spojení)
		value = line.split(";")[1] # a obsah za středníkem (vysvětlení, proč je spojení blbě)
		notokboomer[key] = value # přidá je do slovníku jako klíč a hodnotu
with open(os.path.join("slovniky", "typochyby.txt"), "r", encoding="utf8") as typochyby:
	typochyby = typochyby.read().splitlines()
with open(os.path.join("slovniky", "kontextovky.txt"), "r", encoding="utf8") as kontextovky:
	kontextovky = kontextovky.read().splitlines()

# Načtení uživatelských slovníků

if os.path.exists(os.path.join("slovniky", "ptydepe_pridej.txt")):
	with open(os.path.join("slovniky", "ptydepe_pridej.txt"), "r", encoding="utf8") as ptydepepridej:
		ptydepepridej = ptydepepridej.read().splitlines()
		ptydepe = ptydepe + ptydepepridej

if os.path.exists(os.path.join("slovniky", "ptydepe_odeber.txt")):
	with open(os.path.join("slovniky", "ptydepe_odeber.txt"), "r", encoding="utf8") as ptydepeodeber:
		ptydepeodeber = ptydepeodeber.read().splitlines()
		ptydepe = [x for x in ptydepe if x not in ptydepeodeber]

# Načtení souboru s textem

if len(sys.argv) == 1:

	okno(ptydepe, typochyby, kontextovky, **notokboomer)

else:

	try:
		with open(sys.argv[1], mode="r", encoding="utf-8") as dokument:
			obsah = dokument.read() 
	except UnicodeDecodeError: 
		with open(sys.argv[1], mode="r") as dokument: # pro txt uložené v libre docs s jiným kódováním
			obsah = dokument.read()
	except FileNotFoundError:
		print ("Kiki nenašla soubor.")
		quit()

	mujclanek = Kiki(obsah, ptydepe, typochyby, kontextovky, **notokboomer)

	print("Kiki pomáhá editovat * github.com/michalkasparek/kiki\n")
	print(mujclanek.kompletni_vypis)