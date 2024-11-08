"""
Ce module contient les fonctions qui permettent de scrapper les données du site Books to Scrape.

"""

import sys
import re
from urllib.parse import urljoin
from modules.get_it import SITE
from modules.get_it import HOME_SOUP
from modules.get_it import get_html
from modules.class_type import Book


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
    Permet de récupérer les données d'un livre.

    Retourne un dictionnaire avec l'UPC du livre comme clé et les données du livre comme valeur.

    """
    soup = get_html(page_url)

    # Cette fonction permet de simplifier l'extraction de données et de rendre stable le script : il ne plantera pas si une donnée n'existe pas ou si la structure du site n'a pas été respecté, il renverra une valeur par défault.
    def get_data_or_default(
        tag_name,
        text=None,
        attribute="text",
        id=None,
        default="Non renseigné(e)",
        next_sibling=False,
    ):

        # On récupère l'élément en fonction des paramètres text ou id (si définis)
        element = (
            soup.find(tag_name, text=text, id=id) if text or id else soup.find(tag_name)
        )

        if element:
            if next_sibling:
                # Si le paramètre next_sibling est True, on cherche le prochain élément frère
                next_element = element.find_next_sibling()
                return next_element.text.strip() if next_element else default

            elif attribute == "text":
                # Si on récupère du texte, simplement extraire le texte de l'élément
                return element.text.strip()

            else:
                # Si on veut un autre attribut (comme "src" pour les images, etc.)
                return element[attribute]

        return default

    # Et hop on récupère les données
    product_page_url = page_url
    upc = get_data_or_default("th", "UPC", next_sibling=True)
    title = get_data_or_default("h1")
    price_including_tax = get_data_or_default(
        "th", "Price (incl. tax)", next_sibling=True
    )
    price_excluding_tax = get_data_or_default(
        "th", "Price (excl. tax)", next_sibling=True
    )

    # Stock avec extraction du nombre grâce à mon merveilleux ami Regex
    stock_text = get_data_or_default("th", "Availability", next_sibling=True)
    regex_match = re.search(r"\((\d+)", stock_text)
    number_available = regex_match.group(1) if regex_match else "Non renseigné(e)"

    # Description
    product_description = get_data_or_default(
        "div", id="product_description", next_sibling=True
    )

    # Catégorie
    path_links = soup.find(class_="breadcrumb").find_all("a")
    category = path_links[2].text.strip() if len(path_links) > 2 else "Non renseigné(e)"

    # Rating avec conversion en chiffre
    review_rating_in_letter = soup.find("p", class_="star-rating")["class"][1]
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    review_rating = rating_map.get(review_rating_in_letter, "Non renseigné(e)")

    # URL de l'image
    image_url = urljoin(page_url, get_data_or_default("img", attribute="src"))

    # Maintenant que toutes les données ont été récoltés, les mettre en place dans l'objet
    book_data = Book(
        product_page_url=product_page_url,
        upc=upc,
        title=title,
        price_including_tax=price_including_tax,
        price_excluding_tax=price_excluding_tax,
        number_available=number_available,
        product_description=product_description,
        category=category,
        review_rating=review_rating,
        image_url=image_url,
    )

    return {f"book_{upc}": book_data}


def books_url_dictionnary_scraping(books_url_dictionnary):
    books_dictionnary = {}

    book_numb = 1
    total_of_books_to_scrap = len(books_url_dictionnary)

    for book_url in books_url_dictionnary.values():
        print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
        books_dictionnary.update(scrap_book_data(book_url))
        book_numb += 1

    return books_dictionnary
