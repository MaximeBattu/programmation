import time
import random
import os
import ctypes

import multiprocessing as mp
import numpy as np

TAILLE = 30
NB_PROCESS = 5

def clear():
    os.system("clear")

# Create a shared two dimensionnal array
shared_current_grid = mp.Array(ctypes.c_int, TAILLE * TAILLE)
shared_next_grid = mp.Array(ctypes.c_int, TAILLE * TAILLE)

# create a numpy array from the shared memory block
current_grid = np.frombuffer(shared_current_grid.get_obj(), ctypes.c_int)
next_grid = np.frombuffer(shared_next_grid.get_obj(), ctypes.c_int)

# reshape the array into a two dimensional array
current_grid = current_grid.reshape((TAILLE, TAILLE))
next_grid = next_grid.reshape((TAILLE, TAILLE))

# Fill the starting grid 
for ligne in current_grid :
    for cellule in ligne :
        cellule = 0

def display_grid(grid):
    for line in grid:
        for cell in line:
            if cell == 0:
                print(" ", end="")
            else:
                print("X", end="")
        print("|")
    print("‾"*TAILLE)

def addGlider(x, y, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,   0, 1],
                       [1,  0, 1],
                       [0,  1, 1]])
    grid[x:x+3, y:y+3] = glider

# Fonction qui renvoie le nombre de voisins vivants d'une cellule donnée
def living_neighbours_count(x, y, grid):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif x + i < 0 or x + i >= TAILLE or y + j < 0 or y + j >= TAILLE:
                continue
            elif grid[x + i][y + j] == 1:
                count += 1
    return count

# Fonction qui traire une cellule
def render_cell(x, y, current_grid, next_grid):
    living_neighbours = living_neighbours_count(x, y, current_grid)
    if current_grid[x][y] == 1:
        if living_neighbours == 2 or living_neighbours == 3:
            next_grid[x][y] = 1
        else :
            next_grid[x][y] = 0
    else:
        if living_neighbours == 3:
            next_grid[x][y] = 1


# Fonction qui traite une ligne
def render_line(line, current_grid, next_grid):
    for cell in range(TAILLE):
        render_cell(line, cell, current_grid, next_grid)

# Ajout d'une glider dans la grille de départ
addGlider(1, 1, current_grid)

for i in range(TAILLE):
    for j in range(len(current_grid[i])):
        if random.randint(0, 4) == 0:
            current_grid[i][j] = 1
            

while True:
    # Pack de processus
    for pack in range(TAILLE//NB_PROCESS):
        # print(f"Pack #{pack}")
        for line in range(NB_PROCESS) :
            p = mp.Process(target=render_line, args=(pack*NB_PROCESS + line, current_grid, next_grid))
            p.start()
        
        for _ in range(NB_PROCESS):
            p.join()

    display_grid(next_grid)

    for i in range(TAILLE):
        for j in range(len(next_grid[i])):
            current_grid[i][j] = next_grid[i][j]

    time.sleep(0.2)
    clear()