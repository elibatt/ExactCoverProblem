"""
EC base con A e B matrici di int
"""

import numpy as np
import array as arr
import os, psutil
import sys
from sys import getsizeof
import gc
import guppy  
from guppy import hpy 
import time 
import timeout_decorator
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora_M(I, U, inter):
  global COV

  for k in inter:
    riassunto_esecuzione.append(" -- "+str(I)+", "+str(k)+"\n")
    Itemp = I + [k]
    Utemp=[sum(x) for x in zip(U,A[k])]
    Utemp=[1 if x==2 else x for x in Utemp]
    if all(y==1 for y in Utemp):
      COV.append(Itemp)
    else:
      Bk=[]
      for z in range(0, k):
        if (B[z][k] == 1):
          Bk.append((z))
      
      Intertemp = np.intersect1d(inter, Bk).astype(np.int16)
      if len(Intertemp) > 0:
        Esplora_M(Itemp, Utemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_M(A):
  global COV
  COV = []
  print("Inizio Calcolo COV")
  for i in range(len(A)):
    riassunto_esecuzione.append(" -- "+str(i)+"\n")
    if all(y==0 for y in A[i]):
      continue
    if all(y==1 for y in A[i]):
      COV.append([i])
      continue

    for j in range(i):
      riassunto_esecuzione.append(" -- "+str(i)+", "+str(j)+"\n")
      intersezione = [sum(x) for x in zip(A[i],A[j])]
      intersezione = [1 if x==2 else 0 for x in intersezione ]
      intersezione_pos=[]

      if all(y==0 for y in intersezione):
        I = [i, j]
        U = [sum(x) for x in zip(A[i],A[j])]
        U = [1 if x==2 else x for x in U ]

        if all(y==1 for y in U):
          COV.append(I)
        else:
          B[j][i] = 1

          B1 = []
          B2 = []
          for k in range(0, j):
            if B[k][i]==1:
              B1.append((k))
            if B[k][j]==1:
              B2.append((k))
          
          for x in B1:
            if x in set(B2):
              intersezione_pos.append(x)
          
          if len(intersezione):
            Esplora_M(I, U, intersezione_pos)
  riassunto_esecuzione.append("B finale -> "+str(mod.actualsize(B))+" bytes\n")
  print("Ritorno Calcolo COV")
  return COV

######################codice##############

if len(sys.argv) > 1:
  percorso_file = "file/" + sys.argv[1]
else:
  percorso_file = "file/matrice_consegna_relazione.txt"

try:
  h = hpy()
  h.setref()

  start_time = time.time()

  A = mod.leggi_matrice(percorso_file)
  B = [[0 for col in range(len(A))] for row in range(len(A))]
  riassunto_esecuzione=[]

  COV = EC_M(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '1-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '1-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")