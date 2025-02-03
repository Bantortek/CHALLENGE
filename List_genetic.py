import math
import numpy as np
import matplotlib.pyplot as plt
import random
import pt_list_to_txt as lt
import time
import multiprocessing
import concurrent.futures
import os
import liste_couple as lc

def Initialisation_gen(nb_par_gen):
# entrée : nombre d'élement par génération
# sortie : un dictionnaire de nb_par_gen de dérengement aléatoire des nombre de 1 à 20

    dico_final={}
    while len(dico_final)<nb_par_gen:
        list_ordoné = list(range(1, 21))
        random.shuffle(list_ordoné)
        dico_final[tuple(list_ordoné)]=0
        #print (list_ordoné)
    return dico_final


def Tri_dico(dico):
#entrée : dictionnaire des dérangement avec les scores
#sortie : dictionnaire des dérangement avec les scores trié selon l'ordre d'itération par le score
    dico=dict(sorted(dico.items() ,key=Trieur,reverse=True))
    return dico

def Trieur(list):
    #print(str(list[1]))
    score,temps,fuel=list[-1]
    resultat=score*(10**20)+round(temps,14)*(10**16)+fuel
    return resultat



def exec(key_chunk,list_parent,nb_process):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result=executor.map(Chunk_couple,key_chunk,[list_parent]*nb_process)
        f=[res for res in result]

    return f

