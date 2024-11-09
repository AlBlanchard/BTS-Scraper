"""
Ce module contient les fonctions qui permettent de scrapper les données du site Books to Scrape.

"""

import sys
from urllib.parse import urljoin
from modules.get_it import SITE
from modules.get_it import HOME_SOUP
from modules.get_it import get_html
from modules.get_it import get_data_of_element
from modules.class_type import Book
from modules.data_cleaner import clean_price
from modules.data_cleaner import clean_stock
from modules.data_cleaner import clean_rating
from modules.get_it import find_book_data_element


def scrap_category():
    """
    Permet de récupérer toutes les catégories du site, avec leur URL associée.

    Les stocke dans un dictionnaire,
    avec comme clé le nom de la catégorie et comme valeur l'URL de la catégorie.
    """

    all_category_dictionnary = {}

    # Une fonction try/except pour gérer les erreurs de structure du site.
    # Sinon, le script plantera si la structure du site a changé.
    try:
        all_category_anchor = HOME_SOUP.find(class_="nav-list").find("ul").find_all("a")

    except AttributeError:
        print(
            "Erreur 'all_category_anchor' : Le site semble avoir changé de structure."
        )
        sys.exit()

    for category_anchor in all_category_anchor:
        all_category_dictionnary[category_anchor.text.strip()] = urljoin(
            SITE, category_anchor["href"]
        )

    return all_category_dictionnary


def scrap_product_url(page_url):
    """
    Permet de récupérer les URL des livres d'une page.

    Les stocke dans un dictionnaire,
    avec comme clé le titre du livre et comme valeur l'URL du livre.
    """

    soup = get_html(page_url)
    books_dictionnary = {}

    # Une fonction try/except pour gérer les erreurs de structure du site.
    # Sinon, le script plantera si la structure du site a changé.
    try:
        all_books_h3 = soup.find_all("h3")
    except AttributeError:
        print("Erreur 'all_books_h3' : Le site semble avoir changé de structure.")
        sys.exit()

    # Pas besoin de try/except, il est possible que la page n'ait pas de page suivante.
    next_page_anchor = soup.find(class_="next")

    # En cas de plusieurs page, un compteur pour faire patienter l'utilisateur...
    there_is_a_pager = bool(soup.find(class_="current"))
    if there_is_a_pager:
        page_number = soup.find(class_="current").text.strip().lower()
        print(f"Scan {page_number}...")
    else:
        print("Scan page 1 of 1...")

    # Boucle pour récupérer les titres et URL des livres.
    # Les stocke dans un dictionnaire. La clé est le titre du livre et la valeur est l'URL du livre.
    # Encore try/except quand il s'agit de la structure du site pour éviter les plantages.
    for book in all_books_h3:
        try:
            book_anchor = book.find("a")
            book_title = book_anchor["title"]
            book_url = urljoin(page_url, book_anchor["href"])
            books_dictionnary[book_title] = book_url  # Ajouter au dictionnaire
        except AttributeError:
            print("Erreur 'book_anchor' : Le site semble avoir changé de structure.")
            sys.exit()

    # Vérifie s'il y a une autre page
    if next_page_anchor:
        next_page_uri = next_page_anchor.find("a")["href"]
        next_page_url = urljoin(page_url, next_page_uri)

        # Appel récursif pour scrapper la page suivante
        books_dictionnary.update(scrap_product_url(next_page_url))

    return books_dictionnary


def search_book_name_and_url(book_name, url=SITE):
    """
    Permet de rechercher un livre via une partie de son titre.
    Retourne l'URL du livre si trouvé.
    """

    while url:
        soup = get_html(url)

        # En cas de plusieurs page, un compteur pour faire patienter l'utilisateur...
        there_is_a_pager = bool(soup.find(class_="current"))
        if there_is_a_pager:
            page_number = soup.find(class_="current").text.strip().lower()
            print(f"Scan {page_number}...")
        else:
            print("Scan page 1 of 1...")

        # Recherche d'une correspondance avec le titre des livres sur la page
        for h3 in soup.find_all("h3"):
            title = h3.find("a")["title"]

            # Pour que la comparaison soit insensible à la casse
            if book_name.lower() in title.lower():
                print(f"Trouvé : {title}")
                book_url = urljoin(url, h3.find("a")["href"])

                return book_url

        there_is_an_other_page = bool(soup.find(class_="next"))

        if there_is_an_other_page:
            next_page_anchor = soup.find(class_="next").find("a")
            next_page_url = urljoin(url, next_page_anchor["href"])
            url = next_page_url
        else:
            break

    print("Aucune correspondance trouvée, assurez vous que le titre soit correct.")
    sys.exit()


def scrap_book_data(page_url):
    """
    Extrait les données d'un livre depuis la page donnée et retourne un dictionnaire.
    """

    # Récupération des éléments HTML relatifs aux données du livre
    book_elements = find_book_data_element(page_url)

    # Extraction des données en utilisant find_element et get_data_of_element
    upc = get_data_of_element(book_elements["upc_element"])
    title = get_data_of_element(book_elements["title_element"])

    # Enlève le symbole £ des prix (clean_price)
    price_incl_tax = clean_price(
        get_data_of_element(book_elements["price_incl_tax_element"])
    )
    price_excl_tax = clean_price(
        get_data_of_element(book_elements["price_excl_tax_element"])
    )

    # Nettoie la disponibilité du stock (clean_stock)
    number_available = clean_stock(
        get_data_of_element(book_elements["number_available_element"])
    )

    # Description du produit
    product_description = get_data_of_element(
        book_elements["product_description_element"]
    )

    # Catégorie
    category = get_data_of_element(book_elements["category_element"])

    # Évaluation en étoiles (conversion du texte en notation numérique)
    rating_text = get_data_of_element(book_elements["rating_element"], attr="class")
    rating_text = rating_text[1] if rating_text != "Non renseigné(e)" else rating_text
    review_rating = clean_rating(rating_text)

    # URL de l'image
    image_url = urljoin(
        page_url, get_data_of_element(book_elements["image_element"], attr="src")
    )

    # Création de l'objet de données du livre
    book_data = Book(
        product_page_url=page_url,
        upc=upc,
        title=title,
        price_including_tax=price_incl_tax,
        price_excluding_tax=price_excl_tax,
        number_available=number_available,
        product_description=product_description,
        category=category,
        review_rating=review_rating,
        image_url=image_url,
    )

    return {f"book_{upc}": book_data}


def books_url_dictionnary_scraping(books_url_dictionnary):
    """
    Scrap les données de tous les livres d'un dictionnaire d'URL.
    Retourne un dictionnaire de données de livres.
    """

    books_dictionnary = {}

    book_numb = 1
    total_of_books_to_scrap = len(books_url_dictionnary)

    for book_url in books_url_dictionnary.values():
        print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
        books_dictionnary.update(scrap_book_data(book_url))
        book_numb += 1

    return books_dictionnary
