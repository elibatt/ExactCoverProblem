"""
File per capitolo 3.1 della relazione
"""

import gc
from sys import getsizeof
import sys
import numpy as np
import array as arr
import os, psutil
import guppy  
from guppy import hpy
import time 
import timeout_decorator
import _include.funzioni_comuni as mod

def leggi_matrice(percorso_file):
    input = open(percorso_file, "r")
    A = []
    for line in input:
        if(line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        parts = [eval(i) for i in parts]
        A.append(parts)
    return A

def leggi_matrice_np(percorso_file):
    input = open(percorso_file, "r")
    A = []
    for line in input:
        if(line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        parts = [eval(i) for i in parts]
        A.append(parts)
    return np.array(A)

def leggi_posizioni_matrice(percorso_file):
    input = open(percorso_file, "r")
    A = list()
    N = 0
    M = 0
    for line in input:
        if (line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        M = len(parts)
        parts = [i for i, x in enumerate(parts) if x == "1"]

        for x in parts:
            A.append((N, x))
        N = N + 1
    return A, N, M

def leggi_posizioni_matrice_np(percorso_file):
    input = open(percorso_file, "r")
    A = []
    N = 0
    M = 0
    for line in input:
        if (line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        M = len(parts)
        parts = [i for i, x in enumerate(parts) if x == "1"]

        for x in parts:
            A.append((N, x))
        N = N + 1
    A = np.array(A, dtype=object)
    return A, N, M

def leggi_posizioni_arr_matrice(percorso_file):
    input = open(percorso_file, "r")
    A = list()
    N = 0
    M = 0
    for line in input:
        if (line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        M = len(parts)
        parts = [i for i, x in enumerate(parts) if x == "1"]

        A.append(parts)
        N = N + 1
    return A, N, M

def leggi_posizioni_arr_matrice_np(percorso_file):
    input = open(percorso_file, "r")
    A = []
    N = 0
    M = 0
    for line in input:
        if (line.startswith(";;;") or line == "\n"):
            continue
        ind = line.index("-")
        line = line[0:ind]
        parts = line.split(" ")[:-1]
        M = len(parts)
        parts = [i for i, x in enumerate(parts) if x == "1"]

        A.append(parts)
        N = N + 1
    A=np.array([np.array(xi) for xi in A], dtype=object)
    return A, N, M

def actualsize(input_obj):
    memory_size = 0
    ids = set()
    objects = [input_obj]
    while objects:
        new = []
        for obj in objects:
            if id(obj) not in ids:
                ids.add(id(obj))
                memory_size += getsizeof(obj)
                new.append(obj)
        objects = gc.get_referents(*new)
    return memory_size

percorso_file = "file/nuovastruttura_A.txt"

A = leggi_matrice(percorso_file)
print(A)
A_np = leggi_matrice_np(percorso_file)
A_pos, N, M = leggi_posizioni_matrice(percorso_file)
print(A_pos)
A_np_pos, N, M = leggi_posizioni_matrice_np(percorso_file)
A_arr, N, M = leggi_posizioni_arr_matrice(percorso_file)
print(A_arr)
A_np_arr, N, M = leggi_posizioni_arr_matrice_np(percorso_file)

print("BASE:")
print("A - matrice di interi = " + str(actualsize(A)) + " B")
print("A - array di tuple = " + str(actualsize(A_pos)) + " B")
print("A - array di array = " + str(actualsize(A_arr)) + " B")
print("----")
print("NP:")
print("A - matrice di interi = " + str(A_np.nbytes) + " B")
print("A - array di tuple = " + str(A_np_pos.nbytes) + " B")
A_np_arr_size = 0
for x in A_np_arr:
    A_np_arr_size += x.nbytes
print("A - array di array = " + str(A_np_arr_size) + " B")