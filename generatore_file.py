import sys
import numpy as np
import random
import _include.funzioni_comuni as mod

np.set_printoptions(threshold=sys.maxsize)
# Esecuzione
mod.leggi_configurazioni("config.txt")

for i in range(mod.num_file_da_generare):
    try:
        with open('./file/input_'+str(i+1)+'.txt', 'w') as f:
            percentuale_zero = random.randint(mod.min_percentuale_zero, mod.max_percentuale_zero)

            num_righe = random.randint(mod.min_righe, mod.max_righe)
            num_colonne = random.randint(mod.min_colonne, mod.max_colonne)
            array = np.random.randint(100, size=(num_righe, num_colonne))

            array[array <= percentuale_zero] = 0
            array[array > percentuale_zero] = 1

            tmp_min_righe = mod.min_righe
            if(mod.elimina_righe_zeri):
                num_righe_zero = sum(~np.all(array == 0, axis=1))
                num_righe = num_righe_zero
                array = array[~np.all(array == 0, axis=1)]

                if(num_righe < mod.min_righe):
                    mod.min_righe = num_righe

            f.write(';;;input_'+str(i+1)+'\n')

            content = str(array)
            content = content.replace(" [", "")
            content = content.replace("[[", "")
            content = content.replace("]]", " -")
            content = content.replace("]", " -")

            f.write(content)
            f.write("\n\n;;;|N| = " + str(num_righe))
            f.write("\n;;;|M| = " + str(num_colonne))
            f.write("\n;;;min_righe = " + str(mod.min_righe) + "; max_righe = " + str(mod.max_righe) + ";")
            f.write("\n;;;min_colonne = " + str(mod.min_colonne) + "; max_colonne = " + str(mod.max_colonne) + ";")
            f.write("\n;;;percentuale_zero = " + str(percentuale_zero) + "%")

            # resetto numero minimo di righe
            min_righe = tmp_min_righe
    except FileNotFoundError:
        print("errore")
print("\nFile generati correttamente\n")