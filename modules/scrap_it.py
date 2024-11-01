from modules.get_it import SITE
from urllib.parse import urljoin
from modules.get_it import get_html
from modules.get_it import HOME_SOUP

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

    all_products_h3 = soup.find_all("h3")

    for product in all_products_h3 : # va chercher toutes les uri vers les produits
        product_anchor = product.find("a")

        product_title = product_anchor["title"]   
        product_url = urljoin(page_url, product_anchor["href"]) #urljoin, fonction de base dans python, merveilleux pour contrer les url relatives .../.../...

        products_dictionnary[product_title] = product_url

    # L'idée est de vérifier s'il existe une autre page dans cette catégorie, si c'est le cas, refaire le processus

    there_is_an_other_page = bool(soup.find(class_="next"))

    if there_is_an_other_page :
        next_page_anchor = soup.find(class_="next").find("a")
        next_page_uri = next_page_anchor["href"]
        next_page_url = urljoin(page_url, next_page_uri)

        products_dictionnary.update(scrap_product_url(next_page_url))

        return products_dictionnary
    
    return products_dictionnary



    

