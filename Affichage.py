from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont

#Importation du fichier et vérification du format (.wav only)
globalpathfilename = str()
def selec_fichier():
    pathfilename =  filedialog.askopenfilename(initialdir = "/",title = "Sélection du fichier audio",filetypes = (("audio files","*.*"),("all files","*.*")))
    longueur = len(pathfilename)
    ext = []
    for loop in range(4):
        ext.append(pathfilename[longueur-(1+loop)])
    ext.reverse()
    Extension = "".join(ext)
    if Extension != ".wav":
        messagebox.showerror("Erreur", "Mauvais Format : Veuillez sélectionner un fichier .wav")
    else:
        Filenamebox.delete(0.0, END)
        Filenamebox.insert(END, pathfilename)
        globalpathfilename = pathfilename
    

def switchMode():
    SM = AnaGen.get()
    if SM == 0:
       Generateur.grid_forget()
       Analyseur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)
    elif SM == 1:
        Analyseur.grid_forget()
        Generateur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)

'_____________________________________________________________________________________________________________________'

#Fonction pour récupérer les différentes entrées de l'interface (pour éviter de fouiller dans le code)

#Amplitude : Amp.get()

#Durée de la note : DNote.get()

#Gamme : GammeEntry.get()

#Nom du fichier : saisieNom.get()

'_____________________________________________________________________________________________________________________'
    
main = Tk()
main.title("oscilloraptorz")
main.configure(background="white")
Label (main, text="Module d'analyse et de génération de sons :", bg="white", fg="black", font="none 15 bold") .grid(row=1, column=1, sticky=NW)
FontSS = tkFont.Font(size=18)

'_____________________________________________________________________________________________________________________'

#fenêtre de droite
CadreMode = LabelFrame(main, bg="white", bd=0, height=50)
CadreMode.grid(row=2, column=1, sticky=NW, pady=7, padx=10)
AnaGen = IntVar()
AnaGen.set(0)
Ana = Radiobutton(CadreMode, text="Analyseur", value=0, variable=AnaGen, indicatoron=0, command=switchMode)
Ana.grid(row=2, column=1, sticky=NW, pady=5, padx=10)
Gen = Radiobutton(CadreMode, text="Générateur", value=1, variable=AnaGen, indicatoron=0, command = switchMode)
Gen.grid(row=2, column=2, sticky=NW, pady=5, padx=10)

'_____________________________________________________________________________________________________________________'

#Fenêtre analyseur
Analyseur = LabelFrame(main, bg="white", bd=2, height=400, text="Analyser un Son", font="FontSS")
Analyseur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)

#Importation du fichier
Filenamebox = Text(Analyseur, width = 35, height=1, wrap=WORD, bg="white", fg="blue")
Filenamebox.grid(row=3, column=1, sticky=NW, pady=10, padx=8)
Button(Analyseur, text="IMPORTER", width=12, command=selec_fichier) .grid(row=4, column=1, sticky=NW, padx=8, pady=2)

#Affichage en Diese ou en bémol
Diese = IntVar() #faudra peut être déclarer toutes ces variables dès le début
Diese.set(1)
Di = Radiobutton(Analyseur, text='Dièse (#)', value=1, variable=Diese, bg ="white")
Di.grid(row=6, column=1, sticky=W, padx=4, pady=11)
Label (Analyseur, text="<-- Affichage -->", bg="white") .grid(row=6, column=1, padx=4, pady=11)
Be = Radiobutton(Analyseur, text='Bémol (b)', value=0, variable=Diese, bg ="white")
Be.grid(row=6, column=1, sticky=E, padx=4, pady=11)

