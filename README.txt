TABLE DES MATIERES
-----------------------------

* Introduction
* Conditions
* Instalation
* Lancement
* Utilisation
* Description synthétique du fonctionnement interne de l'application
* Auteur



#INTRODUCTION
-------------

Cette application permet de synchroniser deux dossiers en local offrant deux possibilités de synchronisation:
	* synchroniser tous les fichiers (toutes les extensions confondues)
	* synchroniser les fichiers avec une extension choisie 

Cette application fonctionne sur tous les OS.

Pour le bon fonctionnement de l'application :
	* Le dossier source ne doit pas contenir de fichier nommé ControlFS.cvs ce nom est réservé.
	* Le dossier destination ne doit pas contenir de fichier nommé ControlFD.cvs ce nom est réservé.



#CONDITIONS
-----------

Ce projet necessite les modules suivants pour fonctionner :
	* python 
	* pip
	* flask
	* bibliothèque pandas de python



#INSTALATION
---------------

1) Installer python (et pip si besoin): Windows : https://www.python.org/downloads/windows/
					Linux   : sudo apt-get install python3.7
2) Installer pandas : pip install pandas
3) Instaler flask : pip install flask



#LANCEMENT
----------

1) Creer un dossier
2) Copier les dossiers (templates, statics) et les fichiers (function.py, app.py) dans ce dossier crée.

Dans l'invite de commande :
3) Entrer dans le dossier crée 
4) Préparer l'environnement : py -m venv venv
5) Activer l'environnement  : venv/Scripts/activate
6) Lancer l'application     : py app.py

Dans un navigateur internet
7) Taper dans la barre d'adresse : localhost:5000
8) Tester l'application



#UTILISATION
------------

Pour synchroniser tous les fichiers : il faut les chemins absolus des dossiers source et destination
Pour synchroniser les fichiers avec extension: il faut les chemins absolus des dossiers source, dossier destination et l'extension



#DESCRIPTION SYNTHETIQUE DU FONCTIONNEMENT INTERNE DE L'APPLICATION
--------------------------

Cette application est basé sur des fichiers de controle pour fonctionner.
ControlFS.csv = Le fichier de controle source qui repertorie tous les fichiers présents dans le dossier source. 
ControlFD.csv = Le fichier de controle destination qui repertorie tous les fichiers présents dans le dossier destination.

Fichier de controle : - utilise la librairie pandas de python pour simplifier la manipulation de données,
		      - permet de garder l'ancien état du dossier avant un changement (suppression, ajout ou modification de fichier),
		      - permet de detecter facilement les changements (en comparant le fichier de controle avec l'état du dossier actuel, après changement) 
			ces changements sont stockés dans un dataFramme nommé dataframmeMod.


1) [bouton valider]
Si les chemins de dossiers sont validés avec succès (dossiers trouvés) :
	* Si le fichier ControlFS.csv n'existe pas : --> Création du fichier et Ajout de tous les fichiers (fileName, extension, modificationDate, size) dans le fichier
						     --> Completer le dataframmeMod avec tous les fichiers avec la mention add (fileName,add) 
	* Si le fichier ControlFS.csv existe       : --> Actualisation du fichier par rapport aux changements effectués dans le dossier source (Ajout, Suppression, Modification)
						     --> Completer le dataframmeMod avec les changements constatés avec la mention add,del ou mod (fileName,add) (fileName,del) (fileName,mod)
	* Si le fichier ControlFD.csv n'existe pas : --> Création du fichier vide
							
2) [bouton synchroniser]
Applique les changements contenus dans dataframmeMod au dossier destination pour la synchronisation.

 

#AUTEUR
-------

RAKOTOBE Corine (rakotobecorinendriana@yahoo.fr)