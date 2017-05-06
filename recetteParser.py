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
        self.ingred = ingred
        self.preparation = preparation

def extraction(str, motif,deb, fin):
	n = deb + len(motif)
	return str[n:fin]

def parser_ingredients(str, deb, fin):
	list_ing = []
	debRecherche = deb

	while debRecherche < (fin - 2):
	
		d = str.find("<NomItem>", debRecherche)
		f = str.find("</NomItem>", debRecherche)
		nomItem = extraction(str, "<NomItem>", d, f)
		d = str.find("<Quantite>", debRecherche)
		f = str.find("</Quantite>", debRecherche)
		quantitie = extraction(str, "<Quantite>", d, f)
		item = (nomItem, quantitie)
		list_ing.append(item)
		debRecherche = str.find("</Item>", debRecherche) + 7
		
	return list_ing


def read_file(filename):
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
			recette = Recette(nom, tempsPrep, tempsCuis, nbPers, ingred, preparation)
			list_recettes.append(recette)

	return list_recettes

def lire(list_recettes):
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