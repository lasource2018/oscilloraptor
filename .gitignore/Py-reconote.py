from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
import wave, struct, math
from struct import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Définition des fonctions
    
#Importation du fichier et vérification du format (.wav only)
def selec_fichier():
    pathfilename =  filedialog.askopenfilename(initialdir = "/",title = "Sélection du fichier audio",filetypes = (("audio files","*.*"),("all files","*.*")))
    longueur = len(pathfilename)
    ext = []
    for boucle in range(1,5):
        ext.append(pathfilename[-boucle])
    ext.reverse()
    Extension = "".join(ext)
    if Extension != ".wav":
        messagebox.showerror("Erreur", "Mauvais Format : Veuillez sélectionner un fichier .wav")
    else:
        Filenamebox.delete(0.0, END)
        Filenamebox.insert(END, pathfilename)
        return pathfilename

#switch entre les onglets générer et analyser
def switchMode():
    SM = AnaGen.get()
    if SM == 0:
       Generateur.grid_forget()
       Analyseur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)
    elif SM == 1:
        Analyseur.grid_forget()
        Generateur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)


# Ecris un fichier audio .wav à partir d'une onde sinusoïde et d'une fréquence d'échantillonage
def Ecriture_Son(nomFichier, listeEch) :

    nbreOctets = 2
    nbreCanaux = 1
    fech = 44100
    
    nbreEchant = len(listeEch)
    parametres = (nbreCanaux, nbreOctets,fech, nbreEchant, 'NONE', 'notcompressed')
    
    
    Liste = []
    for i in range(nbreEchant) :
        b = struct.pack('h',listeEch[i])
        Liste.append(b[0])
        Liste.append(b[1])
    
    data = bytes(Liste)
    
    f = wave.open(nomFichier, 'wb')
    f.setparams(parametres)
    f.writeframes(data)
    f.close()
    messagebox.showinfo("Succès", "Le fichier son a bien été généré avec succès.")
    
# 2 dictionnaire classant les notes de D0 131 à DO 523 soit 2 octaves
oc = { "C": 131, "C#": 139, "Db" : 139,"D": 147, "D#": 156,"Eb":156, "E": 165, "F": 175, "F#": 185,"Gb":185, "G": 196, "G#": 208, "Ab":208,"A": 220, "A#" :233,"Bb" : 233, "B" : 247 }

oc2 = { "C":  262, "C#": 277, "Db": 277,"D": 294, "D#": 311, "Eb": 311,"E":330, "F":349, "F#": 370, "Gb": 370, "G": 392, "G#": 415, "Ab": 415, "A": 440, "A#" :466, "Bb" :466, "B" :  494, "C2" : 523 }


# ensemble des gammes majeures et mineures

CM = [oc["C"],oc["D"],oc["E"],oc["F"],oc["G"],oc["A"],oc["B"],oc2["C"] ] 
Am = [oc["A"],oc["B"],oc2["C"],oc2["D"],oc2["E"],oc2["F"],oc2["G#"],oc2["A"]]

#Gammes Majeurs avec #
GM = [oc["G"],oc["A"],oc["B"],oc2["C"],oc2["D"],oc2["E"],oc2["F#"],oc2["G"]]
DM = [oc["D"],oc["E"],oc["F#"],oc["G"],oc["A"],oc["B"],oc2["C#"],oc2["D"]]
AM = [oc["A"],oc["B"],oc2["C#"],oc2["D"],oc2["E"],oc2["F#"],oc2["G#"],oc2["A"]] 
EM = [oc["E"],oc["F#"],oc["G#"],oc["A"],oc["B"],oc2["C#"],oc2["D#"],oc2["E"]] 
BM = [oc["B"],oc2["C#"],oc2["D#"],oc2["E"],oc2["F#"],oc2["G#"],oc2["A#"],oc2["B"]] 
F_M = [oc["F#"],oc["G#"],oc["A#"],oc["B"],oc2["C#"],oc2["D#"],oc2["F"],oc2["F#"]] 
C_M = [oc["C#"],oc["D#"],oc["F"],oc["F#"],oc["G#"],oc["A#"],oc2["C"],oc2["C#"]]

