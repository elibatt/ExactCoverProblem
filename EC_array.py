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
import _include.funzioni_comuni as mod

mod.leggi_configurazioni("config.txt")

def Esplora_A(I, U, inter):
  global COV
  
  for k in inter:
    riassunto_esecuzione.append(" -- "+str(I)+", "+str(k)+"\n")
    Itemp = I + [k]

    Utemp=[sum(x) for x in zip(U,A[k])]
    Utemp=[1 if x==2 else x for x in Utemp]
    
    if all(y==1 for y in Utemp):
      COV.append(Itemp)
    else:
      Bk = [b[0] for b in B
            if b[1]==k and b[0]<k]
      
      Intertemp = np.intersect1d(inter, Bk).astype(np.int16)
      if len(Intertemp)>0:
        Esplora_A(Itemp, Utemp, Intertemp)

#ritorna COV
@timeout_decorator.timeout(mod.tempo_limite, timeout_exception=StopIteration)
def EC_A(A):
  global COV
  global B
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
      intersezione_pos = []

      if all(y==0 for y in intersezione):
        I = [i, j]
        U=[sum(x) for x in zip(A[i],A[j])]
        U=[1 if x==2 else x for x in U ]

        if all(y==1 for y in U):
          COV.append(I)
        else:
          B.append((j,i))
          
          B1 = [b for b in B
                if b[1]==i and b[0]<j]
          B2 = [b for b in B
                if b[1]==j and b[0]<j]

          for x in B1:
            if [item for item in B2 if x[0] in item] != []:
              intersezione_pos.append(x[0])
            elif [item for item in B2 if x[1] in item] != []:
              intersezione_pos.append(x[1])
          
          if intersezione_pos:
            Esplora_A(I, U, intersezione_pos)
  riassunto_esecuzione.append("\nB finale -> "+str(mod.actualsize(B))+" bytes\n")
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
  B = list()
  riassunto_esecuzione=[]

  COV = EC_A(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '2-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto('./file/output/output_'+nome_file_input, A, mod.actualsize(A), B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '2-base', nome_file_input, mod.actualsize(A), B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")