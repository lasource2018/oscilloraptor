import math
import wave, struct
from struct import *
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from music21 import

def lecture_Son(nomFichier) :
    
    data = []
    f = wave.open(nomFichier, 'rb')

    nbCanaux = f.getnchannels()
    nbreEchant = f.getnframes()
    tailleEchant = f.getsampwidth()
    fech = f.getframerate()
    """
    print("Nombre de canaux :", nbreCanaux)
    print("Féquence d'échantillonnage :", fech)
    print("Taille de chaque échantillon :", tailleEchant, "octets")
    print("Nombre d'échantillons :", nbreEchant)

    print("Lecture du fichier...")
    """
    
    if tailleEchant == 2 :
        for i in range(nbreEchant) :
            b = f.readframes(1)
            val = struct.unpack('2h', b)
            data.append(val[0])
    elif tailleEchant == 1 :
        for i in range(nbreEchant) :
            b = f.readframes(1)
            val = struct.unpack('b', b)
            data.append(val[0])
    else :
        print("Format de fichier non reconnu")
        
    
    return f,data,nbCanaux,nbreEchant,fech


def Ecriture_Son(nomFichier, listeEch) :

    fech = 44100    #par défault pour le moment, mais peut être choisit par l'utilisateur
    nbreOctets = 2
    nbreCanaux = 1
    
    nbreEchant = len(listeEch)
    parametres = (nbreCanaux, nbreOctets,fech, nbreEchant, 'NONE', 'notcompressed')
    
    print("Enregistrement du fichier...")
    
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
    
    
def octave(freq):
    n = 0
    # pour reconnaitre les notes, on les transpose à l'octave 3. Cela permet une meilleur optimisation
    while freq < 255 or freq> 500 :
        if freq < 255:
            freq = freq * 2
            n = n - 1
        elif freq > 500:
            freq = freq/2
            n = n + 1
    return freq, n
    
Diese = 1        

def notefreqjuste (frequence, Diese): #Diese = 1 ou 0 selon affichage b ou #
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


oc = { "C": 131, "C#": 139, "D": 147, "D#": 156, "E": 165, "F": 175, "F#": 185, "G": 196, "G#": 208, "A": 220, "A#" :233, "B" : 247 }

oc2 = { "C":  261.63, "C#": 277.18, "Db": 277.18,"D": 293.66, "D#": 311.13, "Eb": 311.13,"E":329.63, "F":349.23, "F#": 369.99, "Gb": 369.99, "G": 392.00, "G#": 415.30, "Ab": 415.30, "A": 440.00, "A#" :466.16, "Bb" :466.16, "B" :  493.88, "C2" : 523 }

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
D_m = [oc["D#"],oc["E#"],oc["F#"],oc["G#"],oc["A#"],oc["B#"],oc2["D"],oc2["D#"]]
A_m = [oc["A#"],oc["B#"],oc2["C#"],oc2["D#"],oc2["E#"],oc2["F#"],oc2["A"],oc2["A#"]] 

