from modules.get_it import SITE
from urllib.parse import urljoin
from modules.get_it import get_html
from modules.get_it import HOME_SOUP
import re
from modules.class_type import Book

def scrap_category() :

    all_category_dictionnary = {}
    all_category_anchor = HOME_SOUP.find(class_="nav-list").find("ul").find_all("a")

    for category_anchor in all_category_anchor :
        all_category_dictionnary[category_anchor.text.strip()] = urljoin(SITE, category_anchor["href"])

    return all_category_dictionnary 

all_category_dictionnary = scrap_category()

def scrap_product_url(page_url) :
    soup = get_html(page_url) 
    products_dictionnary = {} 

    # Récupérer tous les produits et vérifier les pages suivantes en une seule recherche
    all_products_h3 = soup.find_all("h3")
    next_page_anchor = soup.find(class_="next")

    # En cas de plusieurs page, un compteur pour faire patienter l'utilisateur...
    there_is_a_pager = bool(soup.find(class_="current"))
    if there_is_a_pager :
        page_number = soup.find(class_="current").text.strip().lower()
        print(f"Scan {page_number}...")
    else :
        print("Scan page 1 of 1...")


    for product in all_products_h3:
        product_anchor = product.find("a")
        product_title = product_anchor["title"]
        product_url = urljoin(page_url, product_anchor["href"])
        products_dictionnary[product_title] = product_url  # Ajouter au dictionnaire

    # Vérifier s'il y a une autre page
    if next_page_anchor:
        next_page_uri = next_page_anchor.find("a")["href"]
        next_page_url = urljoin(page_url, next_page_uri)

        # Appel récursif pour scrapper la page suivante
        products_dictionnary.update(scrap_product_url(next_page_url))

    return products_dictionnary 


def search_book_name_and_url(book_name, url=SITE) :
    while url :
        soup = get_html(url)

        # En cas de plusieurs page, un compteur pour faire patienter l'utilisateur...
        there_is_a_pager = bool(soup.find(class_="current"))
        if there_is_a_pager :
            page_number = soup.find(class_="current").text.strip().lower()
            print(f"Scan {page_number}...")
        else :
            print("Scan page 1 of 1...")

        # Recherche d'une correspondance avec le titre des livres sur la page
        for h3 in soup.find_all("h3") :
            title = h3.find("a")["title"]

            if book_name.lower() in title.lower() : #Pour que la comparaison soit insensible à la casse
                print(f"Trouvé : {title}")
                book_url = urljoin(SITE, h3.find("a")["href"])
                
                return book_url
            
        there_is_an_other_page = bool(soup.find(class_="next"))
        
        if there_is_an_other_page :
            next_page_anchor = soup.find(class_="next").find("a")
            next_page_url = urljoin(url, next_page_anchor["href"])
            url = next_page_url

        else :
            print("Pas trouvé, assurez vous que le titre soit correct.")
            exit()

def scrap_book_data(page_url):
    soup = get_html(page_url)

    # Cette fonction permet de simplifier l'extraction de données et de rendre stable le script : il ne plantera pas si une donnée n'existe pas ou si la structure du site n'a pas été respecté, il renverra une valeur par défault. 
    def get_data_or_default(tag_name, text=None, attribute="text", id=None, default="Non renseigné(e)"):
        element = soup.find(tag_name, text=text, id=id) if text or id else soup.find(tag_name)
        if element:
            if attribute == "text":
                return element.find_next_sibling("td").text.strip() if tag_name == "th" else element.text.strip()
            else:
                return element[attribute]
        return default

    # Et hop on récupère les données
    product_page_url = page_url
    upc = get_data_or_default("th", "UPC")
    title = get_data_or_default("h1")
    price_including_tax = get_data_or_default("th", "Price (incl. tax)")
    price_excluding_tax = get_data_or_default("th", "Price (excl. tax)")

    # Stock avec extraction du nombre grâce à mon merveilleux ami Regex
    stock_text = get_data_or_default("th", "Availability")
    regex_match = re.search(r'\((\d+)', stock_text)
    number_available = regex_match.group(1) if regex_match else "Non renseigné(e)"

    # Description
    product_description = get_data_or_default("div", id="product_description")

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
        product_page_url = product_page_url,
        upc = upc,
        title = title,
        price_including_tax = price_including_tax,
        price_excluding_tax = price_excluding_tax,
        number_available = number_available,
        product_description = product_description,
        category = category,
        review_rating = review_rating,
        image_url = image_url
    )

    return {f"book_{upc}": book_data}


def books_url_dictionnary_scraping(books_url_dictionnary) :
        books_dictionnary = {}
        
        book_numb = 1
        total_of_books_to_scrap = len(books_url_dictionnary)

        for book_url in books_url_dictionnary.values() :
            print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
            books_dictionnary.update(scrap_book_data(book_url))
            book_numb += 1

        return books_dictionnary 

