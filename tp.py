'''
@auteur(e)s     Bradley Colas et Jean Luc Adrien
@matricules     e2353376 et e2368878
@date           19-05-2024
'''

class DonneesGeo:
    def __init__(self, ville, pays, latitude, longitude):
        self.ville = str(ville)
        self.pays = str(pays)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f"{self.ville}, {self.pays}, {self.latitude}, {self.longitude}"


import csv
def lireDonneesCsv(nomFichier):
    donnees_geo = [] #liste des objets
    with open(nomFichier, mode='r', encoding='utf-8') as fichier_csv: #Mode lecture du fichier csv
        lecteur_csv = csv.reader(fichier_csv)
        next(lecteur_csv)  # Ignorer la première ligne (en-tête)
        for ligne in lecteur_csv:
            print(ligne) #Affichage de chaque ville du fichier csv
            if len(ligne) == 4:  # pour s'assurer que la ligne contient exactement 4 éléments
                ville, pays, latitude, longitude = ligne #Separation de chaque element
                latitude_float = float(latitude)
                longitude_float = float(longitude)
                donnees_geo.append(DonneesGeo(ville, pays, latitude_float, longitude_float)) #Creation de l'objet pour chaque ville
    return donnees_geo


import json
def ecrireDonneesJson(nomFichier, listeObjDonneesGeo):
    data = [] #liste contenant les dictionnaires de ville
    for donnee in listeObjDonneesGeo: #Ajout de chaque objet ville en forme de dictionnaire a la liste data
        data.append({
            'ville': donnee.ville,
            'pays': donnee.pays,
            'latitude': donnee.latitude,
            'longitude': donnee.longitude
        })

    with open(nomFichier, 'w') as f: #On les ajoute dans le fichier en mode ecriture
        json.dump(data, f)

import math
def trouverDistanceMin(nomFichier):

    with open(nomFichier, 'r') as f: #Lecture du fichier JSON (Ville en dictionnaire)
        dico_villes = json.load(f)

    liste_calcul_distance = [] #liste contenant les calculs de chaque ville

    for i in range(len(dico_villes)):  # Parcourt les villes (dictionnaire) du fichier JSON, donc les villes actuelles
        for j in range(i + 1,len(dico_villes)):  # Parcourt les villes restantes pour les comparer avec la ville actuelle
            ville_1 = dico_villes[i]["ville"]
            pays_1 = dico_villes[i]["pays"]
            latitude_1 = dico_villes[i]["latitude"]
            longitude_1 = dico_villes[i]["longitude"]

            ville_2 = dico_villes[j]["ville"]
            pays_2 = dico_villes[j]["pays"]
            latitude_2 = dico_villes[j]["latitude"]
            longitude_2 = dico_villes[j]["longitude"]

            # Calcul de distance (formule)
            rayon = 6371

            #Conversion en radian de ville 1 et ville 2 :
            latitude_1_radian = math.radians(latitude_1)
            latitude_2_radian = math.radians(latitude_2)

            longitude_1_radian = math.radians(longitude_1)
            longitude_2_radian = math.radians(longitude_2)

            delta_latitude_radian = latitude_2_radian - latitude_1_radian
            delta_longitude_radian = longitude_2_radian - longitude_1_radian


            # Formule
            radical = math.sin(delta_latitude_radian / 2) ** 2 + math.cos(latitude_1_radian) * math.cos(latitude_2_radian) * math.sin(delta_longitude_radian / 2) ** 2
            distance_ville = 2 * rayon * math.asin(math.sqrt(radical))

            # Ajout des villes 1 et 2 et leur distances dans la liste de calculs
            liste_calcul_distance.append((ville_1, pays_1, latitude_1, longitude_1, ville_2, pays_2, latitude_2, longitude_2, distance_ville))

    # Trie des villes en fonction de la distance minimum (Derniere position)
    liste_calcul_distance.sort(key=lambda x: x[-1])


    with open('distances.csv', mode='w', encoding='utf-8') as fichier_distances: #Creation du fichier distances.csv
        writer = csv.writer(fichier_distances)
        # On Ajoute d'abord cette ligne comme entete pour chaque ville
        writer.writerow(['ville1', 'pays1', 'latitude1', 'longitude1', 'ville2', 'pays2', 'latitude2', 'longitude2', 'distance'])

        for distance in liste_calcul_distance: #Pour chaque calculs entre les ville 1 et ville 2 dans la liste
            writer.writerow(distance) #On l'ajoute dans le fichier distances.csv


    distance_min = liste_calcul_distance[0] # On prend prend le premier calcul qui est la distance minimal dans la liste et on l'affiche
    print(f"Distance minimale en km entre 2 villes : Ville 1 : {distance_min[0]} {distance_min[1]} {distance_min[2]} {distance_min[3]} et Ville 2 : {distance_min[4]} {distance_min[5]} {distance_min[6]} {distance_min[7]} Distance en kilomètres : {distance_min[8]}")



def menu():

    choix_1_valide = "" #Variable pour savoir si l'utilisateur a fait le choix 1
    choix_2_valide = "" #Variable pour savoir si l'utilisateur a fait le choix 2

    while True: #Boucle pour afficher le menu en continu apres chaque choix saut q (quitter)
        print("Menu")
        print("1- Creation et affichage du fichier CSV\n2- Sauvegarde en JSON\n3- Affichage distance minimale et sauvegarde des calculs (distances.csv)\nq- pour quitter")

        choix = input("Choisissez une option : ")

        if choix == '1': # Creation et affichage du fichier
            Liste_Objet_DonneesGeo = lireDonneesCsv("Ville.csv")
            choix_1_valide = "OK" #Choix 1 valide, variable affecter

        elif choix == '2': # Sauvegarde en JSON
            if choix_1_valide == "OK":
                ecrireDonneesJson("Ville.json", Liste_Objet_DonneesGeo)
                print("Données sauvegardées dans le fichier Ville.json.")
                choix_2_valide = "OK" #Choix 2 valide, variable affecter
            else:
                print("Erreur, Exécuter d'abord l'option 1.")

        elif choix == '3': # Affichage distance minimale et sauvegarde des calculs (distances.csv)
            if choix_2_valide == "OK":
                trouverDistanceMin("Ville.json")
                print("Calculs de distance sauvegardés dans le fichier distances.csv.")
            else:
                print("Erreur : Veuillez d'abord exécuter l'option 2 pour sauvegarder les données au format JSON.")

        elif choix == 'q':
            print("Sortie du programme.")
            break

        else:
            print("Choix non valide : ")


menu()