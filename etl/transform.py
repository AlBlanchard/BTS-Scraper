"""
Module de transformation des données.
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

    for book_url in books_url_list:
        print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
        books_dictionnary.update(extract_book_data(book_url))
        book_numb += 1

    return books_dictionnary
