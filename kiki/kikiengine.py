#!/usr/bin/env python

"""
Skript obsahuje:
1/ Funkci rozsekej_po_vetach pro rozdělení (českého) textu do vět. Bere do úvahy akademické tituly a některé další chytáky. Je optimalizovaná pro nalezení nejdelší, nikoliv nejkratší věty v textu a práci si ulehčuje drobnými, ale efektivními podfuky, např. odstraněním uvozovek. Nelze ji proto využít tam, kde je nutná maximální přesnost a věrnost.
2/ Třídu Kiki s metodami pro stylistickou analýzu (českých) textů.

__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

from markdown import markdown
import re

def rozsekej_po_vetach(k_rozsekani):

    neni_konec_vety = "(?<!(.Ing\.|[MJ]UDr\.|MVDr\.|.MgA\.|RNDr\.|PhDr\.|rmDr\.|prof\.|.Mgr\.|..Bc\.|..Dr.|.tzv\.|..tj\.|zejm\.|\szvl\.))"

    vety = re.sub("[„“]", "", k_rozsekani)
    vety = re.sub("\s+\n", "\n", vety)
    vety = re.sub("(\w)\n", "\\1.\n", vety) # doplní tečku na konec řádků končíčích písmenem/číslem
    vety = re.sub("\s\s+", " ", vety) # odstranění dvojtých mezer, mezer na koncích řádků atd.
    vety = re.sub("(?<=[\.\!\?…])"+neni_konec_vety+"\s(?=([A-Z]|[ÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\(]))", "\n", vety)
    vety = re.sub("(?<=[\.\!\?…])"+neni_konec_vety+"\s[–-•]\s", "\n", vety)
    vety = re.sub("(?<=[a-ž][\.\!\?…])\s(?=\d+)", "\n", vety) # "odřenýma ušima. 28. listopadu jsem"
    vety = vety.splitlines()

    return vety

class Kiki:

    def __init__(self, surovy_vstup, ptydepe, typochyby, kontextovky, **notokboomer):

        interpunkce = "(,\s|;\s|\s–\s|\s\-\s|:\s|\(|\))"
        zajmena = "(\skter|\sjenž\s|\sjež\s|\sjehož\s|\sjemuž\s|\sjejímž\s|\sjejž\s|\sco\s|\scož\s)"

        self.html_vstup = markdown(surovy_vstup)
        self.plaintext = re.sub("<(/)?br(/)?>", "\n", self.html_vstup) # nahradí tag <br> zalomením řádky
        self.plaintext = re.sub("<[^>]*>", "", self.plaintext) # odstraní z html zbylé tagy
        
        self.titulek = self.plaintext.partition('\n')[0]
        
        self.slova = re.sub("(https?:\/\/\S*|www.\\S*)", "", self.plaintext) # odstraní všechny url adresy
        self.slova = re.sub("[,\.:;!?„“…'\"\']", "", self.slova) # vymaže interpunkci
        self.slova = re.sub("(-|–|—)", " ", self.slova) # dlouhá-sousloví se nebudou počítat jako jedno slovo
        self.slova = self.slova.split()
        self.nejdelsi_slovo = max(self.slova, key=len)
        self.nejdelsi_slovo_delka = len(self.nejdelsi_slovo)

        self.pocet_slov = len(self.slova)
        self.pocet_znaku = len(self.plaintext)
        self.pocet_normostran = round(self.pocet_znaku / 1800, 1)
        self.ns = str(self.pocet_normostran) # převede počet normostran na string
        self.ns = self.ns.replace(".", ",") # vymění anglickou desetinnou tečku za českou desetinnou čárku
        self.minuty_cteni = round(self.pocet_slov/200) # průměrný čtenář přečte za minutu 200 slov (zdroj: internet)
        
        self.vety = rozsekej_po_vetach(self.plaintext)

        self.nejdelsi_veta = max(self.vety, key=len)
        self.nejdelsi_veta_znaky = len(self.nejdelsi_veta)
        self.nejdelsi_veta_slova = len(self.nejdelsi_veta.split())

        self.vztazna_zajmena = {} 
        for x in self.vety:
            pocet_zajmen = len(re.findall(zajmena, x, re.IGNORECASE))
            self.vztazna_zajmena[x] = pocet_zajmen # přidá do slovníku větu a hodnotu
        self.nejvic_zajmen = max(self.vztazna_zajmena, key=self.vztazna_zajmena.get) # vybere ze slovníku větu s nejvyšší hodnotou
        self.pocet_zajmen = max(self.vztazna_zajmena.values()) # uloží do proměnné počet nalezených vztažných zájmen v rekordní větě

        # Souvětí s nejvíce interpunkčními znaménky

        self.carkyvevetach = {}
        for x in self.vety:
            carky = len(re.findall(interpunkce, x))
            self.carkyvevetach[x] = carky 
            self.nejviccarek = max(self.carkyvevetach, key=self.carkyvevetach.get)
            self.pocetcarek = max(self.carkyvevetach.values())

        # Slova za uvozovkami

        self.citace = re.split("[,\?\!]“[^\n]", self.plaintext) # rozdělí dokument v místech, kde jdou po sobě čárka, otazník nebo vykřičník a uvozovky, a za nimi nenásleduje konec řádku
        del self.citace[0]
        self.slova_po_uvozovkach = [x.split()[0] for x in self.citace]
        self.slova_po_uvozovkach = [re.sub("[\.,\?:;]", "", x) for x in self.slova_po_uvozovkach] # odstraní bordýlek

        # Ošklivé fráze

        self.ptydepe_nalezene = []
        for ptydepe in ptydepe:
            ptydepe_vyskyt = re.findall(ptydepe, self.plaintext, re.IGNORECASE)
            self.ptydepe_nalezene.append(ptydepe_vyskyt)

        # Not ok boomer

        self.boomerstiny_nalezene = []
        for key, value in notokboomer.items():
            boomerstina_vyskyt = re.findall(key, self.plaintext, re.IGNORECASE)
            if boomerstina_vyskyt:
                self.boomerstiny_nalezene.append(value)

        # Jedno slovo dvakrát po sobě

        self.opakovani = re.findall("\\b(\\w+)\\s\\1\\b", self.plaintext, re.IGNORECASE)
        self.opakovani = [re.sub("(\\w+)", "\\1 \\1", x) for x in self.opakovani] # zduplikuje duplikáty (asi by to mělo jít i lepším regexem v předchozím řádku)

        # Pojmy v uvozovkách

        self.uvozovky = re.findall("„\\w+\\s*\\w*\\s*\\w*“", self.plaintext, re.IGNORECASE) # 1 až 3 slova mezi uvozovkami

        # Typografické chyby

        self.typochyby_nalezene = []
        for typochyby in typochyby:
            typochyba_nalezena = re.findall(typochyby, self.plaintext, re.IGNORECASE)
            self.typochyby_nalezene.append(typochyba_nalezena)

        # Slova, u kterých je nutné pohlídat kontext

        self.plaintext_1radek = re.sub("\n", " ", self.plaintext)
        self.kontextovky_nalezene = []
        for kontextovky in kontextovky:
            kontextovka_vyskyt = re.findall(kontextovky, self.plaintext_1radek, re.IGNORECASE)
            self.kontextovky_nalezene.append(kontextovka_vyskyt)
				
        # Úprava seznamů pro pěkný výstup

        self.ptydepe_nalezene = list(filter(None, self.ptydepe_nalezene)) # vymaže prázdné subsety
        self.ptydepe_nalezene = sum(self.ptydepe_nalezene, []) # spojí subsety do jednoho setu

        self.typochyby_nalezene = list(filter(None, self.typochyby_nalezene)) # vymaže prázdné subsety
        self.typochyby_nalezene = sum(self.typochyby_nalezene, []) # spojí subsety do jednoho setu

        self.kontextovky_nalezene = sum(self.kontextovky_nalezene, []) # vymaže prázdné subsety

        # Výpis

        self.kompletni_vypis = (self.titulek + "\n- titulek: " + str(len(self.titulek)) 
        + " znaků s mezerami\n- dokument: " + str(self.pocet_znaku) + " znaků s mezerami, " 
        + str(self.pocet_slov) + " slov, " + str(self.ns) + " NS, " + str(self.minuty_cteni) 
        + " min čtení" + "\n\nNejdelší slovo:\n- " + str(self.nejdelsi_slovo) + " (" 
        + str(self.nejdelsi_slovo_delka) + " znaků)" + "\n\nNejdelší věta:\n- " 
        + str(self.nejdelsi_veta) + " ("+ str(self.nejdelsi_veta_slova) + " slov, " 
        + str(self.nejdelsi_veta_znaky) + " znaků)" + "\n\nVěta s nejvíce interpunkčními znaménky:\n- " 
        + str(self.nejviccarek) + " (" + str(self.pocetcarek) + "×)\n\nVěta s nejvíce vztažnými zájmeny:\n- " 
        + str(self.nejvic_zajmen) + " (" + str(self.pocet_zajmen) + "×) \n\nPořadí slov po citacích:\n- " 
        + ", ".join(self.slova_po_uvozovkach) + "\n\nZlá, ošklivá slůvka:\n- " + ", ".join(self.ptydepe_nalezene) 
        + "\n\nNot OK boomer:\n- " + "\n- ".join(self.boomerstiny_nalezene) + "\n\nZduplikovaná slova slova:\n- " 
        + ", ".join(self.opakovani) + "\n\nTypografické chyby:\n- " + ", ".join(self.typochyby_nalezene) 
        + "\nSprávná znaménka ke zkopírování: … „ “ ‚ ‘ ×\n\nTermity v uvozovkách:\n- " + ", ".join(self.uvozovky) 
        + "\n\nPohlídat kontext:          ▼\n- " + "\n- ".join(self.kontextovky_nalezene))