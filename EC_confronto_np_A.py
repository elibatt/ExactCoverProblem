"""
EC confronto base e NP con A e B lista di tuple delle posizioni compatibili senza usare NP
"""
import sys
import numpy as np
import array as arr
import os, psutil
import guppy  
from guppy import hpy
import time 
import timeout_decorator
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora_base(I, U, inter):
  global COV_base
  
  for k in inter:
    Itemp = np.union1d(I, k)[::-1].astype(np.int16)

    Utemp=np.union1d(U, A[k]).astype(np.int16)

    if(len(Utemp) == M):
      COV_base.append(list(Itemp))
    else:
      Bk = [b[0] for b in B_base
            if b[1]==k and b[0]<k]
      Intertemp = np.intersect1d(inter,Bk).astype(np.int16)
      if Intertemp.size:
        Esplora_base(Itemp, Utemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_base(A):
  global COV_base
  global B_base
  COV_base = []

  for i in range(N):
    if len(A[i]) == 0:
      continue
    if len(A[i]) == M:
      COV_base.append([i])
      continue

    for j in range(i):
      intersezione = np.intersect1d(A[i], A[j]).astype(np.int16)

      if not intersezione.size:
        I = (i, j)
        U=np.union1d(A[i], A[j])

        if len(U) == M:
          COV_base.append(I)
        else:
          B_base.append((j, i))

          B1 = [b for b in B_base
                if b[1]==i and b[0]<j]
          B2 = [b for b in B_base
                if b[1]==j and b[0]<j]
          intersezione = np.intersect1d(B1, B2).astype(np.int16)
          if len(intersezione):
            Esplora_base(I, U, intersezione)
  riassunto_esecuzione_base.append("B base finale ->"+str(mod.actualsize(B_base))+" bytes\n")
  return COV_base


def Esplora_plus(I, cardU, inter):
  global COV_plus
  
  for k in inter:
    Itemp = np.union1d(I, k)[::-1].astype(np.int16)

    cardTemp = cardU + len(A[k])

    if(cardTemp == M):
      COV_plus.append(list(Itemp))
    else:
      Bk = [b[0] for b in B_plus
            if b[1]==k and b[0]<k]
      Intertemp = np.intersect1d(inter,Bk).astype(np.int16)
      if Intertemp.size:
        Esplora_plus(Itemp, cardTemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_plus(A):
  global COV_plus
  global B_plus
  COV_plus = []

  card = []

  for i in range(N):
    if len(A[i]) == 0:
      continue
    if len(A[i]) == M:
      COV_plus.append([i])
      continue

    card.append(len(A[i]))

    for j in range(i):
      intersezione = np.intersect1d(A[i], A[j]).astype(np.int16)

      if not intersezione.size:
        I = (i, j)
        cardU = card[i] + card[j]

        if cardU == M:
          COV_plus.append(I)
        else:
          B_plus.append((j, i))

          B1 = [b for b in B_plus
                if b[1]==i and b[0]<j]
          B2 = [b for b in B_plus
                if b[1]==j and b[0]<j]
          intersezione = np.intersect1d(B1, B2).astype(np.int16)
          if len(intersezione):
            Esplora_plus(I, cardU, intersezione)
  riassunto_esecuzione_plus.append("B plus finale ->"+str(mod.actualsize(B_plus))+" bytes\n")
  return COV_plus

######################codice##############

if len(sys.argv) > 1:
  percorso_file = "file/" + sys.argv[1]
else:
  percorso_file = "file/matrice_consegna_relazione.txt"

try:
  h = hpy()
  h.setref()

  start_time = time.time()

  A, N, M = mod.leggi_posizioni_arr_matrice_np(percorso_file)
  B_base = []
  riassunto_esecuzione_base=[]

  COV_base = EC_base(A)

  exec_time_base = (time.time() - start_time) * 1000.0
  heapStatus_base = h.heap()

  h.setref()

  start_time = time.time()

  A, N, M = mod.leggi_posizioni_arr_matrice_np(percorso_file)
  B_plus = []
  riassunto_esecuzione_plus=[]
  card_M = len(A[0])

  COV_plus = EC_plus(A)

  exec_time_plus = (time.time() - start_time) * 1000.0
  heapStatus_plus = h.heap()

  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_finale('./file/output/output_'+nome_file_input, mod.ottieni_matrice_binaria(A,N,M), mod.actualsize(A), B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_interrotto('./file/output/output_'+nome_file_input, mod.ottieni_matrice_binaria(A,N,M), mod.actualsize(A), B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")