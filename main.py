from modules.get_it import get_html
from modules.scrap_it import scrap_product_url
from urllib.parse import urljoin
from modules.get_it import SITE

all_products_url_list = []

page_category_uri = "catalogue/category/books/travel_2/index.html"

url_to_scrap = urljoin(SITE, page_category_uri)

home_soup = get_html(url_to_scrap)

scrap_product_url(home_soup, url_to_scrap, all_products_url_list)

print(all_products_url_list)