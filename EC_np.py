"""
EC base con A matrice NP, B lista di tuple delle posizioni compatibili
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

def Esplora(I, U, inter):
  global COV
  
  for k in inter:
    riassunto_esecuzione.append(" -- "+str(I)+", " + str(k)+"\n")

    Itemp = np.union1d(I, k)[::-1].astype(np.int16).tolist()

    Utemp=[sum(x) for x in zip(U,A[k])]
    Utemp=[1 if x==2 else x for x in Utemp ]
    Utemp=np.array(Utemp).astype(np.int16)

    if(np.all(Utemp==1)):
      COV.append(Itemp)
    else:
      Bk = [b[0] for b in B
            if b[1]==k and b[0]<k]
      Intertemp = np.intersect1d(inter,Bk).astype(np.int16)
      if Intertemp.size:
        Esplora(Itemp, Utemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC(A):
  global COV
  global B
  COV = []
  print("Inizio Calcolo COV")
  for i in range(len(A)):
    riassunto_esecuzione.append(" -- "+str(i)+"\n")
    if np.all(A[i]==0):
      continue
    if np.all(A[i]==1):
      COV.append([i])
      continue

    for j in range(i):
      riassunto_esecuzione.append(" -- "+str(i)+", "+str(j)+"\n")
      res1 = np.where(A[i]==1)
      res2 = np.where(A[j]==1)
      intersezione = np.intersect1d(res1, res2).astype(np.int16)

      if not intersezione.size:
        I = [i, j]
        U=[sum(x) for x in zip(A[i],A[j])]
        U=[1 if x==2 else x for x in U ]
        U=np.array(U).astype(np.int16)
        intersezione_pos = []

        if np.all(U==1):
          COV.append(I)
        else:
          B.append((j, i))

          B1 = [b[0] for b in B
                if b[1]==i and b[0]<j]
          B2 = [b[0] for b in B
                if b[1]==j and b[0]<j]
          intersezione = np.intersect1d(B1, B2).astype(np.int16).tolist()
          # for x in B1:
          #   if x in set(B2):
          #     intersezione_pos.append(x)

          # if len(intersezione_pos):
          #   Esplora(I, U, intersezione_pos)
          if len(intersezione):
            Esplora(I, U, intersezione)
  riassunto_esecuzione.append("B finale ->"+str(mod.actualsize(B))+" bytes\n")
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

  A = np.array(mod.leggi_matrice(percorso_file)).astype(np.int16)
  B = list()
  riassunto_esecuzione=[]

  COV = EC(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '3-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '3-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")