#Affichage des intervalles et des notes
InterNote = LabelFrame(Analyseur, bg="white", text="Intervalle", bd=0)
InterNote.grid(row=7, column=1, sticky=W, padx=4, pady=1)
PrintInter = "YOLO" #REMPLACER PAR : Sortie(FreqNoteJuste)
Label(InterNote, text=PrintInter).grid(row=1, column=1, sticky=W, padx=4, pady=3)
NomNotes = LabelFrame(Analyseur, bg="white", text="Notes détectées", bd=0)
s = " - " #je met un tiret entre chaque note
ListeNote = ("a", "b", "c") #A SUPPRIMER C'EST POUR MES TESTS
Label(InterNote, text= s.join(ListeNote)).grid(row=2, column=1, sticky=W, padx=4, pady=7)

'_____________________________________________________________________________________________________________________'

#Fenêtre Générateur
Generateur = LabelFrame(main, bg="white", bd=2, height=400, text="Générer un Son", font="FontSS")
Generateur.columnconfigure(1, minsize=35)

#Amplitude
Amp = Scale(Generateur, orient="horizontal", from_=0, to=15000, resolution=100, sliderlength=20, label="Amplitude", length=277, bg="white")
Amp.grid(row=1, column=1, sticky=NW, padx=8, pady=6)

#Durée de la note
DNote = Scale(Generateur, orient="horizontal", from_=1, to=5, resolution=0.5, sliderlength=20, label="Durée de la Note", length=277, bg="white")
DNote.grid(row=2, column=1, sticky=NW, padx=8, pady=6)

#Gamme
Gammetext = Label(Generateur, text="Gamme :", bg="white")
Gammetext.grid(row=3, column=1, sticky=NW, padx=8, pady=12)
GammeEntry = Spinbox(Generateur, bg="white", values=("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"), wrap=True)
GammeEntry.grid(row=3, column=1, padx=20, pady=12, sticky=E)

#saisie du nom du fichier
NameFileEntry = Label(Generateur, text="Nom du Fichier :", bg="white")
NameFileEntry.grid(row=4, column=1, sticky=NW, padx=8, pady=12)
SaisieNom = Entry(Generateur, bg="white", width = 22)
SaisieNom.grid(row=4, column=1, padx=20, pady=12, sticky=E)

'_____________________________________________________________________________________________________________________'

#Fenêtre de gauche (les graphiques)
Graphs = Frame(main, height=400, width=550, bg="white")
Graphs.grid(row=3, column=2, pady = 15, padx=15)
p = PanedWindow(Graphs, orient="vertical")
p.grid(row=2, column=1)
p.add(Label(p, text="sf qsf qsff qsfqsf qsf azd za zsd", bg="black"))
p.add(Label(p, text="ALLAHU AKBAR", bg="blue"))


main.mainloop()

"""
import matplotlib.pyplot as plt
import numpy as np
import wave, struct
import sys

f = wave.open('lol2.wav','r')

plt.ion()
larg_frame = 44100

    # Sequence contenant une note
for i in range(0,larg_frame*8,larg_frame):
    f.setpos(i)
    donnee = f.readframes(larg_frame)
    data = struct.unpack('%sh' % (larg_frame ), donnee)
    
    
   
    signal = []
    n = 0
    for i in range(0,len(data),175):    # toute cette partie visait à réduire le nombre 
        signal.append(data[i])          # d'échantillon pour obtenir un signal (175 est une
        n += 1                          # est un diviseur de 44100, pour les trouver tu peux partir
    fs = 44100//175                     # de la multiplication de 2**2 * 3**2 * 5**2 * 7**2)
            
    n = len(signal)
    k = np.arange(n)
    T = n //252
    freq = k//T
    freq = freq[range(n//2)]
    
    Y = np.fft.fft(signal)/n
    Y = Y[range(n//2)]
    
    
            
            
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))       
            
    Time=np.linspace(0, len(signal)/fs, num=len(signal))
    
    plt.figure(1)
    plt.title('Signal Wave...')
    plt.ylim(-5500,5500)
    ax1.plot(Time,signal)
    ax2.plot(freq,abs(Y), 'r')
    plt.draw()
    plt.pause(3)
    plt.close()
"""







