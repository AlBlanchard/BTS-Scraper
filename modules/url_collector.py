"""
Ce module contient les fonctions qui permettent de scrapper les données du site Books to Scrape.

"""

import sys
from urllib.parse import urljoin
from modules.get_it import get_html, pagination_counter


def doublon_checker(book_url, new_books_url_list, global_books_url_list):
    """
    Vérifie si l'URL est en doublon dans la liste en cours ou globale.
    """

    if book_url in new_books_url_list:
        print(f"URL en doublon détecté : {book_url}")
    elif book_url in global_books_url_list:
        print(f"URL en doublon détecté : {book_url}")
    else:
        # Si ce n'est pas un doublon, on l'ajoute à la liste temporaire
        new_books_url_list.append(book_url)


def h3_collector(soup):
    """
    Récupère les éléments h3 de la page.
    """

    try:
        all_books_h3 = soup.find_all("h3")

    except AttributeError:
        print("Erreur 'all_books_h3' : Le site semble avoir changé de structure.")
        sys.exit()

    return all_books_h3


def next_page_collector(soup, page_url, global_books_url_list):
    """
    Récupère l'URL de la page suivante.
    """

    next_page_anchor = soup.find(class_="next")
    if next_page_anchor:
        next_page_uri = next_page_anchor.find("a")["href"]
        next_page_url = urljoin(page_url, next_page_uri)
        book_url_collector(next_page_url, global_books_url_list)


def book_url_collector(page_url, global_books_url_list=None):
    """
    Permet de récupérer les URL des livres d'une page et de les regrouper dans une liste.
    Gère la pagination grace à deux listes : global_books_url_list et new_books_url_list.
    new_books_url_list est une liste temporaire qui est fusionnée avec global_books_url_list.
    Vérifie aussi les doublons avant la fusion.
    Retourne global_books_url_list, la liste totale des URL des livres.
    """

    if global_books_url_list is None:
        global_books_url_list = []

    soup = get_html(page_url)

    new_books_url_list = []

    pagination_counter(soup)
    all_books_h3 = h3_collector(soup)

    # Collecter les url des livres et vérifier les doublons avant de les ajouter
    for book_h3 in all_books_h3:
        try:
            book_url = urljoin(page_url, book_h3.find("a")["href"])
            doublon_checker(book_url, new_books_url_list, global_books_url_list)

        except AttributeError:
            print(
                "Erreur 'book_h3_find('a')' : Le site semble avoir changé de structure."
            )
            sys.exit()

    # Fusionner les listes
    global_books_url_list.extend(new_books_url_list)

    # Gérer la pagination si nécessaire
    next_page_collector(soup, page_url, global_books_url_list)

    return global_books_url_list
