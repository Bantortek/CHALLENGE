import math as np
import matplotlib.pyplot as plt
import random
import pt_list_to_txt as lt
import time

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
    score,temps,fuel=list[1]
    resultat=score*(10**20)+int(temps)*(10**10)+fuel
    return resultat

def Crossover(dico,nb_par_gen,nb_tri):
# entrée : dictionnaire des dérangement trié
# sortie : dictionnaire de dérangement de la prochaine génération (sans mutation)
    list_parent=[]
    dico_gen_suivante={}
    for key in dico:
        if len(list_parent)<nb_tri:
            list_parent.append(list(key))
    couples=Couple_random(nb_par_gen,nb_tri)
    for couple in couples:
        enfant1,enfant2=XXX(list_parent,couple)
        dico_gen_suivante[tuple(enfant1)]=0
        dico_gen_suivante[tuple(enfant2)]=0
    return dico_gen_suivante


def Couple_random(nb_par_gen, nb_tri):
# entrée : nombre d'apartition d'un nombre possible
# sortie : liste de nb_gen//2 couple de nombre (de 1 à nb_tri compris) sans doublon (ex (1,2) peut être dedans mais pas (2,1))
    list_couple=[]
    dico_apparition={}
    nb_apparition=nb_par_gen//nb_tri
    for i in range (1,nb_tri+1):
        dico_apparition[i]=0
    while len(list_couple)<(nb_par_gen//2):
        nb_valide=True
        while nb_valide:
            nb1=random.randint(1,nb_tri)
            if dico_apparition[nb1]<nb_apparition:
                nb_valide=False
        nb_valide=True
        while nb_valide:
            nb2=random.randint(1,nb_tri)
            if dico_apparition[nb2]<nb_apparition and nb2!=nb1:
                nb_valide=False
        couple=[nb1,nb2]
        couple=sorted(couple)
        if couple not in list_couple:
            list_couple.append(couple)
    return list_couple


def XXX(list_parent,couple):
# entrée : liste des parent (parent qui est une liste de dérangement) / couple d'entier des numéros des parents à associer
# sortie : 2 liste enfants 
    enfant1=[]
    enfant2=[]
    parent1=list_parent[couple[0]-1]
    parent2=list_parent[couple[1]-1]
    for i in range (len(parent1)//2):
        enfant1.append(parent1[i])
        enfant2.append(parent2[i])
    for i in range (len(parent1)//2):
        nb_found=True
        j=-1
        while nb_found:
            j+=1
            if parent2[-1-j] not in enfant1:
                nb_found=False
        if  i==0:
            enfant1.append(parent2[-1-j])
        else:     
            enfant1.insert(-i,parent2[-1-j])
        nb_found=True
        j=-1
        while nb_found:
            j+=1
            if parent1[-1-j] not in enfant2:
                nb_found=False
        if i==0:
            enfant2.append(parent1[-1-j])
        else:
            enfant2.insert(-i,parent1[-1-j])
    return enfant1, enfant2




def Mutation(dico_gen_suiv,tx_mutation,nb_de_mutation):
# entreé : dico de la génération suivante / taux de muté dans la population en % / nb d'échange dans un dérangement donné
# Sortie : dico muté
    list_gen=[]
    for key in dico_gen_suiv:
        list_gen.append(list(key))
    nb_a_mute=int(tx_mutation*len(list_gen)/100)
    list_a_mute=[]
    list_element_mute=[]
    while len(list_a_mute)<nb_a_mute:
        nb=random.randint(0,len(list_gen)-1)
        if nb not in list_a_mute:
            list_a_mute.append(nb)
        

    while len(list_element_mute)<nb_a_mute:
        list_couple=[]
        while len(list_couple)<2*nb_de_mutation:
            nb=random.randint(0,19)
            if nb not in list_couple:
                list_couple.append(nb)
        list_element_mute.append(list_couple)

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
    
    dico_mute={}
    for i in list_gen:
        dico_mute[tuple(i)]=0

    return dico_mute


TEMPS_INDICATIF=False
liste_score=[]
def Solution(list_pt_map,nb_gen_max=10,nb_par_gen=1000,nb_tri=100,tx_mutation=75,nb_de_mutation=1):
# entrée : matrice 20X3 qui représente la map + parametre de la selection
# sortie : liste de len 20 qui est la meilleur solution après selection naturelle

    time1=time.time()
    if (nb_tri*nb_tri-1)<nb_par_gen:
        return "Erreur nb_tri est trop petit"
    if nb_par_gen%nb_tri!=0:
        return "Erreur le nb_par_gen doit être multiple de nb_tri"
    if nb_tri%2!=0:
        return "Erreur nb_tri doit être multiple de 2"
    dico_derangement=Initialisation_gen(nb_par_gen)
    list_pt_map_archive = list_pt_map.copy()
    print('=========================================')
    for j in range (nb_gen_max):
        time100=time.time()
        time10=time.time()
        for key in dico_derangement:
            #print(key)
            list_pt_map = list_pt_map_archive.copy()
            dico_derangement[key]=lt.pt_list_to_txt(list(key), list_pt_map)[2]
            #print('OK')
        time20=time.time()
        if TEMPS_INDICATIF:
            print('Temps score = ',time20-time10)

        time10=time.time()
        dico_trier=Tri_dico(dico_derangement)
        time20=time.time()
        if TEMPS_INDICATIF:
            print('Temps tri = ',time20-time10)

        time10=time.time()
        dico_gen_suiv=Crossover(dico_trier,nb_par_gen,nb_tri)
        time20=time.time()
        if TEMPS_INDICATIF:
            print('Temps crossover = ',time20-time10)

        time10=time.time()
        dico_gen_mute=Mutation(dico_gen_suiv,tx_mutation,nb_de_mutation)
        time20=time.time()
        if TEMPS_INDICATIF:
            print('Temps mutation = ',time20-time10)
        

        time10=time.time()
        dico_derangement=dico_gen_mute
        time20=time.time()
        if TEMPS_INDICATIF:
            print('Temps copy = ',time20-time10)
        time200=time.time()
        if TEMPS_INDICATIF:
            print("Temps par gen = ", time200-time100,'\n')
        print('Tx de completion = ',(100*(j+1))/nb_gen_max,'%')
        i=0
        for key in dico_trier:
            if i ==0:
                solution = list(key)
                score=dico_trier[tuple(solution)]
            i = -1
        score[1]=abs(score[1]-lt.time_limit)
        print('Score = ',score)
        global liste_score
        liste_score.append(score[1])
        print('=========================================')
    for key in dico_gen_suiv:
        list_pt_map = list_pt_map_archive.copy()
        dico_gen_suiv[key]=lt.pt_list_to_txt(list(key), list_pt_map)[2]


    dico_trier=Tri_dico(dico_gen_suiv)
    i=0
    for key in dico_trier:
        #print(key)
        if i ==0:
            solution = list(key)
            score=dico_trier[tuple(solution)]
        i = -1
    time2=time.time()
    print("temps d'execution = ", time2-time1)

    #print(dico_trier.values())
    score[1]=abs(score[1]-lt.time_limit)
    return solution , score



'''
list_pt_map=lt.input_txt_to_list(r"C:\CHALLENGE\donnees-map.txt")
# print(list_pt_map)
list_solution=Solution(list_pt_map,500,1000,100,25,4)
print(list_solution)
'''

ray = 0.65
cyl_coord = lt.input_txt_to_list(r"C:\CHALLENGE\donnees-map.txt")
pt_list =Solution(cyl_coord,750,6000,80,50,1)[0]
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
