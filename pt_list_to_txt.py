import math as m


def pt_list_to_txt(pt_list, cyl_coord):
    """
    transforme une liste de points en liste de commandes pour le robot
    :param pt_list: liste contenant les cylindres dans l'ordre dans lequel on veut les parcourir
    :param cyl_coord: liste des cylindres avec leurs coordonnées en x, en y, et leur valeur en points (dimensions: n*3)
    :return: rien (écrit directement dans un fichier texte)
    """
    sortie = ""
    pos_actuelle = [0, 0, 0]  # [x,y,angle]
    for pt in pt_list:
        distance = m.sqrt((cyl_coord[pt][0] - pos_actuelle[0]) ** 2 + (cyl_coord[pt][1] - pos_actuelle[1]) ** 2)
        angle_absolu = m.acos((cyl_coord[pt][0] - pos_actuelle[0]) / distance)
        angle = round((angle_absolu - pos_actuelle[2])*180/m.pi)
        sortie += f"TURN {angle}\nGO {distance}\n"
    sortie += "FINISH"
    with open("script.txt", 'w') as file:
        file.write(sortie)


def input_txt_to_list(txt_file):
    with open(txt_file) as file:
        entree = file.read()
    entree = entree.split("\n")
    sortie = []
    for elt in entree:
        if elt:
            sortie.append([float(x) for x in elt.split(" ") if x])
    return sortie


pt_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

cyl_coord = input_txt_to_list("donnees-map.txt")

pt_list_to_txt(pt_list, cyl_coord)
