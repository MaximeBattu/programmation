import ctypes
import multiprocessing as mp
import random
import time
import queue

def creeExpression(queue):
    """
        Retourne une expression aléatoire et la met dans la Queue d'expression
    """
    opd1 = random.randint(1, 10)
    opd2 = random.randint(1, 10)
    operateur = random.choice(['+', '-', '*', '/'])
    
    expression = str(opd1) + operateur + str(opd2)
    
    queue.put(expression)
    
    return expression

def fils(expressionCalculs, queueResult, keepCalculating):
    """
        Calcul l'expression récupérée depuis la Queue et met le résultat dans la Queue
    """
    while keepCalculating.value:
        # Gestion de l'exception si la Queue est vide
        pris = True
        try :
            expression = expressionCalculs.get(timeout=0.4)
        except queue.Empty:
            pris = False
        
        if pris :
            print(f"Le fils a recu {expression}")
            expression = expression
            res=eval(expression)
            print(f"Dans fils, le résultat = {res}")
            queueResult.put(res)
            print(f"Le fils a envoyé {res}")

def demandeur(nbCalcul, expressionCalculs, queueResult, keepCalculating):
    """
        Met des expressions de calculs dans la Queue associée
    """
    for i in range(nbCalcul):
        strCalcul = creeExpression(expressionCalculs)

        result = queueResult.get() 

        print(f"{strCalcul} = {result}\n")

        time.sleep(0.2)

    keepCalculating.value = False

if __name__ == "__main__":
    # Queue d'expression
    expressionCalculs = mp.Queue()
    # Queue de résultat
    queueResult = mp.Queue()
    
    childProcesses = []
    
    keepCalculating = mp.Value(ctypes.c_bool, True)

    nbCalcul = input("Combien de calculs voulez-vous lancer ? 2 par défaut\n")
    if (nbCalcul):
        nbCalcul = int(nbCalcul)
    else:
        nbCalcul = 2
        
    nbProcesses = input("Combien de processus calculateurs ? 2 par défaut\n")
    if (nbProcesses):
        nbProcesses = int(nbProcesses)
    else:
        nbProcesses = 2

    app = mp.Process(target=demandeur, args=(
        nbCalcul, expressionCalculs, queueResult, keepCalculating))
    
    for i in range(nbCalcul):
        child = mp.Process(target=fils, args=(
        i, expressionCalculs, queueResult, keepCalculating))
        childProcesses.append(child)

    app.start()
    for i in range(nbCalcul):
        childProcesses[i].start()

    app.join()
    for i in range(nbCalcul):
        childProcesses[i].join()
