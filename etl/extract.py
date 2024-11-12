"""
Module d'extraction des données du site Books to Scrape.
"""

import sys
import re
from urllib.parse import urljoin
from modules.data_cleaner import clean_price, clean_stock, clean_rating
from modules.get_it import (
    get_html,
    get_data_of_element,
    find_book_data_element,
    pagination_counter,
    SITE,
    HOME_SOUP,
)
from modules.class_type import Book


def extract_category():
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
        all_category_dictionnary[category_anchor.text.strip().lower()] = urljoin(
            SITE, category_anchor["href"]
        )

    return all_category_dictionnary


def extract_book_data(page_url):
    """
    Extrait les données d'un livre depuis la page en paramètre
    Retourne un dictionnaire {book_'upc': Book} contenant les données du livre.
    Book est une instance de la classe Book.
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


def search_book_name_and_extract_url(book_name, url=SITE):
    """
    Permet de rechercher un livre via une partie de son titre.
    Retourne l'URL du livre si trouvé.
    """
    # Divise book_name en mots individuels pour la recherche
    book_name_words = book_name.lower().split()

    while url:
        soup = get_html(url)

        pagination_counter(soup)

        # Recherche d'une correspondance avec le titre des livres sur la page
        for h3 in soup.find_all("h3"):
            title = h3.find("a")["title"]

            # Vérifie si tous les mots de book_name sont présents dans le titre
            if all(
                re.search(rf"\b{re.escape(word)}\b", title.lower())
                for word in book_name_words
            ):
                print(f"Trouvé : {title}")
                book_url = urljoin(url, h3.find("a")["href"])
                return book_url

        try:
            next_page_anchor = soup.find(class_="next").find("a")
            next_page_url = urljoin(url, next_page_anchor["href"])
            url = next_page_url
        except AttributeError:
            break

    print("Aucune correspondance trouvée, assurez vous que le titre soit correct.")
    sys.exit()
