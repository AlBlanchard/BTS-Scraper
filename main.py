from modules.get_it import get_html
from modules.scrap_it import scrap_product_url
from modules.scrap_it import all_category_dictionnary 
from urllib.parse import urljoin
from modules.get_it import SITE
import sys


if len(sys.argv) != 2:
    print("Erreur : Vous devez fournir exactement un argument.")
    sys.exit(1)

if sys.argv[1] in all_category_dictionnary :
    
    print("Scrap en cours...")

    url_to_scrap = urljoin(SITE, all_category_dictionnary[sys.argv[1]])
    page_soup = get_html(url_to_scrap)
    products_dictionnary = scrap_product_url(page_soup, url_to_scrap)

    print(products_dictionnary)

    exit()

else :
    print("Argument invalide")
    exit()



