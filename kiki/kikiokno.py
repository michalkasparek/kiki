#!/usr/bin/env python

"""
Skript s GUI editorské pomocnice Kiki

__author__ = "Michal Kašpárek"
__email__ = "michal.kasparek@gmail.com"
__license__ = "MIT"
__status__ = "Development"
"""

import tkinter as tk
from kikiengine import Kiki

def okno(ptydepe, typochyby, kontextovky, **notokboomer):

    vzkaz_nahore = "Sem přijde text článku"
    vzkaz_dole = "Kiki\n\nhttps://github.com/michalkasparek/kiki"

    window = tk.Tk()
    window.title("Kiki pomáhá editovat")
    window.geometry("720x640")

    def do_prace(*args):
        frame3.delete(1.0, tk.END)
        clanek = frame1.get(1.0, tk.END)
        mujclanek = Kiki(clanek, ptydepe, typochyby, kontextovky, **notokboomer)
        frame3.insert(tk.END, mujclanek.kompletni_vypis)

    def vymaz(*args):
        if len(frame1.get(1.0, tk.END)) < 50:
            frame1.delete(1.0, tk.END)
        
    nahore = tk.Frame(master=window, height = 150, width = 720)
    nahore.pack(fill="both")
    nahore.pack_propagate(0)

    scroll1 = tk.Scrollbar(nahore)
    scroll1.pack(side= "right", fill="y")

    frame1 = tk.Text(master=nahore, wrap="word", padx=10, pady=10, yscrollcommand=scroll1.set)
    frame1.pack(side = "left", fill = "x", expand = True)
    frame1.insert(tk.END, vzkaz_nahore)

    frame2 = tk.Button(master=window, text="Kiki, koukni na to", border=3, command=do_prace, pady = 3)
    frame2.pack(fill = "both", expand = False)

    dole = tk.Frame(master=window, height = 300, width = 720)
    dole.pack(fill="both", expand = True)

    scroll2 = tk.Scrollbar(dole)
    scroll2.pack(side= "right", fill="y")

    frame3 = tk.Text(master=dole, wrap="word", padx=10, pady=10, yscrollcommand=scroll2.set)
    frame3.pack(side = "left", fill = "both", expand = True)
    frame3.insert(tk.END, vzkaz_dole)

    scroll1.config(command=frame1.yview)
    scroll2.config(command=frame3.yview)

    window.bind("<Control-k>", do_prace)
    frame1.bind("<Button-1>", vymaz)

    window.mainloop()