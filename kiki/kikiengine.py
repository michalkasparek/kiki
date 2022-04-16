#!/usr/bin/env python

"""
Skript obsahuje:
1/ Funkci rozsekej_po_vetach pro rozdělení (českého) textu do vět. Bere do úvahy akademické tituly 
a některé další chytáky. Je optimalizovaná pro nalezení nejdelší, nikoliv nejkratší věty v textu 
a práci si ulehčuje drobnými, ale efektivními podfuky, např. odstraněním uvozovek. Nelze ji proto 
využít tam, kde je nutná maximální přesnost a věrnost.
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

    def __init__(self, surovy_vstup, ptydepe, typochyby, kontextovky, dublety, **notokboomer):

        interpunkce = "(,\s|;\s|\s–\s|\s\-\s|:\s|\(|\))"
        zajmena = "(\skter|\sjenž\s|\sjež\s|\sjehož\s|\sjemuž\s|\sjejímž\s|\sjejž\s|\sco\s|\scož\s)"

        self.html_vstup = markdown(surovy_vstup)
        self.plaintext = re.sub("<(/)?br(/)?>", "\n", self.html_vstup) # nahradí tag <br> zalomením
        self.plaintext = re.sub("<[^>]*>", "", self.plaintext) # odstraní z html zbylé tagy
        self.plaintext_1radek = re.sub("\n", " ", self.plaintext)

        self.titulek = self.plaintext.partition('\n')[0]
        
        self.slova = re.sub("(https?:\/\/\S*|www.\\S*)", "", self.plaintext_1radek) # odstraní urls
        self.slova = re.sub("[,\.:;!?\(\)„“…'\"\']", "", self.slova) # vymaže interpunkci
        self.slova = re.sub("(-|–|—)", " ", self.slova) # dlouhá-sousloví se nebudou počítat
        self.slova = self.slova.split()
        self.nejdelsi_slovo = max(self.slova, key=len)
        self.nejdelsi_slovo_delka = len(self.nejdelsi_slovo)

        self.pocet_slov = len(self.slova)
        self.pocet_znaku = len(self.plaintext)
        self.pocet_normostran = self.pocet_znaku / 1800
        self.ns = "{:.1f}".format(self.pocet_normostran).replace(".", ",")
        self.minuty_cteni = round(self.pocet_slov/200) # 200 slov za minutu (zdroj: internet)

        self.vety = rozsekej_po_vetach(self.plaintext)

        self.nejdelsi_veta = max(self.vety, key=len)
        self.nejdelsi_veta_znaky = len(self.nejdelsi_veta)
        self.nejdelsi_veta_slova = len(self.nejdelsi_veta.split())

        # Věta s nejvíce vztažnými zájmeny

        self.vztazna_zajmena = {} 
        for x in self.vety:
            pocet_zajmen = len(re.findall(zajmena, x, re.IGNORECASE))
            self.vztazna_zajmena[x] = pocet_zajmen
        self.nejvic_zajmen = max(self.vztazna_zajmena, key=self.vztazna_zajmena.get)
        self.pocet_zajmen = max(self.vztazna_zajmena.values()) 

        # Věta s nejvíce interpunkčními znaménky

        self.carkyvevetach = {}
        for x in self.vety:
            carky = len(re.findall(interpunkce, x))
            self.carkyvevetach[x] = carky 
            self.nejviccarek = max(self.carkyvevetach, key=self.carkyvevetach.get)
            self.pocetcarek = max(self.carkyvevetach.values())

        # Slova za uvozovkami

        self.citace = re.split("[,\?\!]“[^\n]", self.plaintext) # rozdělí dokument na konci citací
        del self.citace[0]
        self.slova_po_uvozovkach = [x.split()[0] for x in self.citace]
        self.slova_po_uvozovkach = [re.sub("[\.,\?:;]", "", x) for x in self.slova_po_uvozovkach] # odstraní bordýlek

        # Ošklivé fráze

        self.ptydepe_nalezene = []
        for ptydepe in ptydepe:
            ptydepe_vyskyt = re.findall(ptydepe, self.plaintext, re.IGNORECASE)
            if ptydepe_vyskyt:
                self.ptydepe_nalezene.append(ptydepe_vyskyt)

        # Not ok boomer

        self.boomerstiny_nalezene = []
        for key, value in notokboomer.items():
            boomerstina_vyskyt = re.findall(key, self.plaintext, re.IGNORECASE)
            if boomerstina_vyskyt:
                self.boomerstiny_nalezene.append(str(", ".join(boomerstina_vyskyt)) + ": " + value)

        # Dublety

        self.dublety_nalezene = []
        for x in dublety:
            dub1 = re.search(x[0], self.plaintext, re.IGNORECASE)
            dub2 = re.search(x[1], self.plaintext, re.IGNORECASE)
            if dub1 and dub2:
                self.dublety_nalezene.append(dub1.group() + "/" + dub2.group())

        # Jedno slovo dvakrát po sobě

        self.opakovani = re.findall("\\b(\\w+)\\s\\1\\b", self.plaintext, re.IGNORECASE)
        self.opakovani = [re.sub("(\\w+)", "\\1 \\1", x) for x in self.opakovani] # zduplikuje duplikáty

        # Pojmy v uvozovkách

        self.uvozovky = re.findall("„\\w+\\s*\\w*\\s*\\w*“", self.plaintext, re.IGNORECASE)

        # Typografické chyby

        self.typochyby_nalezene = []
        for typochyby in typochyby:
            typochyba_nalezena = re.findall(typochyby, self.plaintext, re.IGNORECASE)
            if typochyba_nalezena:
                self.typochyby_nalezene.append(typochyba_nalezena)

        # Slova, u kterých je nutné pohlídat kontext

        self.kontextovky_nalezene = []
        for kontextovky in kontextovky:
            kontextovka_vyskyt = re.findall(kontextovky, self.plaintext_1radek, re.IGNORECASE)
            if kontextovka_vyskyt:
                self.kontextovky_nalezene.append(kontextovka_vyskyt)
				
        # Úprava seznamů pro pěkný výstup

        self.ptydepe_nalezene = sorted(self.ptydepe_nalezene, key=len, reverse=True)
        self.ptydepe_pekne = []
        for x in self.ptydepe_nalezene:
            self.ptydepe_pekne.append(str(x[0]) + " (" + str(len(x)) + "×)")

        self.typochyby_nalezene = sum(self.typochyby_nalezene, [])
        self.kontextovky_nalezene = sum(self.kontextovky_nalezene, [])

        # Výpis

        nr = "\n"
        nr_odr = "\n- "

        self.kompletni_vypis = f"""{self.titulek}
