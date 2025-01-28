import math as np
#import matplotlib.pyplot as plt
import random

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
    sorted(dico ,key= lambda list: list[1])
    return dico


def Crossover(dico,nb_par_gen,nb_tri):
# entrée : dictionnaire des dérangement trié
# sortie : dictionnaire de dérangement de la prochaine génération (sans mutation)
    list_parent=[]
    for key,values in dico:
        if len(list)<nb_tri:
            list_parent.append(list(key))
    couples=Couple_random(nb_par_gen,nb_tri)
    for couple in couples:
        enfant1,enfant2=XXX(list_parent,couple)

    
    
    return


def Couple_random(nb_par_gen, nb_tri):
# entrée : nombre d'apartition d'un nombre possible
# sortie : liste de nb_gen//2 couple de nombre sans doublon (ex (1,2) peut être dedans mais pas (2,1))
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
    


def Solution(list_pt_map,nb_gen_max=10,nb_par_gen=1000,nb_tri=10):
# entrée : matrice 20X3 qui représente la map + parametre de la selection
# sortie : liste de len 20 qui est la meilleur solution après selection naturelle
    if nb_par_gen%nb_tri!=0:
        return "Erreur le nb_par_gen doit être multiple de nb_tri"
    if nb_tri%2!=0:
        return "Erreur nb_tri doit être multiple de 2"
    dico_derangement=Initialisation_gen(nb_par_gen)
    for i in range (nb_gen_max):
        ## calcule score
        dico_derangement=Tri_dico(dico_derangement)
        dico_derangement=Crossover(dico_derangement,nb_par_gen,nb_tri)
    return
