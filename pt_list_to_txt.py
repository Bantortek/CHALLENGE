import math as m
import time
import matplotlib.pyplot as plt

def input_txt_to_list(txt_file):
    with open(txt_file) as file:
        entree = file.read()
    entree = entree.split("\n")
    sortie = []
    for elt in entree:
        if elt:
            sortie.append([float(x) for x in elt.split(" ") if x])
    return sortie

def pt_list_to_txt(pt_list, cyl_coord):
    """
    transforme une liste de points en liste de commandes pour le robot
    :param pt_list: liste contenant les cylindres dans l'ordre dans lequel on veut les parcourir
    :param cyl_coord: liste des cylindres avec leurs coordonnées en x, en y, et leur valeur en points (dimensions: n*3)
    :return: rien (écrit directement dans un fichier texte)
    """
    sortie = ""
    pos_actuelle = [0, 0, 0]  # [x,y,angle_deg]
    dir_act = [1, 0]
    trajet = [[pos_actuelle[0]],
              [pos_actuelle[1]],
              [-m.pi / 2]
              ]
    for pt in pt_list:
        distance = m.sqrt((cyl_coord[pt][0] - pos_actuelle[0]) ** 2 + (cyl_coord[pt][1] - pos_actuelle[1]) ** 2)
        dir_obj = [cyl_coord[pt][0] - pos_actuelle[0], cyl_coord[pt][1] - pos_actuelle[1]]

        angle_rad = m.atan((dir_act[0] * dir_obj[1] - dir_act[1] * dir_obj[0]) /
                              (dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1]))
        if dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1] < 0:
            if angle_rad < 0:
                angle_rad += m.pi
            else:
                angle_rad -= m.pi
        dir_act = dir_obj
        angle_deg = m.degrees(angle_rad)

        pos_actuelle[0] = cyl_coord[pt][0]
        pos_actuelle[1] = cyl_coord[pt][1]
        pos_actuelle[2] = angle_deg

        sortie += f"TURN {pos_actuelle[2]}\nGO {distance}\n"

        # partie affichage dans le graph (affiche ce qu'on veut faire, pas ce qui est fait réellement)
        trajet[2].append(angle_rad)
        trajet[0].append(trajet[0][-1] + dir_act[0])
        trajet[1].append(trajet[1][-1] + dir_act[1])
        # ===============================

    sortie += "FINISH"
    with open("script.txt", 'w') as file:
        file.write(sortie)
    return trajet


# sortir une liste [points, temps_mis, carburant_utilisé]


pt_list = [4, 19]

cyl_coord = input_txt_to_list("donnees-map.txt")
x_list = []
y_list = []
for elt in cyl_coord:
    x_list.append(elt[0])
    y_list.append(elt[1])
trajet = pt_list_to_txt(pt_list, cyl_coord)

plt.scatter(x_list, y_list)
for i in range(len(x_list)):
    crcl = plt.Circle((x_list[i], y_list[i]), 0.65) # cylindres d'1m de diamètre et robot de 0.3m de diamètre
    plt.gca().add_patch(crcl)
plt.plot(trajet[0], trajet[1])
plt.axis('equal')
plt.show()
