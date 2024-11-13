"""
Module de chargement des données scrapées dans un fichier CSV et téléchargement des images.

Ce module utilise les modules save_it et extract pour sauvegarder les données scrapées 
dans un fichier CSV et télécharger les images.
"""

from modules.save_it import (
    download_image,
    save_books_to_csv,
    clear_previous_data,
    save_books_to_csv_by_category,
)


def load_book_data(books_dictionary, global_data=False):
    """Sauvegarde les données scrapées dans un fichier CSV et télécharge les images."""

    clear_previous_data()
    book_number = 1

    # Téléchargement des images, affiche également la progression dans le terminal
    for book in books_dictionary.values():
        print(f"Download image {book_number} of {len(books_dictionary)}")
        download_image(book)
        book_number += 1

    save_books_to_csv_by_category(books_dictionary)

    # Si l'argument global_data est True,
    # On sauvegarde également les données de tous les livres dans un seul fichier
    if global_data:
        save_books_to_csv(books_dictionary)
