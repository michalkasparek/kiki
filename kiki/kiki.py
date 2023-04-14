#!/usr/bin/env python

"""
Funkce a třídy pro běh Kiki:

- kikiokno() = okno s programem
- rozsekej_po_vetach() = rozdělovač vět 
- Kiki() = třída s metodami pro analýzu textu
- kikistart() = načte soubor (když dostane cestu), nebo otevře okno (když ne)
"""

import sys
import os
import re
from markdown import markdown
import tkinter as tk


def kikiokno():
    vzkaz_nahore = "Sem přijde text článku"
    vzkaz_dole = "Michal Kašpárek 2022-3\n\nAktualizace, návod, licence: https://github.com/michalkasparek/kiki\n\nKontakt: michal.kasparek@gmail.com"

    window = tk.Tk()
    window.title("Kiki pomáhá editovat")
    window.geometry("720x640")

    def do_prace(*args):
        frame3.delete(1.0, tk.END)
        clanek = frame1.get(1.0, tk.END)
        mujclanek = Kiki(clanek)
        frame3.insert(tk.END, mujclanek.kompletni_vypis)

    def vymaz(*args):
        if len(frame1.get(1.0, tk.END)) < 50:
            frame1.delete(1.0, tk.END)

    nahore = tk.Frame(master=window, height=150, width=720)
    nahore.pack(fill="both")
    nahore.pack_propagate(0)

    scroll1 = tk.Scrollbar(nahore)
    scroll1.pack(side="right", fill="y")

    frame1 = tk.Text(
        master=nahore, wrap="word", padx=10, pady=10, yscrollcommand=scroll1.set
    )
    frame1.pack(side="left", fill="x", expand=True)
    frame1.insert(tk.END, vzkaz_nahore)

    frame2 = tk.Button(
        master=window, text="Kiki, koukni na to", border=3, command=do_prace, pady=3
    )
    frame2.pack(fill="both", expand=False)

    dole = tk.Frame(master=window, height=300, width=720)
    dole.pack(fill="both", expand=True)

    scroll2 = tk.Scrollbar(dole)
    scroll2.pack(side="right", fill="y")

    frame3 = tk.Text(
        master=dole, wrap="word", padx=10, pady=10, yscrollcommand=scroll2.set
    )
    frame3.pack(side="left", fill="both", expand=True)
    frame3.insert(tk.END, vzkaz_dole)

    scroll1.config(command=frame1.yview)
    scroll2.config(command=frame3.yview)

    window.bind("<Control-k>", do_prace)
    frame1.bind("<Button-1>", vymaz)

    window.mainloop()


def rozsekej_po_vetach(k_rozsekani):
    neni_konec_vety = "(?<!(.Ing\.|[MJ]UDr\.|MVDr\.|.MgA\.|RNDr\.|PhDr\.|rmDr\.|prof\.|.Mgr\.|..Bc\.|..Dr.|.tzv\.|..tj\.|zejm\.|\szvl\.))"

    vety = re.sub("[„“]", "", k_rozsekani)
    vety = re.sub("\s+\n", "\n", vety)
    vety = re.sub(
        "(\w)\n", "\\1.\n", vety
    )  # doplní tečku na konec řádků končíčích písmenem/číslem
    vety = re.sub(
        "\s\s+", " ", vety
    )  # odstranění dvojtých mezer, mezer na koncích řádků atd.
    vety = re.sub(
        "(?<=[\.\!\?…])" + neni_konec_vety + "\s(?=([A-Z]|[ÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\(]))",
        "\n",
        vety,
    )
    vety = re.sub(
        "(?<=[\.\!\?…]\))" + neni_konec_vety + "\s(?=([A-Z]|[ÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ\(]))",
        "\n",
        vety,
    )
    vety = re.sub("(?<=[\.\!\?…])" + neni_konec_vety + "\s[–-•]\s", "\n", vety)
    vety = re.sub(
        "(?<=[a-ž][\.\!\?…])\s(?=\d+)", "\n", vety
    )  # "odřenýma ušima. 28. listopadu jsem"
    vety = vety.splitlines()

    return vety


