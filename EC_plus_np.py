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
from collections import Counter
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora(I, cardU, inter):
  global COV
  
  for k in inter:
    riassunto_esecuzione.append(" -- "+str(I)+", "+str(k)+"\n")
    Itemp = np.union1d(I, k)[::-1]

    cardTemp = cardU + sum(a==1 for a in A[k])

    if cardTemp == card_M:
      COV.append(list(Itemp))
    else:
      Bk = [b[0] for b in B
            if b[1]==k and b[0]<k]
      Intertemp = np.intersect1d(inter,Bk)
      if Intertemp.size:
        Esplora(Itemp, cardTemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC(A):
  global COV
  global B
  COV = []
  print("Inizio Calcolo COV")
  card = []

  for i in range(len(A)):
    riassunto_esecuzione.append(" -- "+str(i)+"\n")
    if np.all(A[i]==0):
      continue
    if np.all(A[i]==1):
      COV.append([i])
      continue
    
    card.append(sum(a==1 for a in A[i]))

    for j in range(i):
      riassunto_esecuzione.append(" -- "+str(i)+", "+str(j)+"\n")
      res1 = np.where(A[i]==1)
      res2 = np.where(A[j]==1)
      intersezione = np.intersect1d(res1, res2)

      if not intersezione.size:
        I = (i, j)
        cardU = card[i] + card[j]

        if cardU == card_M:
          COV.append(I)
        else:
          B.append((j, i))

          B1 = [b for b in B
                if b[1]==i and b[0]<j]
          B2 = [b for b in B
                if b[1]==j and b[0]<j]
          intersezione = np.intersect1d(B1, B2).astype(np.int16)
          if len(intersezione):
            Esplora(I, cardU, intersezione)
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

  A = np.array(mod.leggi_matrice(percorso_file)).astype(np.int16)
  B = list()
  riassunto_esecuzione = []
  card_M = A.shape[1]

  COV = EC(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale_plus('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '3-plus', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto_plus('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '3-plus', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")