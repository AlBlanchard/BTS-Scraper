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
        all_category_dictionnary[category_anchor.text.strip()] = category_anchor["href"] #strip() nettoie le texte

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


def search_book_name(book_name, url) :
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
                print(book_url)
                return True
            
        there_is_an_other_page = bool(soup.find(class_="next"))
        
        if there_is_an_other_page :
            next_page_anchor = soup.find(class_="next").find("a")
            next_page_url = urljoin(url, next_page_anchor["href"])
            url = next_page_url

        else :
            print("Pas trouvé, assurez vous que le titre soit correct.")
            return False

def scrap_book_data(page_url):
    soup = get_html(page_url)
    books_dictionnary = {}

    # Et on récolte toutes les données
    product_page_url = page_url 

    upc = soup.find("th", text="UPC").find_next_sibling("td").text.strip()

    title = soup.find("h1").text.strip()

    price_including_tax = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").text.strip()

    price_excluding_tax = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text.strip()

    stock_text = soup.find("th", text="Availability").find_next_sibling("td").text.strip()

    regex_match = re.search(r'\((\d+)', stock_text) #Regex pour sortir le nombre en stock
    if regex_match:
        number_available = regex_match.group(1)
    else:
        print(f"Stock Error : {page_url}")
        exit()

    there_is_a_description = bool(soup.find("div", id="product_description"))
    if there_is_a_description :
        product_description = soup.find("div", id="product_description").find_next("p").text.strip()
    else :
        product_description = "Pas de description."

    path_links = soup.find(class_="breadcrumb").find_all("a")

    category = path_links[2].text.strip()

    review_rating_in_letter = soup.find("p", class_="star-rating")["class"][1]
    match review_rating_in_letter :
        case "One" :
            review_rating = 1
        case "Two" :
            review_rating = 2
        case "Three" :
            review_rating = 3
        case "Four" :
            review_rating = 4
        case "Five" :
            review_rating = 5
        case _ :
            print(f"Rating Error : {page_url}")
            exit()

    image_url = urljoin(page_url, soup.find("img")["src"])

    # Maintenant que toutes les données ont été récoltés, les mettre en place 
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
        image_url=image_url
    )

    books_dictionnary[f"book_{upc}"] = book_data

    return books_dictionnary


    

