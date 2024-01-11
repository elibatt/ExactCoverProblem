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

    Utemp = list(set(U) | set(A[k]))
    
    if len(Utemp) == M:
      COV.append(Itemp)
    else:
      Bk = [b for b in B[k] if b<k]
      
      Intertemp = []
      for x in inter:
        if x in set(Bk):
          Intertemp.append(x)
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
    if len(A[i]) == 0:
      continue
    if len(A[i]) == M:
      COV.append([i])
      continue

    for j in range(i):
      riassunto_esecuzione.append(" -- "+str(i)+", "+str(j)+"\n")
      


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
          COV.append(I)
        else:
          B[i].append(j)
          
          B1 = [b for b in B[i] if b<j]
          B2 = [b for b in B[j] if b<j]

          for x in B1:
            if x in set(B2):
              intersezione_pos.append(x)
          
          if intersezione_pos:
            Esplora_A(I, U, intersezione_pos)
  riassunto_esecuzione.append("\nB finale -> "+str(mod.actualsize(B))+" bytes\n")
  print("Ritorno Calcolo COV")
  COV = np.array(COV, dtype=object)
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

  A, N, M = mod.leggi_posizioni_arr_matrice_np(percorso_file) 
  B = [list() for row in range(len(A))]
  riassunto_esecuzione=[]

  COV = EC_A(A)

  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  print("Inizio stampa")
  dim_A = mod.actualsize(A)
  A = mod.ottieni_matrice_binaria(A, N, M)

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_finale('./file/output/output_'+nome_file_input, A, dim_A, B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('OK', '5-base', nome_file_input, dim_A, B, COV, riassunto_esecuzione, heapStatus, exec_time)
except StopIteration:
  exec_time = (time.time() - start_time) * 1000.0
  heapStatus = h.heap()
  dim_A = mod.actualsize(A)
  A = mod.ottieni_matrice_binaria(A, N, M)

  nome_file_input = percorso_file
  if "/" in percorso_file:
    nome_file_input = percorso_file.partition("/")[2]

  mod.stampa_output_interrotto('./file/output/output_'+nome_file_input, A, dim_A, B, riassunto_esecuzione, COV, heapStatus, exec_time)
  mod.stampa_storico('STOP', '5-base', nome_file_input, dim_A, B, COV, riassunto_esecuzione, heapStatus, exec_time)
  print("Esecuzione interrotta per superamento limite massimo di tempo")
except FileNotFoundError:
  print("Percorso file non trovato")