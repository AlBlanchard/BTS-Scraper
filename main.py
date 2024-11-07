"""

Faire une explication

"""

import sys
from modules.scrap_it import scrap_product_url
from modules.get_it import SITE
from modules.argv_check import validate_script_arguments
from modules.scrap_it import books_url_dictionnary_scraping
from modules.scrap_it import scrap_book_data
from modules.scrap_it import scrap_category
from modules.scrap_it import search_book_name_and_url
from modules.save_it import save_it
from modules.get_it import get_html

if not validate_script_arguments(sys.argv):
    sys.exit()

argv_1 = sys.argv[1].lower()
argv_2 = sys.argv[2].lower()

if argv_1 == "infos":
    if len(sys.argv) == 2:
        print(
            "\n"
            "Voici comment exécuter les différentes fonctions du script :\n\n"
            "main.py category 'nom_de_la_catégorie'   -> Scrape les livres d'une catégorie spécifique\n"
            "main.py category all                     -> Scrape tous les livres de toutes les catégories\n"
            "main.py book 'nom_du_livre'              -> Scrape un livre en utilisant une partie de son titre\n"
            "main.py book 'url_du_livre'              -> Scrape un livre via son URL\n"
            "main.py infos category                   -> Affiche toutes les catégories du site dans la console\n"
        )
    elif argv_2 == "category":
        all_category_dictionnary = scrap_category()

        print("\nVoici toutes les catégories du site :\n")
        for category in all_category_dictionnary:
            print(category)

    else:
        print(f"L'argument '{sys.argv[2]}' n'est pas valide")


if argv_1 == "category":
    all_category_dictionnary = scrap_category()

    if argv_2 == "all":
        books_url_dictionnary = scrap_product_url(SITE)
        books_dictionnary = books_url_dictionnary_scraping(books_url_dictionnary)

        save_it(books_dictionnary)

    elif argv_2 in all_category_dictionnary:
        books_url_dictionnary = scrap_product_url(all_category_dictionnary[sys.argv[2]])
        books_dictionnary = books_url_dictionnary_scraping(books_url_dictionnary)

        save_it(books_dictionnary)

    else:
        print(f"L'argument '{sys.argv[2]}' n'est pas valide")

if argv_1 == "book":
    book_url = search_book_name_and_url(argv_2)
    book_data = scrap_book_data(book_url)

    save_it(book_data)
