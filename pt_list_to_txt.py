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

time_limit = 10 * 60

def pt_list_to_txt(pt_list, cyl_coord):
    """
    transforme une liste de points en liste de commandes pour le robot
    :param pt_list: liste contenant les cylindres dans l'ordre dans lequel on veut les parcourir
    :param cyl_coord: liste des cylindres avec leurs coordonnées en x, en y, et leur valeur en points (dimensions: n*3)
    :return: rien (écrit directement dans un fichier texte)
    """
    ray = 0.65  # 0.65 #somme des rayons du robot et d'un cylindre
    fuel = 2 * 10 ** 4
    global time_limit
    Vo = 1
    a_const = 0.0698
    b = 10 ** -2
    bo = 10 ** -2

    sortie = ""
    pos_actuelle = [0, 0, 0]  # [x,y,angle_deg]
    dir_act = [1, 0]
    trajet = [[pos_actuelle[0]],
              [pos_actuelle[1]],
              [-m.pi / 2]
              ]
    points_passes = []
    i = 0
    draw_list = []

    time = 0
    score = 0
    masse = 0
    stop_the_count = True
    while i < len(pt_list) or i < len(pt_list):
        # print("===========================\n",len(cyl_coord),pt_list[i],len(pt_list),i)
        pt = cyl_coord[pt_list[i] - 1]
        points_passes.append(pt_list[i])
        # on regarde si on passe par un cylindre invoulu ou pas:
        go_next = True

        for u in range(len(cyl_coord)):
            cyl = cyl_coord[u]
            if u not in points_passes and go_next:
                a = (pt[1] - pos_actuelle[1]) / (pt[0] - pos_actuelle[0])
                # calcul des coordonnées du point d'intersection de la droite départ-arrivée et sa perpendiculaire
                # passant par le centre du cylindre observé (point le plus proche du centre sur la droite)
                x_intersec = (a ** 2 * pt[0] + a * cyl[1] - a * pt[1] + cyl[0]) / (a ** 2 + 1)
                y_intersec = a * (x_intersec - pt[0]) + pt[1]

                if i == len(pt_list) - 1:
                    draw_list.append([
                        [(pos_actuelle[0], pos_actuelle[1]), a],
                        [(cyl[0], cyl[1]), -1 / a],
                        [x_intersec, y_intersec],
                        0
                    ])
                if pos_actuelle[0] < pt[0]:
                    interval_test = pos_actuelle[0] < cyl[0] < pt[0]
                else:
                    interval_test = pos_actuelle[0] > cyl[0] > pt[0]
                if m.sqrt((x_intersec - cyl[0]) ** 2 + (y_intersec - cyl[1]) ** 2) <= ray and interval_test:
                    # si il est trop proche du centre du cercle
                    # calcul des deux points de chaque coté du cylindre possibles
                    new_x_a = cyl[0] + (ray + 0.1) / m.sqrt(
                        1 + 1 / (a ** 2))  # <======================== 1/racine was 0.66/racine
                    new_y_a = -1 / a * (new_x_a - cyl[0]) + cyl[1]
                    new_x_b = cyl[0] - (ray + 0.1) / m.sqrt(
                        1 + 1 / (a ** 2))  # <======================== 1/racine was 0.66/racine
                    new_y_b = -1 / a * (new_x_b - cyl[0]) + cyl[1]
                    if new_y_b < new_y_a:  # détermine lequel des deux est au dessus et lequel est en dessous
                        new_pt_max = [new_x_a, new_y_a, 0]
                        new_pt_min = [new_x_b, new_y_b, 0]
                    else:
                        new_pt_max = [new_x_b, new_y_b, 0]
                        new_pt_min = [new_x_a, new_y_a, 0]
                    if a * (cyl[0] - pt[0]) + pt[1] < cyl[1]:
                        # si la trajectoire passe en dessous du centre, on prend le point en dessous du cylindre
                        cyl_coord.append(new_pt_min)
                        draw_list.append([new_pt_min, pt, 1])
                    else:
                        cyl_coord.append(new_pt_max)
                        draw_list.append([new_pt_max, pt, 1])
                    pt_list.insert(i, len(cyl_coord) - 1)
                    pt = cyl_coord[pt_list[i]]
                    points_passes.append(len(cyl_coord) - 1)
                    go_next = False
                    # print(i,len(pt_list))

        distance = m.sqrt((pt[0] - pos_actuelle[0]) ** 2 + (pt[1] - pos_actuelle[1]) ** 2)
        dir_obj = [pt[0] - pos_actuelle[0], pt[1] - pos_actuelle[1]]

        angle_rad = m.atan((dir_act[0] * dir_obj[1] - dir_act[1] * dir_obj[0]) /
                           (dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1]))
        if dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1] < 0:
            if angle_rad < 0:
                angle_rad += m.pi
            else:
                angle_rad -= m.pi
        dir_act = dir_obj
        angle_deg = m.degrees(angle_rad)

        pos_actuelle[0] = pt[0]
        pos_actuelle[1] = pt[1]
        pos_actuelle[2] = angle_deg

        sortie += f"TURN {pos_actuelle[2]}\nGO {distance}\n"

        # partie affichage dans le graph (affiche ce qu'on veut faire, pas ce qui est fait réellement)
        trajet[2].append(angle_rad)
        trajet[0].append(trajet[0][-1] + dir_act[0])
        trajet[1].append(trajet[1][-1] + dir_act[1])
        # ===============================
        # partie calcul score

        if time < time_limit and fuel > 0:
            score += pt[2]
            if pt[2] == 1:
                masse += 1
            if pt[2] == 2:
                masse += 2
            if pt[2] == 3:
                masse += 2
            vitesse = Vo * m.exp(-a_const * masse)
            time += distance / vitesse
            conso = masse * b + bo
            fuel -= conso * distance

        if (time >= time_limit or fuel <= 0) and stop_the_count:
            score -= pt[2]
            if time > time_limit:
                time = time_limit
            if fuel < 0:
                fuel = 0
            stop_the_count = False

        #print(pt, score, time)
        # ===============================
        i += 1

    sortie += "FINISH"
    with open("script.txt", 'w') as file:
        file.write(sortie)

    return trajet, draw_list, [score, time_limit-time, fuel]


# sortir une liste [points, temps_mis, carburant_utilisé]
"""
pt_list = [3, 4, 2, 5, 1, 6, 14, 20, 15, 16, 19, 18, 17, 13, 9, 10, 11, 12, 8, 7]
ray = 0.65
cyl_coord = input_txt_to_list(r"C:\CHALLENGE\donnees-map.txt")
x_list = []
y_list = []
for elt in cyl_coord:
    x_list.append(elt[0])
    y_list.append(elt[1])
trajet, draw_list, results = pt_list_to_txt(pt_list, cyl_coord)
print(results)
for i in range(len(x_list)):
    crcl = plt.Circle((x_list[i], y_list[i]), ray)
    plt.gca().add_patch(crcl)
plt.scatter(x_list, y_list)
plt.plot(trajet[0], trajet[1], color='r')
plt.axis('equal')
plt.show()
"""