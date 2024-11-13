"""
Module de transformation des données.

Ce module contient des fonctions pour organiser les données de livres dans un dictionnaire
et pour organiser les données de livres par catégorie dans un dictionnaire.
"""

from etl.extract import extract_book_data


def organise_books_data_into_dict(books_url_list):
    """
    Lance la fonction extract_book_data pour chaque URL de livre dans la liste.
    Retourne un dictionnaire de données de livres.
    """

    books_dictionnary = {}

    book_numb = 1
    total_of_books_to_scrap = len(books_url_list)

    # Extraction des données de chaque livre
    # Affiche également la progression dans le terminal
    for book_url in books_url_list:
        print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
        books_dictionnary.update(extract_book_data(book_url))
        book_numb += 1

    return books_dictionnary


def organise_books_data_by_category(books_dictionary):
    """
    Organise les données de livres par catégorie.
    Retourne un dictionnaire de données de livres organisé par catégorie.
    """

    books_by_category = {}

    # Création d'un dictionnaire de livres organisé par catégorie
    for book in books_dictionary.values():
        category = book.category

        # Si la catégorie n'existe pas, on la crée
        if category not in books_by_category:
            books_by_category[category] = []
        books_by_category[category].append(book)

    return books_by_category
