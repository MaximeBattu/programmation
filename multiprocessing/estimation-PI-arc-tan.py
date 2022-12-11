import time
import multiprocessing as mp
from multiprocessing import Pool

NP_PROCESS = 2

def arc_tangente(nbIteration):
    """
        calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
    """
    pi = 0
    for i in range(int(nbIteration)):
        pi += 4/(1+ ((i+0.5)/nbIteration)**2)

    return pi


def estimePI(piArcTan, nbIterations):
    """
        Permet d'estimer PI
    """
    return (1/nbIterations) * float(sum(piArcTan))


def multiprocess(nbIterations):
    """
        Méthode Monte Carlo en multi-processus
    """
    start = time.time()

    # On divise le nombre d'itération par le nombre de processus
    iterationsParProcess = [nbIterations/NP_PROCESS for i in range(NP_PROCESS)]

    with Pool(processes=NP_PROCESS) as pool:
        piArcTan = pool.map(arc_tangente, iterationsParProcess)
        pi = estimePI(piArcTan, nbIterations)

    end = time.time()

    temps = end - start

    print(
        f"Temps de traitement {temps:.2f} secondes pour {nbIterations} iterations en multiprocess")
    print(
        f"Valeur estimée Pi par la méthode arc-tangente avec {NP_PROCESS} processus : {pi}")


if __name__ == "__main__":
    
    # Nombre d’essai pour l’estimation
    nbIterations = 100_000_000
    

    multiprocess(nbIterations)
