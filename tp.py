'''
@auteur(e)s     Bradley Colas et Jean Luc Adrien
@matricules     e2353376 et eYYYYYY
@date           13-05-2024
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