- titulek: {len(self.titulek)} znaků s mezerami
- dokument: {self.pocet_znaku} znaků s mezerami, {self.pocet_slov} slov, {self.ns} NS, {self.minuty_cteni} min čtení
{nr}Nejdelší slovo:{nr}- {self.nejdelsi_slovo} ({self.nejdelsi_slovo_delka} znaků)
{nr}Nejdelší věta:{nr}- {self.nejdelsi_veta} ({self.nejdelsi_veta_slova} slov, {self.nejdelsi_veta_znaky} znaků)
{nr}Věta s nejvíce interpunkčními znaménky:{nr}- {self.nejviccarek} ({self.pocetcarek}×)
{nr}Věta s nejvíce vztažnými zájmeny:{nr}- {self.nejvic_zajmen} ({self.pocet_zajmen}×)
{nr}Pořadí slov po citacích:{nr}- {", ".join(self.slova_po_uvozovkach)} 
{nr}Zlá, ošklivá slůvka:{nr}- {", ".join(self.ptydepe_pekne)} 
{nr}Not OK boomer:{nr}- {nr_odr.join(self.boomerstiny_nalezene)} 
{nr}Nejednotná forma:{nr}- {", ".join(self.dublety_nalezene)}
{nr}Zduplikovaná slova slova:{nr}- {", ".join(self.opakovani)}
{nr}Typografické chyby:{nr}- {", ".join(self.typochyby_nalezene)} 
Správná znaménka ke zkopírování: … „ “ ‚ ‘ ×
{nr}Termity v uvozovkách:{nr}- {", ".join(self.uvozovky)} 
{nr}Pohlídat kontext:          ▼{nr}- {nr_odr.join(self.kontextovky_nalezene)}"""