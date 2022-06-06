from os import name
from tkinter import *
from tkinter import ttk
from tool import run

# new tk window
root = Tk()
root.title("parcoursup tool")
frm = ttk.Frame(root, padding=10)
frm.grid()

# number
ttk.Label(frm, text="numéro parcoursup: ").grid(column=0, row=0)
(nb := ttk.Entry(frm)).grid(column=1, row=0)

# password
ttk.Label(frm, text="mot de passe: ").grid(column=0, row=1)
(pss := ttk.Entry(frm, show="*")).grid(column=1, row=1)

# password
ttk.Label(frm, text="nom du fichier: ").grid(column=0, row=2)
tx = ttk.Entry(frm)
tx.insert(0, "data2.csv")
tx.grid(column=1, row=2)

# buttons
ttk.Button(frm, text="Go !", command=lambda: run(nb.get(), pss.get(), tx.get())).grid(column=0, row=3)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=3)
root.mainloop()

