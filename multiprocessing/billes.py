import threading
import time

V = threading.Lock()
N = int(input("Nombre de processus : "))
M = int(input("Nombre d'itérations : "))
B = int(input("Nombre max de billes : "))
D = B
tabRessource = []
tabProcess = []

def Controleur():
    global D
    global B
    while True:
        with V:
            if (D < 0 or D > B):
                print("ERROR !")
                exit()
        time.spleep(1)

def Demander(k_bills, j):
    global D
    print("Process n°",j," demande. Ressources dispo : ", D)
    while (D < k_bills):
        with V:
            print("Process n°",j," en attente de ressources")
            time.sleep(1)
    with V:
        D -= k_bills
    print("Process n°",j," a reçu. Ressources dispo : ", D)

def Rendre(k_bills, j):
    global D
    print("Process n°",j," rends. Ressources dispo : ", D)
    with V:
        D += k_bills
    print("Process n°",j," a rendu. Ressources dispo : ", D)

def Travailleur(j):
    global tabRessource
    global M
    for i in range (0, M):
        Demander(tabRessource[j], j)
        print("Process n°",j, " utilise ses ressources")
        time.sleep(2)
        Rendre(tabRessource[j], j)

for i in range (0, N):
    tmp = int(input("Ressources requises : "))
    while (tmp < 0 or tmp > B):
        tmp = int(input("Merci de choisir un nombre de ressource requis supérieur à 0 et inférieur au nombre de billes max : "))
    tabRessource.append(tmp)

for i in range (0, N):
    tabProcess.append(threading.Thread(target=Travailleur, args=[i]))
    tabProcess[i].start()

for i in range (0, N):
    tabProcess[i].join()