def Crossover(dico,nb_par_gen,nb_tri,multiprocess=False,etape=0):
# entrée : dictionnaire des dérangement trié
# sortie : dictionnaire de dérangement de la prochaine génération (sans mutation)
    etape+=1
    #nb_process=multiprocessing.cpu_count()//2
    nb_process=(multiprocessing.cpu_count()//2)-1
    list_parent=[]
    dico_gen_suivante={}
    for key in dico:
        if len(list_parent)<nb_tri:
            list_parent.append(list(key))
    temps1=time.perf_counter()
    if len(dico)<nb_tri:
        nb_tri=len(dico)
    couples=Couple_random(nb_par_gen,nb_tri)
    #print('Taille couples',len(couples)==nb_tri*(nb_tri-1)/2 ,len(couples))
    temps2=time.perf_counter()
    #print('Temps couple = ',temps2-temps1)
    temps1=time.perf_counter()
    if etape==1:
        multiprocess=False
    
    if  not multiprocess:
        time40=time.perf_counter()
        for couple in couples:
            enfant1,enfant2=XXX(list_parent[int(couple[0])-1],list_parent[int(couple[1])-1])
            dico_gen_suivante[tuple(enfant1)]=0
            if len(dico_gen_suivante)==nb_par_gen:
                break
            dico_gen_suivante[tuple(enfant2)]=0
            if len(dico_gen_suivante)==nb_par_gen:
                break
        time50=time.perf_counter()
    #print('\nAvant debut multi')


    if multiprocess:
        if etape==1:
            nb_de_etape=1
        elif etape==2:
            nb_de_etape=1
        elif etape==3:
            nb_de_etape=1
        else:
            nb_de_etape=1
        chunk_couple_faire=np.array_split(couples, nb_de_etape)
        final_result = {}





        def multi_chunk_couple(morceau_chunk_c,nb_division=1):
            morceau_chunk_c_div=np.array_split(morceau_chunk_c,nb_division)

            key_chunks =[]
            for morceau in morceau_chunk_c_div:
                key_chunks.append(np.array_split(morceau, nb_process))

            

            with concurrent.futures.ProcessPoolExecutor() as pool:
                result_pool=pool.map(exec,key_chunks,[list_parent]*len(key_chunks),[nb_process]*len(key_chunks))

            for res in result_pool:
                for res1 in res:
                    final_result.update(res1)
                    if len(final_result)>=nb_par_gen:
                        break
                if len(final_result)>=nb_par_gen:
                        break

            #print("Multi fini etape = ",k+1)
            #print('Debut final')
            return    
            
            
        #print("Multi fini\n")


        for chunk in chunk_couple_faire:
            multi_chunk_couple(chunk,max((multiprocessing.cpu_count()//16),1))
            if len(final_result)>=nb_par_gen:
                break
        for key in final_result:
            dico_gen_suivante[key]=0
            if len(dico_gen_suivante)==nb_par_gen:
                break



    return dico_gen_suivante


def Chunk_couple(list_chunk_couple,list_parent):
    dico={}
    for couple in list_chunk_couple:
        enfant1,enfant2=XXX(list_parent[int(couple[0])-1],list_parent[int(couple[1])-1])
        dico[tuple(enfant1)]=0
        dico[tuple(enfant2)]=0
    return dico



def Couple_random(nb_par_gen, nb_tri):
    filename=r"C:\\CHALLENGE\\Fichier_couple\\couple"+str(nb_tri)+".npy"
# entrée : nombre d'apartition d'un nombre possible
# sortie : liste de nb_gen//2 couple de nombre (de 1 à nb_tri compris) sans doublon (ex (1,2) peut être dedans mais pas (2,1))
    list_couple=lc.main(filename,nb_tri)

        
    
    return list_couple


def XXX(parent1b,parent2b):
# entrée : liste des parent (parent qui est une liste de dérangement) / couple d'entier des numéros des parents à associer
# sortie : 2 liste enfants 
    parent1=parent1b.copy()
    parent2=parent2b.copy()
    enfant1=parent1[:len(parent1)//2]
    enfant2=parent2[:len(parent2)//2]


    for nb in enfant1:
        if nb in parent2:
            parent2.remove(nb)
    enfant1.extend(parent2)

    for nb in enfant2:
        if nb in parent1:
            parent1.remove(nb)
    enfant2.extend(parent1)


    return enfant1,enfant2




def Mutation(dico_gen_suiv,tx_mutation,nb_de_mutation):
# entreé : dico de la génération suivante / taux de muté dans la population en % / nb d'échange dans un dérangement donné
# Sortie : dico muté
    list_gen=[]
    for key in dico_gen_suiv:
        list_gen.append(list(key))
    nb_a_mute=int(tx_mutation*len(list_gen)/100)
    list_element_mute=[]




    start_ls_a_mute=time.perf_counter()
    list_a_mute=[i for i in range (len(list_gen)-1)]
    random.shuffle(list_a_mute)
    list_a_mute=list_a_mute[:nb_a_mute]
    end_ls_a_mute=time.perf_counter()

    '''
    print('Temps crea list_a_mute methode 2 = ',end_ls_a_mute-start_ls_a_mute)
    print('Test len lis_a_mute',len(list_a_mute)==len(list_a_mute1))
    print(list_a_mute)
    print(list_a_mute1)
    '''

    
        
    start_ls_e_mute=time.perf_counter()
    while len(list_element_mute)<nb_a_mute:
        list_couple=[]
        while len(list_couple)<2*nb_de_mutation:
            nb=random.randint(0,19)
            if nb not in list_couple:
                list_couple.append(nb)
        list_element_mute.append(list_couple)
    end_ls_e_mute=time.perf_counter()
    #print('Temps crea list_element_mute = ',end_ls_e_mute-start_ls_e_mute)

    start_mutation=time.perf_counter()
    for i in range (len(list_a_mute)):
        a_mute=list_gen[list_a_mute[i]].copy()
        k=1
        for j in range (len(list_element_mute[i])):
            if k==1:
                nb1=a_mute[list_element_mute[i][j]]
                nb2=a_mute[list_element_mute[i][j+1]]
                a_mute.pop(list_element_mute[i][j])
                a_mute.insert(list_element_mute[i][j],nb2)

                a_mute.pop(list_element_mute[i][j+1])
                a_mute.insert(list_element_mute[i][j+1],nb1)
            k*=-1
        list_gen[list_a_mute[i]]=a_mute
    end_mutation=time.perf_counter()
    #print('Temps Mutation = ',end_mutation-start_mutation)

    star_dico=time.perf_counter()
    dico_mute={}
    for i in list_gen:
        dico_mute[tuple(i)]=0
    end_dico=time.perf_counter()
    #print('Temps creation dico = ',end_dico-star_dico)

    return dico_mute



def Chunk_score (list_chunk,list_pt_map,script=False):
    dico_result={}
    for chunk in list_chunk:
        dico_result[tuple(chunk)]=lt.pt_list_to_txt(list(chunk),list_pt_map,script)
    return dico_result



liste_score=[]
def Solution(list_pt_map,nb_gen_max=10,nb_par_gen=1000,nb_tri=100,tx_mutation=75,nb_de_mutation=1,multiprocess=False):
# entrée : matrice 20X3 qui représente la map + parametre de la selection
# sortie : liste de len 20 qui est la meilleur solution après selection naturelle
    boa=[]
    test=False
    if (nb_tri*nb_tri-1)<nb_par_gen:
        return "Erreur nb_tri est trop petit"
    if nb_par_gen%nb_tri!=0:
        return "Erreur le nb_par_gen doit être multiple de nb_tri"
    if nb_tri%2!=0:
        return "Erreur nb_tri doit être multiple de 2"
    dico_derangement=Initialisation_gen(nb_par_gen)
    list_pt_map_archive = list_pt_map.copy()
    print('=========================================')




    if multiprocess and test:
        print(int(multiprocessing.cpu_count()*1.5/2))
        temp=np.inf
        for nb_process_it in range(int(multiprocessing.cpu_count()/3),int(multiprocessing.cpu_count()*1.5/2)):
            time10=time.perf_counter()
            dico_temp=dico_derangement.copy()

            keys=list(dico_temp.keys())
            key_chunk_1 = np.array_split(keys, nb_process_it)
            key_chunk=[]

            for k in range (len(key_chunk_1)):
                key_chunk.append([])
                for l in range (len(key_chunk_1[k])):
                    key_chunk[-1].append(list(key_chunk_1[k][l]))

            with concurrent.futures.ProcessPoolExecutor(max_workers=nb_process_it) as pool:
                results = pool.map(Chunk_score, [list(chunk) for chunk in key_chunk],[list_pt_map]*nb_process_it)
                

            final_result = {}
            
            for res in results:
                final_result.update(res)



            time20=time.perf_counter()
            print('Test nombre process = ',nb_process_it,'Temps nécessaire = ',time20-time10,'s')
            if time20-time10-temp>=0:
                break
            nb_process=nb_process_it
            temp=time20-time10
        print(nb_process,temp)
    else:
        nb_process=multiprocessing.cpu_count()//2-1



    for j in range (nb_gen_max):
        print('Génération = ',j+1)
        if multiprocess:
            '''
            if j>nb_gen_max//8 and nb_process+1>multiprocessing.cpu_count()//2:
                nb_process=nb_process//2
            #if j>nb_gen_max//4 and nb_process>multiprocessing.cpu_count()//4:
                #nb_process=nb_process//2
            if j>nb_gen_max//2 and nb_process+1>multiprocessing.cpu_count()//4:
                nb_process=nb_process//2
            '''
        time100=time.perf_counter()
        if TEMPS_INDICATIF:

            time10=time.perf_counter()
        def Scorring(dico_derangement,list_pt_map,nb_process=1,multiprocess=False):
# Singleprocess
##############################################################################################################
    
            if not multiprocess :
                

                for key in dico_derangement:
                    #print(key)
                    list_pt_map = list_pt_map_archive.copy()
                    dico_derangement[key]=lt.pt_list_to_txt(list(key), list_pt_map,script=False)
                    #print('OK')


##############################################################################################################

# Multiprocess
##############################################################################################################
            if multiprocess:



                dico_temp=dico_derangement.copy()

                keys=list(dico_temp.keys())
                key_chunk_1 = np.array_split(keys, nb_process)
                key_chunk=[]

                for k in range (len(key_chunk_1)):
                    key_chunk.append([])
                    for l in range (len(key_chunk_1[k])):
                        key_chunk[-1].append(list(key_chunk_1[k][l]))

                with concurrent.futures.ProcessPoolExecutor(max_workers=nb_process) as pool:
                    results = pool.map(Chunk_score, [list(chunk) for chunk in key_chunk],[list_pt_map]*nb_process)

                final_result = {}
            
                for res in results:
                    #print(res)
                    final_result.update(res)
                dico_derangement=final_result.copy()
            return dico_derangement
        dico_derangement=Scorring(dico_derangement,list_pt_map,nb_process,multiprocess)
        if TEMPS_INDICATIF:
            time20=time.perf_counter()
            print('Nombre de process = ',nb_process)
            print('Temps score     = ',float(str(time20-time10)[:5]),'Taille dico = ',len(dico_derangement))
                
        #print (dico_derangement)


##############################################################################################################


        if TEMPS_INDICATIF:
            time10=time.perf_counter()
        dico_trier=Tri_dico(dico_derangement)
        if TEMPS_INDICATIF:    
            time20=time.perf_counter()
            print('Temps tri       = ',float(str(time20-time10)[:5]),'Taille dico = ',len(dico_trier))
        i=0 
        for key in dico_trier:
            if i==0:
                solution = list(key)
                score=dico_trier[tuple(solution)]
            i = -1
        boa.append([solution,score])
        boa=sorted(boa,key=Trieur,reverse=True)
        if j!=0:
            boa.pop(-1)


        if TEMPS_INDICATIF:
            time10=time.perf_counter()
        dico_gen_suiv=Crossover(dico_trier,nb_par_gen,nb_tri,multiprocess,j)
        if TEMPS_INDICATIF:    
            time20=time.perf_counter()
            print('Temps crossover = ',float(str(time20-time10)[:5]),'Taille dico = ',len(dico_gen_suiv))
        if TEMPS_INDICATIF:
            time10=time.perf_counter()

        
        if TEMPS_INDICATIF:
            time10=time.perf_counter()
        dico_gen_mute=Mutation(dico_gen_suiv,tx_mutation,nb_de_mutation)
        if TEMPS_INDICATIF:
            time20=time.perf_counter()
            print('Temps mutation  = ',float(str(time20-time10)[:5]),'Taille dico = ',len(dico_gen_mute))

        
        if TEMPS_INDICATIF:
            time10=time.perf_counter()
        dico_derangement=dico_gen_mute
        if TEMPS_INDICATIF:
            time20=time.perf_counter()
            #print('Temps copy = ',time20-time10)
        time200=time.perf_counter()

        print('\nScore boa pt = ',boa[0][1][0],'Temps restant = ',boa[0][1][1])
        print("Temps par gen = ", float(str(time200-time100)[:5]))
        print('Tx de completion = ',(100*(j+1))/nb_gen_max,'%')
        


        global liste_score
        liste_score.append(boa[0][1][1])
        print('=========================================')


    dico_trier=Scorring(dico_gen_mute,list_pt_map,nb_process,multiprocess)
    i=0
    for key in dico_trier:
        if i ==0:
            solution = list(key)
            score=dico_trier[tuple(solution)]
            break
    boa.append([solution,score])
    boa=sorted(boa,key=Trieur,reverse=True)
    boa.pop(-1)

    #print(dico_trier.values())
    score[1]=boa[0][1][1]
    return boa



def Trieur2(liste):
    print(liste[-1])
    a=Trieur(liste[-1])
    return a
if __name__ == "__main__":
    TEMPS_INDICATIF=True
    '''
    ray = 0.65
    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-1.txt")
    start=time.perf_counter()
    pt_list =Solution(cyl_coord,10,48000,1200,10,4,multiprocess=True)[0]
    end=time.perf_counter()
    print(pt_list)
    print("Temps d'execution de Solution = ",end-start)
    x_list = []
    y_list = []
    for elt in cyl_coord:
        x_list.append(elt[0])
        y_list.append(elt[1])
    trajet, draw_list, results = lt.pt_list_to_txt(pt_list, cyl_coord)
    print(results)
    for i in range(len(x_list)):
        crcl = plt.Circle((x_list[i], y_list[i]), ray)
        plt.gca().add_patch(crcl)
    plt.scatter(x_list, y_list)
    plt.plot(trajet[0], trajet[1], color='r')
    plt.axis('equal')
    plt.figure()
    liste_nb=[]
    for i in range (1,len(liste_score)+1):
        liste_nb.append(i)
    plt.plot(liste_nb,liste_score)
    plt.show()
    '''
    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-1.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,2,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,1)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-2.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,2)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-3.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,3)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-4.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,4)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-5.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,5)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-6.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,6)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-7.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,7)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-8.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,8)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-9.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,9)

    cyl_coord = lt.input_txt_to_list(r"C:\\CHALLENGE\\donnees-map-10.txt")
    best=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
    for i in range(2):
        a=Solution(cyl_coord,50,48000,1200,10,4,multiprocess=True)
        best.append(a[0])
        best=sorted(best,key=Trieur,reverse=True)
        best.pop(-1)
    b=lt.pt_list_to_txt(best[0][0],cyl_coord,True,10)