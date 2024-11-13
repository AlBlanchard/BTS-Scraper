"""
Ce module permet de scraper les données des livres d'une catégorie spécifique, 
de toutes les catégories, d'un livre via son nom ou d'un livre via son URL.

Il utilise les modules extract, transform et load pour extraire, transformer et charger les données.

Il utilise également le module url_collector pour collecter les URLs des livres.

Il utilise le module get_it pour récupérer le site à scraper.
"""

import requests
from etl.transform import organise_books_data_into_dict
from etl.extract import (
    extract_category,
    extract_book_data,
    search_book_name_and_extract_url,
)
from etl.load import load_book_data
from modules.url_collector import book_url_collector
from modules.get_it import SITE


def scrap_category(argv_2):
    """Scrape les livres d'une catégorie spécifique ou de toutes les catégories."""
    all_category_dictionary = extract_category()

    # Si l'argument est 'all', on scrape tous les livres de toutes les catégories
    if argv_2.lower() == "all":
        books_url_list = book_url_collector(SITE)
        books_dictionary = organise_books_data_into_dict(books_url_list)
        load_book_data(books_dictionary, global_data=True)

    # Si l'argument est une catégorie valide, on scrape les livres de cette catégorie
    elif argv_2.lower() in all_category_dictionary:
        books_url_dictionnary = book_url_collector(
            all_category_dictionary[argv_2.lower()]
        )
        books_dictionary = organise_books_data_into_dict(books_url_dictionnary)
        load_book_data(books_dictionary)

    else:
        print(f"La catégorie '{argv_2}' n'existe pas.")


def scrap_book_from_research(book_name):
    """Cherche un livre par son nom et scrape ses données."""
    book_url = search_book_name_and_extract_url(book_name.lower())
    book_data = extract_book_data(book_url)
    load_book_data(book_data)


def scrap_book_from_url(url):
    """Scrape un livre via son URL."""
    # Permet de scraper uniquement les pages de livres.
    if url.lower().startswith(
        "https://books.toscrape.com/catalogue/"
    ) and not url.lower().startswith("https://books.toscrape.com/catalogue/category/"):
        try:
            book_data = extract_book_data(url)
            load_book_data(book_data)
        except (ValueError, requests.exceptions.RequestException) as e:
            print(f"L'url n'est pas valide: {e}")
    else:
        print("Veuillez entrer une url valide.")
