from modules.get_it import SITE
from urllib.parse import urljoin
from modules.get_it import get_html

def scrap_product_url(soup, actual_page_url, all_products_url_list) :
    
    all_products_h3 = soup.find_all("h3")

    print(actual_page_url)

    for product in all_products_h3 : # va chercher toutes les uri vers les produits
        product_link = product.find("a")

        if product_link and "href" in product_link.attrs : # change les uri en url exploitables pour les requêtes get
            
            product_url = urljoin(actual_page_url, product_link["href"]) #urljoin, fonction de base dans python, merveilleux pour contrer les url relatives .../.../...
            all_products_url_list.append(product_url)

    # L'idée est de vérifier s'il existe une autre page dans cette catégorie, si c'est le cas, refaire le processus

    there_is_an_other_page = bool(soup.find(class_="next"))

    if there_is_an_other_page :
        next_page_anchor = soup.find(class_="next").find("a")
        next_page_uri = next_page_anchor["href"]
        next_page_url = urljoin(actual_page_url, next_page_uri)

        print(next_page_url)

        next_page_soup = get_html(next_page_url)
        scrap_product_url(next_page_soup, next_page_url, all_products_url_list)

        return all_products_url_list
    
    return all_products_url_list

    

