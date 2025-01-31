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


def pt_list_to_txt(pt_list, cyl_coord,script = True):
    """
    transforme une liste de points en liste de commandes pour le robot
    :param pt_list: liste contenant les cylindres dans l'ordre dans lequel on veut les parcourir
    :param cyl_coord: liste des cylindres avec leurs coordonnées en x, en y, et leur valeur en points (dimensions: n*3)
    :return: rien (écrit directement dans un fichier texte)
    """
    ray = 1.9357731992148293  # 0.65 #somme des rayons du robot et d'un cylindre
    fuel = 2 * 10 ** 4
    global time_limit
    Vo = 1
    a_const = 0.0698
    b = 3
    bo = 10 ** 2

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
    while i < len(pt_list):
        # print("===========================\n", len(cyl_coord), pt_list[i], len(pt_list), i)
        # print(pt_list)
        # print(pos_actuelle)
        pt = cyl_coord[pt_list[i] - 1]
        # on regarde si on passe par un cylindre invoulu ou pas:
        go_next = True

        points_intercep = []
        for u in range(len(cyl_coord)):
            cyl = cyl_coord[u]
            if (u + 1) not in points_passes and go_next and (u + 1) != pt_list[i]:
                a = (pt[1] - pos_actuelle[1]) / (pt[0] - pos_actuelle[0])
                # calcul des coordonnées du point d'intersection de la droite départ-arrivée et sa perpendiculaire
                # passant par le centre du cylindre observé (point le plus proche du centre sur la droite)
                x_intersec = (a ** 2 * pt[0] + a * cyl[1] - a * pt[1] + cyl[0]) / (a ** 2 + 1)
                y_intersec = a * (x_intersec - pt[0]) + pt[1]

                interval_test = min(pos_actuelle[0], pt[0]) < x_intersec < max(pos_actuelle[0], pt[0]) and min(
                    pos_actuelle[1], pt[1]) < y_intersec < max(pos_actuelle[1], pt[1])

                #print(u + 1, m.sqrt((x_intersec - cyl[0]) ** 2 + (y_intersec - cyl[1]) ** 2) <= ray, interval_test)
                if m.sqrt((x_intersec - cyl[0]) ** 2 + (y_intersec - cyl[1]) ** 2) <= ray and interval_test:
                    #print(u + 1)
                    # si il est trop proche du centre du cercle
                    # calcul des deux points d'intersection du trajet et du cylindre
                    big_A = 1 + a ** 2
                    big_B = -2 * cyl[0] - 2 * a ** 2 * pt[0] + 2 * a * pt[1] - 2 * a * cyl[1]
                    big_C = cyl[0] ** 2 + a ** 2 * pt[0] ** 2 + 2 * a * (-pt[1] * pt[0] + cyl[1] * pt[0]) + (
                            pt[1] - cyl[1]) ** 2 - ray ** 2
                    delta = big_B ** 2 - 4 * big_A * big_C
                    new_x_a = (-big_B + m.sqrt(delta)) / (2 * big_A)
                    new_y_a = a * (new_x_a - pt[0]) + pt[1]
                    new_x_b = (-big_B - m.sqrt(delta)) / (2 * big_A)
                    new_y_b = a * (new_x_b - pt[0]) + pt[1]

                    dist_a = m.sqrt((new_x_a - pos_actuelle[0]) ** 2 + (new_y_a - pos_actuelle[1]) ** 2)
                    dist_b = m.sqrt((new_x_b - pos_actuelle[0]) ** 2 + (new_y_b - pos_actuelle[1]) ** 2)

                    if dist_a < dist_b:
                        points_intercep.append([u + 1, [new_x_a, new_y_a, cyl[2]], dist_a])
                    else:
                        points_intercep.append([u + 1, [new_x_b, new_y_b, cyl[2]], dist_b])

        if points_intercep:
            points_intercep = sorted(points_intercep, key=lambda list: list[2])
            #print(points_intercep)
            best_point = points_intercep[0]

            pt_list.insert(i, len(cyl_coord) + 1)
            pt_list.remove(best_point[0])
            cyl_coord.append(best_point[1])
            pt = cyl_coord[pt_list[i] - 1]
            points_passes.append(best_point[0])
            # print(i,len(pt_list))
        #print(points_passes)

        distance = m.sqrt((pt[0] - pos_actuelle[0]) ** 2 + (pt[1] - pos_actuelle[1]) ** 2)
        dir_obj = [pt[0] - pos_actuelle[0], pt[1] - pos_actuelle[1]]
        if dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1] == 0:
            angle_rad = 0
        else:
            angle_rad = m.atan((dir_act[0] * dir_obj[1] - dir_act[1] * dir_obj[0]) /
                               (dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1]))
        if dir_act[0] * dir_obj[0] + dir_act[1] * dir_obj[1] < 0:
            if angle_rad < 0:
                angle_rad += m.pi
            else:
                angle_rad -= m.pi
        dir_act = dir_obj
        pres = 15
        angle_deg = m.degrees(round(angle_rad, pres))

        pos_actuelle[0] = pt[0]
        pos_actuelle[1] = pt[1]
        pos_actuelle[2] = angle_deg*0.99

        if pos_actuelle[2] == 0:
            sortie += f"GO {distance*0.99}\n"
        else:
            sortie += f"TURN {pos_actuelle[2]}\nGO {distance}\n"
        # partie affichage dans le graph (affiche ce qu'on veut faire, pas ce qui est fait réellement)
        trajet[2].append(angle_rad)
        trajet[0].append(trajet[0][-1] + dir_act[0])
        trajet[1].append(trajet[1][-1] + dir_act[1])
        # ===============================
        # partie calcul score

        if time < time_limit and fuel > 0:
            if pt_list[i] not in points_passes:
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

        # print(pt, score, time)
        # ===============================
        points_passes.append(pt_list[i])
        i += 1
    # print(points_passes)
    if script:
        sortie += "FINISH"
        with open("script.txt", 'w') as file:
            file.write(sortie)

    return trajet, draw_list, [score, time_limit - time, fuel]


# sortir une liste [points, temps_mis, carburant_utilisé]

# pt_list = [13, 17, 18, 19, 20, 12, 15, 10, 6, 9, 1, 16, 5, 14, 2, 3, 4, 8, 7, 11]
#
# ray = 1.9357731992148293
# cyl_coord = input_txt_to_list(r"C:\CHALLENGE\donnees-map.txt")
# x_list = []
# y_list = []
# for elt in cyl_coord:
#     x_list.append(elt[0])
#     y_list.append(elt[1])
# trajet, draw_list, results = pt_list_to_txt(pt_list, cyl_coord)
# print(results)
# for i in range(len(x_list)):
#     crcl = plt.Circle((x_list[i], y_list[i]), ray)
#     plt.gca().add_patch(crcl)
# print(draw_list)
# for elt in draw_list:
#     plt.scatter([elt[0]], [elt[1]])
# # plt.scatter(x_list, y_list)
# plt.plot(trajet[0], trajet[1], color='r')
# plt.axis('equal')
# plt.show()
