import random
import time
import multiprocessing as mp
from multiprocessing import Pool

NP_PROCESS = 4

def calculMonteCarlo(nbIteration):
    """
        calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
    """
    count = 0
    for i in range(int(nbIteration)):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1:
            count += 1

    return count


def estimePI(count, nbIterations):
    """
        Permet d'estimer PI
    """
    return 4 * sum(count) / nbIterations


def multiprocess(nbIterations):
    """
        Méthode Monte Carlo en multi-processus
    """
    start = time.time()

    # On divise le nombre d'itération par le nombre de processus
    iterationsParProcess = [nbIterations/NP_PROCESS for i in range(NP_PROCESS)]

    with Pool(processes=NP_PROCESS) as pool:
        count = pool.map(calculMonteCarlo, iterationsParProcess)
        pi = estimePI(count, nbIterations)

    end = time.time()

    temps = end - start

    print(
        f"Temps de traitement {temps:.2f} secondes pour {nbIterations} iterations en multiprocess")
    print(
        f"Valeur estimée Pi par la méthode Hit-Miss avec {NP_PROCESS} processus : {pi}")


def monoprocess(nbIterations):
    """
        Méthode Monte Carlo en mono-processus
    """
    start = time.time()

    nbHits = calculMonteCarlo(nbIterations)
    pi = 4 * nbHits / nbIterations

    end = time.time()

    temps = end - start

    print(
        f"Temps de traitement {temps:.2f} secondes pour {nbIterations} iterations en monoprocessus")
    print(f"Valeur estimée Pi par la méthode Mono−Processus {pi}")


if __name__ == "__main__":
    
    # Nombre d’essai pour l’estimation
    nbIterations = 100_000_000
    
    print("Début du multiprocessing")

    multiprocess(nbIterations)
    
    print("Fin du multiprocessing\n")
    print("Début du monoprocessus")
    monoprocess(nbIterations)
    print("Fin du monoprocessus")