class Kiki:
    def __init__(self, surovy_vstup):
        os.chdir(os.path.dirname(__file__))

        ## Načtení slovníků

        with open(
            os.path.join("slovniky", "ptydepe.txt"), "r", encoding="utf-8"
        ) as ptydepe:
            ptydepe = ptydepe.read().splitlines()
        with open(
            os.path.join("slovniky", "notokboomer.txt"), "r", encoding="utf-8"
        ) as notokboomer_vstup:
            notokboomer_vstup = notokboomer_vstup.read().splitlines()
            notokboomer = {}
            for line in notokboomer_vstup:
                key = line.split(";")[
                    0
                ]  # načte z každé řádky obsah před středníkem (regex s různými tvary spojení)
                value = line.split(";")[
                    1
                ]  # a obsah za středníkem (vysvětlení, proč je spojení blbě)
                notokboomer[key] = value
        with open(
            os.path.join("slovniky", "typochyby.txt"), "r", encoding="utf-8"
        ) as typochyby:
            typochyby = typochyby.read().splitlines()
        with open(
            os.path.join("slovniky", "kontextovky.txt"), "r", encoding="utf-8"
        ) as kontextovky:
            kontextovky = kontextovky.read().splitlines()
        with open(
            os.path.join("slovniky", "dublety.txt"), "r", encoding="utf-8"
        ) as dublety_vstup:
            dublety_vstup = dublety_vstup.read().splitlines()
            dublety = []
            for line in dublety_vstup:
                dublety.append([line.split(";")[0], line.split(";")[1]])

        # Načtení uživatelských slovníků

        if os.path.exists(os.path.join("slovniky", "ptydepe_pridej.txt")):
            with open(
                os.path.join("slovniky", "ptydepe_pridej.txt"), "r", encoding="utf-8"
            ) as ptydepepridej:
                ptydepepridej = ptydepepridej.read().splitlines()
                ptydepe = ptydepe + ptydepepridej

        if os.path.exists(os.path.join("slovniky", "ptydepe_odeber.txt")):
            with open(
                os.path.join("slovniky", "ptydepe_odeber.txt"), "r", encoding="utf-8"
            ) as ptydepeodeber:
                ptydepeodeber = ptydepeodeber.read().splitlines()
                ptydepe = [x for x in ptydepe if x not in ptydepeodeber]

        interpunkce = "(,\s|;\s|\s–\s|\s\-\s|:\s|\(|\))"
        zajmena = "(\skter|\sjenž\s|\sjež\s|\sjehož\s|\sjemuž\s|\sjejímž\s|\sjejž\s|\sco\s|\scož\s)"

        self.html_vstup = markdown(surovy_vstup)
        self.plaintext = re.sub(
            "<(/)?br(/)?>", "\n", self.html_vstup
        )  # nahradí tag <br> zalomením
        self.plaintext = re.sub(
            "<[^>]*>", "", self.plaintext
        )  # odstraní z html zbylé tagy
        self.plaintext_1radek = re.sub("\n", " ", self.plaintext)

        self.titulek = self.plaintext.partition("\n")[0]

        self.slova = re.sub(
            "(https?:\/\/\S*|www.\\S*)", "", self.plaintext_1radek
        )  # odstraní urls
        self.slova = re.sub(
            "[,\.:;!?\(\)„“…'\"']", "", self.slova
        )  # vymaže interpunkci
        self.slova = re.sub(
            "(-|–|—)", " ", self.slova
        )  # dlouhá-sousloví se nebudou počítat
        self.slova = self.slova.split()
        self.nejdelsi_slovo = max(self.slova, key=len)
        self.nejdelsi_slovo_delka = len(self.nejdelsi_slovo)

        self.pocet_slov = len(self.slova)
        self.pocet_znaku = len(self.plaintext)
        self.pocet_normostran = self.pocet_znaku / 1800
        self.ns = "{:.1f}".format(self.pocet_normostran).replace(".", ",")
        self.minuty_cteni = round(
            self.pocet_slov / 200
        )  # 200 slov za minutu (zdroj: internet)

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

        self.citace = re.split(
            "[,\?\!]“[^\n]", self.plaintext
        )  # rozdělí dokument na konci citací
        del self.citace[0]
        self.slova_po_uvozovkach = [x.split()[0] for x in self.citace]
        self.slova_po_uvozovkach = [
            re.sub("[\.,\?:;]", "", x) for x in self.slova_po_uvozovkach
        ]  # odstraní bordýlek

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
                self.boomerstiny_nalezene.append(
                    str(", ".join(boomerstina_vyskyt)) + ": " + value
                )

        # Dublety

        self.dublety_nalezene = []
        for x in dublety:
            dub1 = re.search(x[0], self.plaintext, re.IGNORECASE)
            dub2 = re.search(x[1], self.plaintext, re.IGNORECASE)
            if dub1 and dub2:
                self.dublety_nalezene.append(dub1.group() + "/" + dub2.group())

        # Jedno slovo dvakrát po sobě

        self.opakovani = re.findall("\\b(\\w+)\\s\\1\\b", self.plaintext, re.IGNORECASE)
        self.opakovani = [
            re.sub("(\\w+)", "\\1 \\1", x) for x in self.opakovani
        ]  # zduplikuje duplikáty

        # Pojmy v uvozovkách

        self.uvozovky = re.findall(
            "„\\w+\\s*\\w*\\s*\\w*“", self.plaintext, re.IGNORECASE
        )

        # Typografické chyby

        self.typochyby_nalezene = []
        for typochyby in typochyby:
            typochyba_nalezena = re.findall(typochyby, self.plaintext, re.IGNORECASE)
            if typochyba_nalezena:
                self.typochyby_nalezene.append(typochyba_nalezena)

        # Slova, u kterých je nutné pohlídat kontext

        self.kontextovky_nalezene = []
        for kontextovky in kontextovky:
            kontextovka_vyskyt = re.findall(
                kontextovky, self.plaintext_1radek, re.IGNORECASE
            )
            if kontextovka_vyskyt:
                self.kontextovky_nalezene.append(kontextovka_vyskyt)

        # Nejdelší podkapitoly

        self.podkapitoly = re.split("(\*\*\*|## )", surovy_vstup)
        while "***" in self.podkapitoly:
            self.podkapitoly.remove("***")
        while "## " in self.podkapitoly:
            self.podkapitoly.remove("## ")
        self.podkapitoly_prumer = len(surovy_vstup) / len(self.podkapitoly)
        self.nejdelsi_podkapitola = max(self.podkapitoly, key=len)
        self.nejdelsi_podkapitola_kolikrat = (
            len(self.nejdelsi_podkapitola) / self.podkapitoly_prumer
        )
        self.nejdelsi_podkapitola_kolikrat = "{:.2f}".format(
            self.nejdelsi_podkapitola_kolikrat
        ).replace(".", ",")
        self.nejdelsi_podkapitola = re.sub("\n", " ", self.nejdelsi_podkapitola)
        self.nejdelsi_podkapitola = self.nejdelsi_podkapitola.strip()[0:48]
        self.nejdelsi_podkapitola_komplet = f"{self.nejdelsi_podkapitola}… ({self.nejdelsi_podkapitola_kolikrat}× delší než průměr)"

        if len(self.podkapitoly) < 3:
            self.nejdelsi_podkapitola_komplet = ""

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

        self.kompletni_vypis = f"""*** STRUKTURA ***{nr}
{self.titulek}
- titulek: {len(self.titulek)} znaků s mezerami
- dokument: {self.pocet_znaku} znaků s mezerami, {self.pocet_slov} slov, {self.ns} NS, {self.minuty_cteni} min čtení
{nr}Nejdelší slovo:{nr}- {self.nejdelsi_slovo} ({self.nejdelsi_slovo_delka} znaků)
{nr}Nejdelší věta:{nr}- {self.nejdelsi_veta} ({self.nejdelsi_veta_slova} slov, {self.nejdelsi_veta_znaky} znaků)
{nr}Věta s nejvíce interpunkčními znaménky:{nr}- {self.nejviccarek} ({self.pocetcarek}×)
{nr}Věta s nejvíce vztažnými zájmeny:{nr}- {self.nejvic_zajmen} ({self.pocet_zajmen}×)
{nr}Nejdelší podkapitola:{nr}- {self.nejdelsi_podkapitola_komplet}
{nr}*** SLOH ***
{nr}Zlá, ošklivá slůvka:{nr}- {", ".join(self.ptydepe_pekne)} 
{nr}Not OK boomer:{nr}- {nr_odr.join(self.boomerstiny_nalezene)} 
{nr}Pořadí slov po citacích:{nr}- {", ".join(self.slova_po_uvozovkach)}
{nr}Zduplikovaná slova slova:{nr}- {", ".join(self.opakovani)}
{nr}Nejednotná forma:{nr}- {", ".join(self.dublety_nalezene)}
{nr}Termity v uvozovkách:{nr}- {", ".join(self.uvozovky)} 
{nr}Typografické chyby:{nr}- {", ".join(self.typochyby_nalezene)} 
Správná znaménka ke zkopírování: … „ “ ‚ ‘ ×
{nr}Pohlídat kontext:          ▼{nr}- {nr_odr.join(self.kontextovky_nalezene)}
"""


# A do práce!


def kikistart():
    if len(sys.argv) == 1:  # spuštění bez argumentu = Kiki v okně
        kikiokno()

    else:  # spuštění s argumentem = Kiki v terminálu
        try:
            with open(sys.argv[1], mode="r", encoding="utf-8") as dokument:
                obsah = dokument.read()
        except UnicodeDecodeError:
            with open(
                sys.argv[1], mode="r"
            ) as dokument:  # pro txt uložené v libre docs s jiným kódováním
                obsah = dokument.read()
        except FileNotFoundError:
            print("Kiki nenašla soubor.")

        mujclanek = Kiki(obsah)

        print("Kiki pomáhá editovat * github.com/michalkasparek/kiki\n")
        print(mujclanek.kompletni_vypis)
