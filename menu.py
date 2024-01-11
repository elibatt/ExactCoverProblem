import sys
import os

def mainmenu ():
    d = ''
    while d == '':
        print ('\nM E N U')
        print ("####  EC  ####")
        print ('1. Prima versione')
        print ('2. Seconda versione')
        print ('3. Terza versione')
        print ('4. Quarta versione')
        print ('5. Quinta versione')
        print("####  Generatore ####")
        print('6. Generatore files input')
        print ('q. Chiudi')
        option = input ('Seleziona: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option == '1':
            d = submenu ('EC_matrici.py')
        elif option == '2':
            d = submenu('EC_array.py')
        elif option == '3':
            d = submenu ('EC_np.py')
        elif option == '4':
            d = submenu('EC_np_A.py')
        elif option == '5':
            d = submenu ('EC_quinta_versione.py')
        elif option == '6':
            nome_file = 'generatore_file.py'
            print("\n----Esecuzione di " + nome_file + "-----\n\n")
            exec(open(nome_file).read())
            return mainmenu()
        else:
            print ('Scelta non valida!')
    return d

def submenu (nome_file):
    p = ''
    while p == '':
        print ('\nS U B  M E N U')
        print ('1. Base')
        print ('2. Plus')
        print ('3. Confronto')
        print ('b. Indietro')
        print ('q. Chiudi')
        option = input ('Seleziona un\'opzione: ')
        if option.lower () == 'q':
            sys.exit ()
        elif option.lower () == 'b':
            return mainmenu ()
        elif option == '1':
            p = nome_file
            file_da_eseguire = input('Scrivi il nome dell\'istanza da eseguire: ')
            sys.argv = [p,file_da_eseguire]
        elif option == '2':
            if nome_file.startswith("EC_"):
               p = nome_file[0:3] + "plus_" + nome_file[3:len(nome_file)]
            file_da_eseguire = input('Scrivi il nome dell\'istanza da eseguire: ')
            sys.argv = [p, file_da_eseguire]
        elif option == '3':
            if nome_file.startswith("EC_"):
               p = nome_file[0:3] + "confronto_" + nome_file[3:len(nome_file)]
            file_da_eseguire = input('Scrivi il nome dell\'istanza da eseguire: ')
            sys.argv = [p, file_da_eseguire]
        else:
            print ('Selezione non valida!')
    return p

nome_file = mainmenu()
print("\n----Esecuzione di " + nome_file + "-----\n\n")
exec(open(nome_file).read())