#Gammes Mineurs avec #
Em = [oc["E"],oc["F#"],oc["G"],oc["A"],oc["B"],oc2["C"],oc2["D#"],oc2["E"]] 
Bm= [oc["B"],oc2["C#"],oc2["D"],oc2["E"],oc2["F#"],oc2["G"],oc2["A#"],oc2["B"]] 
F_m = [oc["F#"],oc["G#"],oc["A"],oc["B"],oc2["C#"],oc2["D"],oc2["F"],oc2["F#"]]
C_m = [oc["C#"],oc["D#"],oc["E"],oc["F#"],oc["G#"],oc["A"],oc["C"],oc2["C#"]]
G_m = [oc["G#"],oc["A#"],oc["B"],oc2["C#"],oc2["D#"],oc2["E"],oc2["G"],oc2["G#"]]
D_m = [oc["D#"],oc["F"],oc["F#"],oc["G#"],oc["A#"],oc["C"],oc2["D"],oc2["D#"]]
A_m = [oc["A#"],oc["C"],oc2["C#"],oc2["D#"],oc2["F"],oc2["F#"],oc2["A"],oc2["A#"]] 

#Gammes Majeures avec bémol
FM = [oc["F"],oc["G"],oc["A"],oc["Bb"],oc2["C"],oc2["D"],oc2["E"],oc2["F"]]
BbM= [oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"],oc2["F"],oc2["G"],oc2["A"],oc2["Bb"]]
EbM = [oc["Eb"],oc["F"],oc["G"],oc["Ab"],oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"]] 
AbM = [oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["G"],oc2["Ab"]] 
DbM = [oc["Db"],oc["Eb"],oc["F"],oc["Gb"],oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"]]
GbM = [oc["Gb"],oc["Ab"],oc["Bb"],oc2["B"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["Gb"]]
CbM= [oc["B"],oc["Db"],oc["Eb"],oc["E"],oc["Gb"],oc["Ab"],oc["Bb"],oc2["B"]]

# Gammes Mineurs avec bémol
Dm = [oc["D"],oc["E"],oc["F#"],oc["G"],oc["A"],oc["Bb"],oc2["C#"],oc2["D"]]
Gm = [oc["G"],oc["A"],oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"],oc2["F#"],oc2["G"]]
Cm = [oc["C"],oc["D"],oc["Eb"],oc["F"],oc["G"],oc["Ab"],oc["B"],oc2["C2"] ] 
Fm = [oc["F"],oc["G"],oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"],oc2["E"],oc2["F"]]
Bbm = [oc["Bb"],oc2["C"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["Gb"],oc2["A"],oc2["Bb"]]
Ebm = [oc["Eb"],oc["F"],oc["Gb"],oc["Ab"],oc["Bb"],oc2["B"],oc2["D"],oc2["Eb"]] 
Abm = [oc["Ab"],oc["Bb"],oc2["B"],oc2["Db"],oc2["Eb"],oc2["E"],oc2["G"],oc2["Ab"]] 

identification = { "CM": CM, "GM":GM, "DM":DM, "AM":AM, "EM":EM, "FM":FM, "BbM":BbM, "EbM":EbM, "AbM":AbM, "Am":Am, "Em":Em, "Bm":Bm,"Dm":Dm,"Gm":Gm}

# génère une gamme composé d'une suite de sinus, le fichier est ensuite enregistré dans le dossier où est enregistré le code python
def ecrire_gamme(nom_fichier,gamme,amplitude,tps_note):
    E = []
    n = identification[gamme]
    for i in range(len(n)):
        O = [int(round(amplitude*math.sin(2*math.pi*n[i]*t*(1/44100)))) for t in  range(44100*tps_note)]
        E.extend(O)
    Ecriture_Son(nom_fichier, E)


#La fonction reliée au bouton Lancer la génération, qui récupère toutes les valeurs et lance "ecrire_gamme()"

def Launch_Generation():
    nom_fichier = SaisieNom.get()
    gamme = GammeEntry.get()
    amplitude = Amp.get()
    tps_note = DNote.get()
    ecrire_gamme(nom_fichier,gamme,amplitude,tps_note)




# extrait plusieurs données(nombre de canaux, fréquence d'échantillonage, nombre d'échantillon) ainsi que tout le contenu d'un fichier d'un fichier audio .wav
def lecture_Son(nomFichier) :
    
    data = []
    f = wave.open(nomFichier, 'rb')

    nbCanaux = f.getnchannels()
    nbreEchant = f.getnframes()
    tailleEchant = f.getsampwidth()
    fech = f.getframerate()
    
    if tailleEchant == 2 :
        for i in range(nbreEchant) :
            b = f.readframes(1)
            try:
                val = struct.unpack('h', b)
            except:
                val = struct.unpack('2h',b)
            data.append(val[0])
            
    elif tailleEchant == 1 :
        for i in range(nbreEchant) :
            b = f.readframes(1)
            val = struct.unpack('b', b)
            data.append(val[0])
    else :
        print("Format de fichier non reconnu")
        
    
    return f,data,nbCanaux,nbreEchant,fech
    
#définission des intervalles 
       
def IntervalleBasique(L,Intervalle, PositionListe):
    TailleListe = len(L)
    for loop in range(TailleListe):
        quotient = L[loop]/L[0]
        if 2.2 < quotient < 1.8 and Intervalle == "Octave":
            return True
        if 1.49 < quotient < 1.51 and Intervalle == "Quinte":
            if PositionListe:
                return loop
            else :
                return True
            break
        elif 1.32 < quotient < 1.34  and Intervalle =="Quarte":
            if PositionListe:
                return loop
            else :
                return True
            break
        elif 1.18 < quotient <1.23 and Intervalle == "TierceMin":
            return True
            break
        elif 1.24 <quotient <1.26 and Intervalle == "TierceMaj":
            return True
            break
        elif 1.16 < quotient < 1.10 and Intervalle == "Seconde":
            return True
            break
           
def IntervalleComplexe(L, Intervalle, CalcVTheorique):
    TailleListe = len(L)
    if CalcVTheorique :
        if Intervalle == "Sixte":
            ValeurIntervalle = L[0] * (5/4) *(4/3)
        elif Intervalle == "SeptiemeMaj":
            ValeurIntervalle = L[0] * (3/2) * (5/4)
        elif Intervalle == "SeptiemeMin":
            ValeurIntervalle = L[0] * (3/2) * (3/2)
        elif Intervalle == "Neuvieme":
            ValeurIntervalle = (L[0] * (3/2)*(4/3))/2
    else:
        if Intervalle == "Sixte":
            ValeurIntervalle = L[IntervalleBasique(L,"Quarte",True)] * (5/3)
        elif Intervalle == "SeptiemeMaj":
           ValeurIntervalle = L[IntervalleBasique(L,"Quinte", True)]*(5/4)
        elif Intervalle == "SeptiemeMin":
            ValeurIntervalle = L[IntervalleBasique(L, "Quinte",True)]*(3/2)
        if Intervalle == "Neuvieme":
            ValeurIntervalle = L[IntervalleBasique(L,"Quinte", True)] * (3/2)/2
    for loop in range(TailleListe):
        quotient = L[loop]/ValeurIntervalle
        if 0.9 < quotient <= 1.01:
                return True
                break

def GammeDeffinisseur(Liste):
    try:
        if IntervalleBasique(Liste, "TierceMaj",False):
            if IntervalleBasique(Liste,"Quarte", False) :
                if IntervalleComplexe(Liste, "SeptiemeMaj", False):
                    return "Ionien"
                else:
                    return "Mixolydien"
            else :
                return "Lydien"
        else :
            if IntervalleBasique(Liste, "Quinte", False):
                if IntervalleComplexe(Liste,"Sixte", True):
                    if Intervallecomplexe(Liste,"Neuvieme", True):
                        return "Aéolien"
                    else:
                        return "Phrygien"
                else:
                    return "Dorien"
            else:
                return "Locrien"
    except:
        return "."

#Détections d'accords            
def AccordDeffinisseurTaille3(Liste):
    try :
        if IntervalleBasique(Liste, "TierceMaj", False):
            if IntervalleBasique(Liste,"Quinte", False):
                return "."
            elif IntervalleComplexe(Liste, "Sixte",True):
                 return "6"
        elif IntervalleBasique(Liste,"TierceMin", False):
            if IntervalleBasique(Liste,"Quinte", False):
                return "m"
            elif IntervalleComplexe(Liste,"Sixte", True):
                return "m6"
        elif IntervalleBasique(Liste,"Quarte", False):
            if IntervalleBasique(Liste,"Quinte", False):
                    return "sus4"
        elif IntervalleComplexe(Liste,"Neuvevieme", False):
            if IntervalleBasique(Liste,"Quinte", False):
                return "sus2"
        elif IntervalleBasique(Liste, "Octave", False):
            if IntervalleBasique(Liste,"Quinte", False):
                return "PowerChord HEEEELL YEAH"
    except:
        return "."
def AccordDeffinisseurTaille4(Liste):
    try:
        if IntervalleComplexe(Liste,"SeptiemeMin", True):
            if AccordDeffinisseurTaille3(Liste, False) == "6" or "m6" or "sus4" or "sus2":
                return AccordDeffinisseurTaille3(Liste),"/7"
            else:
                return AccordDeffinisseurTaille3(Liste),"7"
        if IntervalleComplexe(Liste,"SeptiemeMaj",True):
            if AccordDeffinisseurTaille3(Liste) == "6" or "m6" or "sus4" or "sus2":
                return AccordDeffinisseurTaille3(Liste), "/∆"
            else :
                return AccordDeffinisseurTaille3(Liste), "∆"
    except:
        return AccordDeffinisseurTaille3(Liste)
    
#détection d'intervalles            
def IntervalleDeffinisseur(Liste):
    try:
        Intervalle = ["Seconde","TierceMaj","TierceMin","Quarte","Quinte","Sixt","SeptiemeMin","septiemeMaj"]
        n = 0
        while n <= len(Intervalle):
            if IntervalleBasique(Liste, Intervalle[n], False) or IntervalleComplexe(Liste, Intervalle[n], True):
                return Intervalle[n]
            n = n + 1
    except:
        return "."

#fonction général qui réunie toute les fonctions qui viennent d'être défini
def sortie(ListeFreq,ListeNote):
    Taille = len(ListeFreq)
    if Taille == 1:
        return ListeNote[0]
    elif Taille == 2:
        return IntervalleDeffinisseur(ListeFreq)
    elif Taille == 3 or 4:
        return ListeNote[0], AccordDeffinisseurTaille4(ListeFreq)
    elif Taille > 5:
        return ListeNote[0], GammeDeffinisseur(ListeFreq)


# A partir d'une note à une octave quelconque, transpose cette note à l'octave 3 (entre 260 et 495) et conserve dans une variable l'octave d'origine 
def octave(freq):
    n = 0
    while freq < 255 or freq> 500 :
        if freq < 255:
            freq = freq * 2
            n = n - 1
        elif freq > 500:
            freq = freq/2
            n = n + 1
    return freq, n


# Identifie une note à partir de sa fréquence, Diese == 1 ou 0 selon affichage souhaités # ou b
def notefreqjuste (frequence, Diese): 
    a, n = octave(frequence)
    if  259 < a < 263:
         return "C",n

    elif 274 < a < 279:
         if Diese == 1:
             return "C#",n
         else:
             return "Db",n
   
    elif 290 < a < 295:
         return "D",n
            
    elif 309 < a < 313:
         if Diese == 1:
             return "D#",n
         else:
             return "Eb",n
            
    elif 326 < a <332:
         return "E",n

    elif 346 < a < 351:
         return "F",n

    elif 366 < a < 371:
        if Diese == 1:
            return "F#",n
        else :
            return "Gb",n

    elif 389 < a < 395:
        return "G",n

    elif 412 < a < 418:
        if Diese == 1:
            return "G#",n
        else:
            return "Ab",n

    elif 437 < a < 443:
        return "A",n

    elif  463 < a < 469:
        if Diese == 1:
            return "A#",n
        else:
            return "Bb",n

    elif 490 < a < 496:
        return "B",n



#fonction d'affinage qui sera utilisé plus tard
def func(x,a,b,c):
    return c * np.exp( -np.power( (x-a)/b, 2) )


#fonction qui va lire le fichier, séparés les données pour chaque note, faire la transformée de fourier pour chaque note et enfin afficher un graphique représentant les 2 courbes


def analyser_son(nomFichier):
    plt.ion     #on utilise pyplot en interactif
    
    # Ouverture du fichier wav a decrypter
    f, x, nbCanaux, nbFrames, fech = lecture_Son(nomFichier)
    
    #Découper le fichier pour analyser une note après l'autre 
    frequences, FreqNoteJuste, ListeNote,  = [], [], [], 
    larg_frame = fech
    for posi in range(0,nbFrames,larg_frame):
    
        # Sequence contenant une note
        f.setpos(posi)
        donnee = f.readframes(larg_frame)
        data = struct.unpack('%sh' % (larg_frame*nbCanaux ), donnee)
    
        # Transformee de Fourier
        fourier  = np.fft.fft(data)                                
        valeur_réelle   = np.real(fourier * fourier.conjugate())
        freqs = np.fft.fftfreq(len(fourier)) * nbFrames
    
        # Estimation de la frequence
        idx = np.argmax(valeur_réelle)
        f0, maxi = np.abs(freqs[idx]), valeur_réelle[idx]
        frequences.append( f0 )
    
        #Ajustement par une gaussienne (permet l'ajustement des valeurs de f0)
        ind = np.where( np.abs(freqs - f0) < 20 )
        popt, pcov = curve_fit( func, freqs[ind], valeur_réelle[ind]/maxi, p0=[f0,1,1] )
        a, b, c = popt
        note, n = notefreqjuste(a,Diese)
        ListeNote += note
        
        FreqNoteJuste.append(oc2[note]*(n-1))
    
        #Affichage
        signal = []
        for i in range(0,len(data),175):     
            signal.append(data[i])                                   
        fs = 44100//175
    
        Time=np.linspace(0, len(signal)/fs, num=len(signal))
    
        plt.subplot(211)
        plt.plot(Time,signal)
        plt.title("onde sonore et sa fréquence fondamentale")
        plt.xlim(0,1)
        
        plt.subplot(212)
        fnew = np.linspace( freqs[ind][0], freqs[ind][-1], 512)
        plt.plot( fnew, maxi * func(fnew,a,b,c), 'r')
        
        plt.draw() 
        plt.pause(0.5)
        plt.clf()
        
    plt.close
    f.close()
    intervale = sortie(FreqNoteJuste, ListeNote)
    return ListeNote, intervale
    
#La fonction reliée au bouton Lancer l'analyse, qui sélectionne et lance la fonction "analyser_son"
def Launch_Analyser():
    nomFichier = selec_fichier()
    a, b = analyser_son(nomFichier)
    AllNotes = " ".join(a)
    return AllNotes

def Launch_Analyser2():
    nomFichier = selec_fichier()
    a, b = analyser_son(nomFichier)
    tableau = []
    print(b)
    tableau.append(b[0])
    tableau.append(b[1][0])
    tableau.append(b[1][1])
    AllIntervalles = " ".join(tableau)
    return AllIntervalles

#Début de l'interface graphique
fenetre = Tk()
fenetre.title("oscilloraptorz")
fenetre.configure(background="white")
Label (fenetre, text="Module d'analyse et de génération de sons :", bg="white", fg="black", font="none 15 bold") .grid(row=1, column=1, sticky=NW)
FontSS = tkFont.Font(size=18)


'_____________________________________________________________________________________________________________________'

#fenêtre de droite
CadreMode = LabelFrame(fenetre, bg="white", bd=0, height=50)
CadreMode.grid(row=2, column=1, sticky=NW, pady=7, padx=10)
AnaGen = IntVar()
AnaGen.set(0)
Ana = Radiobutton(CadreMode, text="Analyseur", value=0, variable=AnaGen, indicatoron=0, command=switchMode)
Ana.grid(row=2, column=1, sticky=NW, pady=5, padx=10)
Gen = Radiobutton(CadreMode, text="Générateur", value=1, variable=AnaGen, indicatoron=0, command = switchMode)
Gen.grid(row=2, column=2, sticky=NW, pady=5, padx=10)

'_____________________________________________________________________________________________________________________'

#Fenêtre analyseur
Analyseur = LabelFrame(fenetre, bg="white", bd=2, height=400, text="Analyser un Son", font="FontSS")
Analyseur.grid(row=3, column=1, sticky=NW, pady=15, padx=10)

#Importation du fichier
Filenamebox = Text(Analyseur, width = 35, height=1, wrap=WORD, bg="white", fg="blue")
Filenamebox.grid(row=3, column=1, sticky=NW, pady=10, padx=8)
Import = Button(Analyseur, text="IMPORTER", command=selec_fichier) 
Import.grid(row=4, column=1, sticky=NW, padx=8, pady=2)
AnaLaunch = Button(Analyseur, text="Lancer l'analyse", command=Launch_Analyser)
AnaLaunch.grid(row=4, column=1, padx=8, pady=2, sticky=E)

#Affichage en Diese ou en bémol
Diese = IntVar() 
Diese.set(1)
Di = Radiobutton(Analyseur, text='Dièse (#)', value=1, variable=Diese, bg ="white")
Di.grid(row=6, column=1, sticky=W, padx=4, pady=11)
Label (Analyseur, text="<-- Affichage -->", bg="white") .grid(row=6, column=1, padx=4, pady=11)
Be = Radiobutton(Analyseur, text='Bémol (b)', value=0, variable=Diese, bg ="white")
Be.grid(row=6, column=1, sticky=E, padx=4, pady=11)

#Affichage des intervalles et des notes
InterNote = LabelFrame(Analyseur, bg="white", text="Intervalle", bd=0)
InterNote.grid(row=7, column=1, sticky=W, padx=4, pady=1)
Label(InterNote, text=Launch_Analyser2()).grid(row=1, column=1, sticky=W, padx=4, pady=3)
NomNotes = LabelFrame(Analyseur, bg="white", text="Notes détectées", bd=0)
Label(InterNote, text=Launch_Analyser()).grid(row=2, column=1, sticky=W, padx=4, pady=7)

'_____________________________________________________________________________________________________________________'

#Fenêtre Générateur
Generateur = LabelFrame(fenetre, bg="white", bd=2, height=400, text="Générer un Son", font="FontSS")
Generateur.columnconfigure(1, minsize=35)

#Amplitude
Amp = Scale(Generateur, orient="horizontal", from_=0, to=15000, resolution=100, sliderlength=20, label="Amplitude", length=277, bg="white")
Amp.grid(row=1, column=1, sticky=NW, padx=8, pady=6)

#Durée de la note
DNote = Scale(Generateur, orient="horizontal", from_=1, to=5, resolution=1, sliderlength=20, label="Durée de la Note", length=277, bg="white")
DNote.grid(row=2, column=1, sticky=NW, padx=8, pady=6)

#Gamme
Gammetext = Label(Generateur, text="Gamme :", bg="white")
Gammetext.grid(row=3, column=1, sticky=NW, padx=8, pady=12)
GammeEntry = Spinbox(Generateur, bg="white", values=("CM", "GM", "DM", "AM", "EM", "FM", "BbM", "EbM", "AbM", "Am", "Em", "Bm","Dm","Gm"), wrap=True)
GammeEntry.grid(row=3, column=1, padx=20, pady=12, sticky=E)

#saisie du nom du fichier
NameFileEntry = Label(Generateur, text="Nom du Fichier :", bg="white")
NameFileEntry.grid(row=4, column=1, sticky=NW, padx=8, pady=12)
SaisieNom = Entry(Generateur, bg="white", width = 22)
SaisieNom.grid(row=4, column=1, padx=20, pady=12, sticky=E)

#Bouton générer
GenLaunch = Button(Generateur, text="Lancer la génération", command=Launch_Generation)
GenLaunch.grid(row=5, column=1, padx=20, pady=12, sticky=W)

'_____________________________________________________________________________________________________________________'



fenetre.mainloop()




