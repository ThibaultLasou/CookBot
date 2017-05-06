#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

class Recette:
    """Classe définissant une recette caractérisée par :
    - son nom
    - son temps de préparation
    - son temps de cuisson
    - le nombre de personnes qui peuvent la déguster
    - ses ingrédients 
    - sa préparation
    """

    def __init__(self, nom, tempsPrep, tempsCuis, nbPers, ingred, preparation): # Constructeur
        
        self.nom = nom
        self.tempsPrep = tempsPrep
        self.tempsCuis = tempsCuis
        self.nbPers= nbPers
        self.ingred = ingred # liste de tuple [(nomIngredient, quantite)]
        self.preparation = preparation

def extraction(str, balise,deb, fin): # extraction du texte entre deux balises 
# deb est la position de la balise d'ouverture dans str et fin la position de la balise de fermeture
	n = deb + len(balise)
	return str[n:fin]

def parser_ingredients(str, deb, fin):
# extraction particulière car on a un nombre quelconque d'ingredients, chaque ingrédient étant associé à sa quantité
	list_ing = []
	debRecherche = deb # debRecherche est l'endroit à partir duquel on va rechercher une balise
# On récupère tous les ingrédients en parcourant le contenu des balises <Ingredients> et </Ingredients>
	while debRecherche < (fin - 2):
	
		d = str.find("<NomItem>", debRecherche) # on cherche la position de la balise <NomItem> à partir de debRecherche
		f = str.find("</NomItem>", debRecherche)
		nomItem = extraction(str, "<NomItem>", d, f)
		d = str.find("<Quantite>", debRecherche)
		f = str.find("</Quantite>", debRecherche)
		quantitie = extraction(str, "<Quantite>", d, f)
		item = (nomItem, quantitie) # on créé le tuple et on l'ajoute à la liste des ingrédients
		list_ing.append(item)
		debRecherche = str.find("</Item>", debRecherche) + 7 # on actualise la position de debut de la prochaine recherche
		
	return list_ing


def read_file(filename): # point d'entrée du parsage des données
	list_recettes = []
	with open(filename, "r") as filepointer:
		chaine = filepointer.read()
		recetteAParser = chaine.split("</Recette>")
		for eltRecette in recetteAParser:
			if eltRecette=="": break
			deb = eltRecette.find("<Titre>")
			fin = eltRecette.find("</Titre>")
			nom = extraction(eltRecette, "<Titre>", deb, fin)
			deb = eltRecette.find("<TempsPreparation>")
			fin = eltRecette.find("</TempsPreparation>")
			tempsPrep = extraction(eltRecette, "<TempsPreparation>", deb, fin)
			deb = eltRecette.find("<TempsCuisson>")
			fin = eltRecette.find("</TempsCuisson>")
			tempsCuis = extraction(eltRecette, "<TempsCuisson>", deb, fin)
			deb = eltRecette.find("<NombrePersonne>")
			fin = eltRecette.find("</NombrePersonne>")
			nbPers = extraction(eltRecette, "<NombrePersonne>", deb, fin)
			deb = eltRecette.find("<Ingredients>")
			fin = eltRecette.find("</Ingredients>")
			ingred = parser_ingredients(eltRecette, deb, fin)
			deb = eltRecette.find("<Preparation>")
			fin = eltRecette.find("</Preparation>")
			preparation = extraction(eltRecette, "<Preparation>", deb, fin)
			# On créé la recette avec toutes ses informations et on l'ajoute à la liste de recette
			recette = Recette(nom, tempsPrep, tempsCuis, nbPers, ingred, preparation)
			list_recettes.append(recette)

	return list_recettes

def lire(list_recettes): # fonction de test qui affiche liste de toutes les recettes
	for elt in list_recettes:
		print(" Nom recette : ", elt.nom)
		print(" Temps de préparation : ", elt.tempsPrep)
		print(" Temps de cuisson : ", elt.tempsCuis)
		print(" Nombre de personnes : ", elt.nbPers)
		print(" Ingrédients : ")

		for ing in elt.ingred:
			print(ing)

		print(" Préparation : ", elt.preparation)

if __name__=="__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('textfile_folder')
    args = argparser.parse_args()

    # file locations
    folder = args.textfile_folder
    filepath = folder+"/recettes.xml"
   
    list_recettes = read_file(filepath)
    lire(list_recettes)