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

def Esplora_A_base(I, U, inter):
  global COV_base
  
  for k in inter:
    Itemp = I + [k]

    Utemp=[sum(x) for x in zip(U,A[k])]
    Utemp=[1 if x==2 else x for x in Utemp]
    
    if all(y==1 for y in Utemp):
      COV_base.append(Itemp)
    else:
      Bk = [b[0] for b in B_base
            if b[1]==k and b[0]<k]

      Intertemp = np.intersect1d(inter, Bk).astype(np.int16)
      if len(Intertemp) > 0:
        Esplora_A_base(Itemp, Utemp, Intertemp)

#ritorna COV
@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_A_base(A):
  global COV_base
  global B_base
  COV_base = []
  print("Inizio Calcolo COV")
  for i in range(len(A)):
    if all(y==0 for y in A[i]):
      continue
    if all(y==1 for y in A[i]):
      COV_base.append([i])
      continue

    for j in range(i):
      intersezione = [sum(x) for x in zip(A[i],A[j])]
      intersezione = [1 if x==2 else 0 for x in intersezione ]
      intersezione_pos = []

      if all(y==0 for y in intersezione):
        I = [i, j]
        U=[sum(x) for x in zip(A[i],A[j])]
        U=[1 if x==2 else x for x in U ]

        if all(y==1 for y in U):
          COV_base.append(I)
        else:
          B_base.append((j, i))
          B1 = [b for b in B_base
                if b[1]==i and b[0]<j]
          B2 = [b for b in B_base
                if b[1]==j and b[0]<j]

          for x in B1:
            if [item for item in B2 if x[0] in item] != []:
              intersezione_pos.append(x[0])
            elif [item for item in B2 if x[1] in item] != []:
              intersezione_pos.append(x[1])
          
          if intersezione_pos:
            Esplora_A_base(I, U, intersezione_pos)
  riassunto_esecuzione_base.append("\nB base finale -> "+str(mod.actualsize(B_base))+" bytes\n")
  print("Ritorno Calcolo COV")
  return COV_base

def Esplora_A_plus(I, cardU, inter):
  global COV_plus

  for k in inter:
    Itemp = I + [k]

    cardTemp = cardU + sum(a==1 for a in A[k])
    if cardTemp == card_M:
      COV_plus.append(Itemp)
    else:
      Bk = [b[0] for b in B_plus
            if b[1]==k and b[0]<k]

      Intertemp = np.intersect1d(inter, Bk).astype(np.int16)
      if len(Intertemp) > 0:
        Esplora_A_plus(Itemp, cardTemp, Intertemp)

@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_A_plus(A):
  global COV_plus
  global B_plus
  COV_plus = []

  card = []

  for i in range(len(A)):
    if all(y==0 for y in A[i]):
      continue
    if all(y==1 for y in A[i]):
      COV_plus.append([i])
      continue

    card.append(sum(a==1 for a in A[i]))
    for j in range(i):
      intersezione = [sum(x) for x in zip(A[i],A[j])]
      intersezione = [1 if x==2 else 0 for x in intersezione ]
      intersezione_pos = []

      if all(y==0 for y in intersezione):
        I = [i, j]
        cardU = card[i] + card[j]

        if cardU == card_M:
          COV_plus.append(I)
        else:
          B_plus.append((j, i))
          B1 = [b for b in B_plus
                if b[1]==i and b[0]<j]
          B2 = [b for b in B_plus
                if b[1]==j and b[0]<j]

          for x in B1:
            if [item for item in B2 if x[0] in item] != []:
              intersezione_pos.append(x[0])
            elif [item for item in B2 if x[1] in item] != []:
              intersezione_pos.append(x[1])
          
          if intersezione_pos:
            Esplora_A_plus(I, cardU, intersezione_pos)
  riassunto_esecuzione_plus.append("\nB plus finale -> "+str(mod.actualsize(B_plus))+" bytes\n")
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

  A = mod.leggi_matrice(percorso_file) 
  B_base = list()
  riassunto_esecuzione_base=[]

  COV_base = EC_A_base(A)

  exec_time_base = (time.time() - start_time) * 1000.0
  heapStatus_base = h.heap()

  h.setref()

  start_time = time.time()

  A = mod.leggi_matrice(percorso_file)
  B_plus = list()
  riassunto_esecuzione_plus=[]
  card_M = len(A[0])

  COV_plus = EC_A_plus(A)

  exec_time_plus = (time.time() - start_time) * 1000.0
  heapStatus_plus = h.heap()

  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_finale('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_confronto_interrotto('./file/output/output_'+nome_file_input, mod.actualsize(A), A, B_base, B_plus, riassunto_esecuzione_base, riassunto_esecuzione_plus, COV_base, COV_plus, heapStatus_base, heapStatus_plus, exec_time_base, exec_time_plus)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")