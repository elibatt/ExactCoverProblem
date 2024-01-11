"""
EC base con A e B lista di tuple delle posizioni compatibili senza usare NP
"""
import sys
import numpy as np
import array as arr
import os, psutil
import guppy  
from guppy import hpy
import time 
import timeout_decorator
from collections import Counter
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora_base(I, U, inter):
  global COV_base
  
  for k in inter:
    Itemp = I + [k]

    Utemp = list(set(U) | set(A[k]))
    
    if len(Utemp) == M:
      COV_base.append(Itemp)
    else:
      Bk = [b for b in B_base[k] if b<k]
      
      Intertemp = []
      for x in inter:
        if x in set(Bk):
          Intertemp.append(x)
      if len(Intertemp)>0:
        Esplora_base(Itemp, Utemp, Intertemp)

#ritorna COV
@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_base(A):
  global COV_base
  global B_base
  COV_base = []
  print("Inizio Calcolo COV")
  for i in range(len(A)):
    if len(A[i]) == 0:
      continue
    if len(A[i]) == M:
      COV_base.append([i])
      continue

    for j in range(i):
      
      condizione_inters = True
      for x in A[i]:
        if x in set(A[j]):
          condizione_inters = False
          break
      intersezione_pos = []
      if condizione_inters:
        I = [i, j]
        
        U = list(set(A[i]) | set(A[j]))

        if len(U) == M:
          COV_base.append(I)
        else:
          B_base[i].append(j)
          
          B1 = [b for b in B_base[i] if b<j]
          B2 = [b for b in B_base[j] if b<j]

          for x in B1:
            if x in set(B2):
              intersezione_pos.append(x)
          
          if intersezione_pos:
            Esplora_base(I, U, intersezione_pos)
  riassunto_esecuzione_base.append("\nB finale -> "+str(mod.actualsize(B_base))+" bytes\n")
  print("Ritorno Calcolo COV")
  COV_base = np.array(COV_base, dtype=object)
  return COV_base

def Esplora_plus(I, cardU, inter):
  global COV_plus
  
  for k in inter:
    Itemp = I + [k]

    cardTemp = cardU + len(A[k])
    
    if cardTemp == M:
      COV_plus.append(Itemp)
    else:
      Bk = [b for b in B_plus[k] if b<k]
      
      Intertemp = []
      for x in inter:
        if x in set(Bk):
          Intertemp.append(x)
      if len(Intertemp)>0:
        Esplora_plus(Itemp, cardTemp, Intertemp)

#ritorna COV
@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_plus(A):
  global COV_plus
  global B_plus
  COV_plus = []

  card = []

  print("Inizio Calcolo COV")
  for i in range(N):
    if len(A[i]) == 0:
      card.append(len(A[i]))
      continue
    if len(A[i]) == M:
      card.append(len(A[i]))
      COV_plus.append([i])
      continue
    
    card.append(len(A[i]))
    for j in range(i):
      
      condizione_inters = True
      for x in A[i]:
        if x in set(A[j]):
          condizione_inters = False
          break
      intersezione_pos = []
      if condizione_inters:
        I = [i, j]
        cardU = card[i] + card[j]

        if cardU == M:
          COV_plus.append(I)
        else:
          B_plus[i].append(j)
          
          B1 = [b for b in B_plus[i] if b<j]
          B2 = [b for b in B_plus[j] if b<j]

          for x in B1:
            if x in set(B2):
              intersezione_pos.append(x)
          
          if intersezione_pos:
            Esplora_plus(I, cardU, intersezione_pos)
  counts = Counter(card)
  riassunto_esecuzione_plus.append("\nCardinalità:\n")
  for k,v in counts.items():
    riassunto_esecuzione_plus.append(str(k) + " = " + str(v) + "\n")
  riassunto_esecuzione_plus.append("\nB finale -> "+str(mod.actualsize(B_plus))+" bytes\n")
  print("Ritorno Calcolo COV")
  COV_plus = np.array(COV_plus, dtype=object)
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
  B_base = [list() for row in range(len(A))]
  riassunto_esecuzione_base=[]

  COV_base = EC_base(A)

  exec_time_base = (time.time() - start_time) * 1000.0
  heapStatus_base = h.heap()

  h.setref()

  start_time = time.time()

  A, N, M = mod.leggi_posizioni_arr_matrice_np(percorso_file)
  B_plus = [list() for row in range(len(A))]
  riassunto_esecuzione_plus=[]
  card_M = len(A[0])

  COV_plus = EC_plus(A)

  exec_time_plus = (time.time() - start_time) * 1000.0
  heapStatus_plus = h.heap()

  print("Inizio stampa")
  dim_A = mod.actualsize(A)
  A = mod.ottieni_matrice_binaria(A, N, M)

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_finale('./file/output/output_'+nome_file_input, A, dim_A, B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
except StopIteration:
  exec_time_base = (time.time() - start_time) * 1000.0
  heapStatus_base = h.heap()
  dim_A = mod.actualsize(A)
  A = mod.ottieni_matrice_binaria(A, N, M)

  if 'B_plus' not in locals():
    B_plus = list(list())
    riassunto_esecuzione_plus = list()
    COV_plus = np.array(list(), dtype=object)
    heapStatus_plus = heapStatus_base
    exec_time_plus = 0.0
  
  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_interrotto('./file/output/output_'+nome_file_input, A, dim_A, B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")