"""
EC plus con A e B matrici di int
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
from collections import Counter
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora_M(I, cardU, inter):
  global COV

  for k in inter:
    riassunto_esecuzione.append(" -- "+str(I)+", "+str(k)+"\n")
    Itemp = I + [k]

    cardTemp = cardU + sum(a==1 for a in A[k])
    if cardTemp == card_M:
      COV.append(Itemp)
    else:
      Bk = []

      for z in range(0, k):
        if (B[z][k] == 1):
          Bk.append((z))

      Intertemp = np.intersect1d(inter, Bk).astype(np.int16)
      if len(Intertemp) > 0:
        Esplora_M(Itemp, cardTemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_M(A):
  global COV
  global B
  COV = []
  print("Inizio Calcolo COV")
  card = []

  for i in range(len(A)):
    riassunto_esecuzione.append(" -- "+str(i)+"\n")
    if all(y==0 for y in A[i]):
      continue
    if all(y==1 for y in A[i]):
      COV.append([i])
      continue
    
    card.append(sum(a==1 for a in A[i]))
    for j in range(i):
      riassunto_esecuzione.append(" -- "+str(i)+", "+str(j)+"\n")
      intersezione = [sum(x) for x in zip(A[i],A[j])]
      intersezione=[1 if x==2 else 0 for x in intersezione ]

      if all(y==0 for y in intersezione):
        I = [i, j]
        cardU = card[i] + card[j]

        if cardU == card_M:
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

          intersezione = np.intersect1d(B1, B2).astype(np.int16)
          
          if len(intersezione):
            Esplora_M(I, cardU, intersezione)
  counts = Counter(card)
  riassunto_esecuzione.append("\nCardinalità di N:")
  for k,v in sorted(counts.items()):
    riassunto_esecuzione.append("\n\tNumero di elementi con cardinalità " + str(k) + " = " + str(v))

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
  card_M = len(A[0])

  COV = EC_M(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale_plus('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '1-plus', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto_plus('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '1-plus', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")