#Gammes Majeures avec bémol
FM = [oc["F"],oc["G"],oc["A"],oc["Bb"],oc2["C"],oc2["D"],oc2["E"],oc2["F"]]
BbM= [oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"],oc2["F"],oc2["G"],oc2["A"],oc2["Bb"]]
EbM = [oc["Eb"],oc["F"],oc["G"],oc["Ab"],oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"]] 
AbM = [oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["G"],oc2["Ab"]] 
DbM = [oc["Db"],oc["Eb"],oc["F"],oc["Gb"],oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"]]
GbM = [oc["Gb"],oc["Ab"],oc["Bb"],oc2["B"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["Gb"]]
Cbm = [oc["Cb"],oc["Db"],oc["Eb"],oc["E"],oc["Gb"],oc["Ab"],oc["Cb"],oc2["Cb"]]

# Gammes Mineurs avec bémol
Dm = [oc["D"],oc["E"],oc["F#"],oc["G"],oc["A"],oc["Bb"],oc2["C#"],oc2["D"]]
Gm = [oc["G"],oc["A"],oc["Bb"],oc2["C"],oc2["D"],oc2["Eb"],oc2["F#"],oc2["G"]]
Cm = [oc["C"],oc["D"],oc["Eb"],oc["F"],oc["G"],oc["Ab"],oc["B"],oc2["C2"] ] 
Fm = [oc["F"],oc["G"],oc["Ab"],oc["Bb"],oc2["C"],oc2["Db"],oc2["E"],oc2["F"]]
Bbm = [oc["Bb"],oc2["C"],oc2["Db"],oc2["Eb"],oc2["F"],oc2["Gb"],oc2["A"],oc2["Bb"]]
Ebm = [oc["Eb"],oc["F"],oc["Gb"],oc["Ab"],oc["Bb"],oc2["B"],oc2["D"],oc2["Eb"]] 
Abm = [oc["Ab"],oc["Bb"],oc2["B"],oc2["Db"],oc2["Eb"],oc2["E"],oc2["G"],oc2["Ab"]] 

def ecrire_gamme(nom_fichier,gamme,amplitude,tps_note):
    E = []
    n = gamme
    for i in range(len(n)):
        O = [int(round(amplitude*math.sin(2*math.pi*n[i]*t*(1/44100)))) for t in  range(44100*tps_note)]
        E.extend(O)
    Ecriture_Son(nom_fichier, E)
    
#ecrire_gamme("gamme_GM.wav",GM,5000,1)


def func(x,a,b,c):
    return c * np.exp( -np.power( (x-a)/b, 2) )
 
#plt.ion()   # utilise pyplot en interactif
 
# Ouverture du fichier wav a decrypter
f, x, nbCanaux, nbFrames, fech = lecture_Son("pianoDM.wav")

#Decouper le fichier pour analyser chaque note après l'autre 
frequences, freq_gauss, FreqNoteJuste, ListeNote = [], [], [], []
larg_frame = 44100
i = 0
for posi in range(0,nbFrames,larg_frame):
    
 
    # Sequence contenant une note
    f.setpos(posi)
    donnee = f.readframes(larg_frame)
    data = struct.unpack('%sh' % (larg_frame*nbCanaux ), donnee)

    # Transformee de Fourier
    w     = np.fft.fft(data)
    sig   = np.real(w * w.conjugate())
    freqs = np.fft.fftfreq(len(w)) * nbFrames
 
    # Estimation de la frequence
    idx = np.argmax(sig)
    f0, maxi = np.abs(freqs[idx]), sig[idx]
    frequences.append( f0 )
    
    #Ajustement par une gaussienne
    ind = np.where( np.abs(freqs - f0) < 20 )
    popt, pcov = curve_fit( func, freqs[ind], sig[ind]/maxi, p0=[f0,1,1] )
    a, b, c = popt
    freq_gauss.append(a)
    note, n = notefreqjuste (a, Diese)
    ListeNote[i] = note
    i += 1
    FreqNoteJuste.append(oc2[note]*(n-1))
    
f.close()
for i in range(len(FreqNoteJuste)):
    print(FreqNoteJuste[i])
print(sortie(FreqNoteJuste))

#Analyse des Fréquences fournit soit par le générateur ou l'analyseur 
"""    
A = [261.63, 293.66, 329.63, 349.23, 392.00,440.00, 493.88]
#F
B = [349.23, 392.00, 440.00, 493.88,523.25, 587.33,659.26]
#A aéolien
L = [3520.00, 3951.07,4186.01,4698.64,5274.04, 5587.65,6271.93]
Diese = 1
"""

ListeNoteMusic21 = []
TailleListePrincipale = len(L)


#création des listes de notes 

#définission des intervalles        
def IntervalleBasique(L,Intervalle, PositionListe):
    TailleListe = len(L)
    for loop in range(TailleListe):
        quotien = L[loop]/L[0]
        if 2.2 < quotien < 1.8 and Intervalle == "Octave":
            return True
        if 1.49 < quotien < 1.51 and Intervalle == "Quinte":
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
        elif 1.18 < quotient <1.23 and Intervalle == "Tierce_maj":
            return True
            break
        elif 1.26 < quotient <1.24 and Intervalle == "Tierce_min":
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
        if Interalle == "Neuvieme":
            ValeurIntervalle = L[IntervalleBasique[L,"Quinte", True] * (3/2)/2
    for loop in range(TailleListe):
        quotien = L[loop]/ValeurIntervalle
        if 0.9 < quotien <= 1:
                return True
                break

    print("yes")
def GammeDeffinisseur(Liste):
    try:
        if IntervalleBasique(Liste, "TierceMaj",False):
            if IntervalleBasique(Liste,"Quarte", False) :
                if IntervalleComplexe(Liste, "SeptiemeMaj", True):
                    return "Ionien"
                else:
                    return "Mixolydien"
            else :
                return "Lydien"
        else :
            if IntervalleBasique(Liste, False):
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
        return "Erreur"

#Détections d'accords            
def AccordDeffinisseurTaille3(Liste):
    try :
        if IntervalleBasique(Liste, False):
            if IntervalleBasique(Liste,"Quinte", False):
                return ""
            elif IntervalleComplexe(Liste, "Sixte",True):
                 return "6"
        elif IntervalleBasique(Liste,"TierceMin", False):
            if IntervalleBasique(Liste,"Quinte", False):
                return "m"
            elif
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
        return "Unknown Chord"
def AccordDeffinisseurTaille4(Liste):
    try:
        if IntervalleComplexe(Liste,"SeptiemeMin", False):
            if AccordDeffinisseurTaille3(Liste, False) == "6" or "m6" or "sus4" or "sus2":
                return AccordDeffinisseurTaille3(Liste),"/7"
            else:
                return AccordDeffiniesseurTaille3(Liste),"7"
        if IntervalleComplexe(Liste, ):
            if AccordDeffinisseurTaille3(Liste) == "6" or "m6" or "sus4" or "sus2":
                return AccordDeffiniesseurTaille3(Liste), "/∆"
            else :
                return AccordDeffiniesseurTaille3(Liste), "∆"
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
        return "Erreur"

def Sortie(Liste):
    Taille = len(Liste)
    if Taille == 1:
        return Liste[0]
    elif Taille == 2:
        return Liste[0], IntervalleDeffinisseur(Liste)
    elif Taille == 3
        return Liste[0], AccordDeffinisseurTaille4(Liste)
    elif Taille < 5:
        return Liste[0], GammeDeffinisseur(Liste)
"""       
affichage gamme
besoin des liste ListeNote et ListeOctaveNote
pour les transformer en liste music21
"""
def Streamcreation(ListeNote,ListeOctaveNote):
    stream1 = stream.Stream()
    for loop in range(TailleListePrincipale):
        Note1 = note.Note("C4")
        Note1.name = ListeNote[loop]
        Note1.octave = ListeOctaveNote[loop]
        stream1.append(Note1)
    return stream1
