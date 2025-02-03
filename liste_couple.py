import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def generate_pairs_chunk(start, end, nb_tri):
    return [(i, j) for i in range(start, end) for j in range(i + 1, nb_tri + 1)]

def generate_pairs(nb_tri):
    num_workers = multiprocessing.cpu_count()-1
    chunk_size = max(1, nb_tri // num_workers)
    map_i_start=[i for i in range(1, nb_tri, chunk_size)]
    map_i_end=[min(i + chunk_size, nb_tri) for i in range(1, nb_tri, chunk_size)]


    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results=executor.map(generate_pairs_chunk,map_i_start,map_i_end,[nb_tri]*len(map_i_end))

    print('multi fini')
    pairs = np.array([item for sublist in results for item in sublist], dtype=int)
    return pairs

def save_array(filename, array, nb_tri):
    with open(filename, 'wb') as f:
        np.save(f, np.append(array, [[nb_tri, nb_tri]], axis=0))
        np.save(f, np.array([nb_tri], dtype=int))

def load_array(filename):
    with open(filename, 'rb') as f:
        array = np.load(f)
        saved_nb_tri = np.load(f)[0]
    return array, saved_nb_tri

def main(filename, nb_tri):
    if os.path.exists(filename):
        try:
            saved_array, saved_nb_tri = load_array(filename)
            if saved_nb_tri == nb_tri:
                #print("Fichier existant avec le bon nb_tri, chargement...")
                return saved_array[:-1]  # Retirer le dernier couple avant de retourner
        except Exception:
            print("Erreur de lecture du fichier, régénération...")
    
    print("Génération d'un nouveau tableau...")
    pairs = generate_pairs(nb_tri)
    print('Génération paire fini')
    save_array(filename, pairs, nb_tri)
    return pairs

if False:
    filename = r"C:\\CHALLENGE\\couple.npy"
    nb_tri = 19200  # À modifier selon le besoin
    result = main(filename, nb_tri)
    print(result)