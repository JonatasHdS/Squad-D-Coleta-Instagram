from os import listdir
from os.path import isfile, join
import csv

# Diretorio
diretorio= r"C:\Users\Pichau\Documents\GitHub\Squad-D-Coleta-Instagram\CSV'sunificados"

# Recupera lista de ficheiros CSV em um diretorio
ficheiros = [f for f in listdir(diretorio) if (isfile(join(diretorio, f)) and f.endswith('.csv')) ]

# Abre ficheiro de saida...
with open("saida"+'.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)

# Para cada ficheiro...
for f in ficheiros:
    with open(f,'r', encoding='utf-8', newline='') as in_file, open('saida'+'.csv','a', encoding='utf-8', newline='') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate

            seen.add(line)
            out_file.write(line)
