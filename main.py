from modules.get_it import get_html
from modules.scrap_it import scrap_product_page_url

home_soup = get_html("index.html")

scrap_product_page_url(home_soup)