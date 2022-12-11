CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

import multiprocessing as mp

import threading
import time
import random
import string
import os,sys
import platform
import ctypes

lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')
def en_couleur(Coul) : print(Coul,end='')

S = int(input("Nombre de serveurs : "))
T = int(input("Max de commande possible : "))

## Variables partagées
tampon = []
tabServeurs = []
tabCommandes = []
lastServie = ""
endService = 0
locker = mp.Lock()

def clients():
    global tampon
    global T
    for i in range (0, T):
        if (i > 0):
            sleeping = random.randint(1, 4)
            time.sleep(sleeping)
        with locker:
            tampon.append(str(random.randint(1, 50)) + str(random.choice(string.ascii_uppercase)))

def major_dHomme():
    global S
    global tampon
    global endService
    global lastServie
    global tabCommandes
    while (endService == 0 and len(tabCommandes) > 0):
        with locker:
            effacer_ecran()
            curseur_invisible()
            for i in range (1, S+1):
                move_to(i, 0)
                erase_line_from_beg_to_curs()
                en_couleur(lyst_colors[i%len(lyst_colors)])
                if (len(tabCommandes[i-1]) > 1):
                    print('Le serveur',i,"traite la commande", tabCommandes[i-1])
                else :
                    print('Le serveur',i,"ne traite pas de commande pour le moment")
            move_to(i+2, 0)
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[i+1%len(lyst_colors)])
            print("Les commandes clients en attente : ", tampon)
            move_to(i+3, 0)
            erase_line_from_beg_to_curs()
            print('Nombres de commandes attente : ', len(tampon))
            move_to(i+4, 0)
            erase_line_from_beg_to_curs()
            if (lastServie == ""):
                print("Aucune commande n'a été servie pour le moment")
            else:
                print('Commande', lastServie,'est servie au client')
        time.sleep(1)

def serveurs(i):
    global tabCommandes
    global tampon
    global lastServie
    global endService
    time.sleep(5)
    while (endService == 0 and len(tampon) > 0 and len(tabCommandes) > 0):
        with locker:
            if (len(tampon) > 0):
                tabCommandes[i] = tampon[0]
                del tampon[0]
            else:
                tabCommandes[i] = "0"
        time.sleep(2)
        with locker:
            sleeping = random.randint(1, 3)
            time.sleep(sleeping)
            lastServie = tabCommandes[i]
            tabCommandes[i] = "0"
        time.sleep(2)

for i in range(0, S):
    tabCommandes.append("0")

if platform.system() == "Darwin" :
    mp.set_start_method('fork')


processClient = mp.Process(target=clients, args=[])
processClient.start()

majorHomme = mp.Process(target=major_dHomme, args=[])
majorHomme.start()

for i in range(0, S):
    tabServeurs.append(mp.Process(target=serveurs, args=[i]))
    tabServeurs[i].start()

for i in range(0, S):
    tabServeurs[i].join()
processClient.join()
majorHomme.join()
