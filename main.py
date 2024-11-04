from modules.get_it import get_html
from modules.scrap_it import scrap_product_url
from modules.scrap_it import all_category_dictionnary 
from urllib.parse import urljoin
from modules.get_it import SITE
from modules.argv_check import entry_correct
from modules.argv_check import argv_check
from modules.scrap_it import search_book_name
import sys
from modules.scrap_it import scrap_book_data

scrap_book_data("https://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html")
exit()

if not entry_correct(sys.argv) :
    exit()

if len(sys.argv) == 1 :
    books_url_dictionnary = scrap_product_url(SITE)
    books_dictionnary = {}

    book_numb = 1
    total_of_books_to_scrap = len(books_url_dictionnary)

    for book_url in books_url_dictionnary.values() :
        print(f"Scrap book {book_numb} of {total_of_books_to_scrap}")
        books_dictionnary.update(scrap_book_data(book_url))
        book_numb += 1

    print(books_dictionnary)



