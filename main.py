"""
Le main comprend uniquement deux grandes conditions :

-> La première vérifie si les arguments constants entrés sont valides. 

-> La deuxième condition vérifie si les arguments variables sont valides, 
puis lance le script en fonction des arguments.

"""

import sys
import requests
from modules.scrap_it import book_url_collector
from modules.get_it import SITE
from modules.argv_check import validate_script_arguments
from modules.scrap_it import organise_books_data_into_dict
from modules.scrap_it import scrap_book_data
from modules.scrap_it import scrap_category
from modules.scrap_it import search_book_name_and_url
from modules.save_it import save_it

# Vérifie si les arguments passés au script sont valides.
if not validate_script_arguments(sys.argv):
    sys.exit()

# Lance le script en fonction des arguments passés.
if len(sys.argv) == 2:

    # Affiche une petite aide pour utiliser le script.
    if sys.argv[1].lower() == "infos":
        print(
            "\n"
            "Voici comment exécuter les différentes fonctions du script :\n\n"
            "main.py category 'nom_de_la_catégorie'\n"
            "-> Scrape les livres d'une catégorie spécifique.\n\n"
            "main.py category all\n"
            "-> Scrape tous les livres de toutes les catégories, cette opération est longue.\n\n"
            "main.py search 'nom_du_livre'\n"
            "-> Cherche le livre qui correspond, puis le scrap. Soyez le plus précis possible.\n"
            "-> Le premier livre trouvé sera scrapé.\n\n"
            "main.py book 'url_du_livre'\n"
            "-> Scrape un livre via son URL.\n\n"
            "main.py infos category\n"
            "-> Affiche toutes les catégories du site dans la console.\n"
        )

elif len(sys.argv) == 3:

    # Permet d'afficher toutes les catégories du site dans la console.
    if sys.argv[1].lower() == "infos" and sys.argv[2].lower() == "category":
        all_category_dictionnary = scrap_category()

        print("\nVoici toutes les catégories du site :\n")
        for category in all_category_dictionnary:
            print(category)

    # L'arg category pour scrap les livres d'une catégorie spécifique ou de toutes les catégories.
    elif sys.argv[1].lower() == "category":
        all_category_dictionnary = scrap_category()

        # Scrap toutes les catégories.
        # Petit trick pour gagner du temps, récupère les données via le home index.
        # Pas de besoin de scraper categorie par categorie.
        if sys.argv[2].lower() == "all":
            books_url_list = book_url_collector(SITE)
            books_dictionnary = organise_books_data_into_dict(books_url_list)

            save_it(books_dictionnary)

        # Vérifie si la categorie existe, puis scrap les livres de cette catégorie.
        elif sys.argv[2] in all_category_dictionnary:
            books_url_dictionnary = book_url_collector(
                all_category_dictionnary[sys.argv[2]]
            )
            books_dictionnary = organise_books_data_into_dict(books_url_dictionnary)

            save_it(books_dictionnary)

        else:
            print(f"La catégorie '{sys.argv[2]}' n'existe pas.")

    # L'arg search lance la recherche d'un livre via une partie de son titre, et scrap ses données.
    elif sys.argv[1].lower() == "search":
        book_url = search_book_name_and_url(sys.argv[2].lower())
        book_data = scrap_book_data(book_url)

        save_it(book_data)

    # L'arg book lance le scrap d'un livre via son URL.
    elif sys.argv[1].lower() == "book":
        if sys.argv[2].lower().startswith(
            "https://books.toscrape.com/catalogue/"
        ) and not sys.argv[2].lower().startswith(
            "https://books.toscrape.com/catalogue/category/"
        ):
            # Stabilise le code en verifiant que l'url soit valide.
            try:
                book_data = scrap_book_data(sys.argv[2])
                save_it(book_data)

            except (ValueError, requests.exceptions.RequestException) as e:
                print(f"L'url n'est pas valide: {e}")

        else:
            print("Veuillez entrer une url valide.")

    else:
        print(f"L'argument {sys.argv[2]} est invalide.")
