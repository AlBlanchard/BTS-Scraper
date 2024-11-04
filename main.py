from modules.scrap_it import scrap_product_url
from modules.scrap_it import all_category_dictionnary 
from modules.get_it import SITE
from modules.argv_check import validate_script_arguments
from modules.scrap_it import books_url_dictionnary_scraping
import sys
from modules.scrap_it import scrap_book_data
from modules.scrap_it import scrap_category
from modules.scrap_it import search_book_name_and_url
from modules.save_it import save_books_to_csv

#scrap_book_data("https://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html")
#exit()

if not validate_script_arguments(sys.argv) :
    exit()

if len(sys.argv) == 1 :
    books_url_dictionnary = scrap_product_url(SITE)
    books_dictionnary = books_url_dictionnary_scraping(books_url_dictionnary)

elif sys.argv[1] == "category" :
    argv_category = sys.argv[2]
    all_category_dictionnary = scrap_category() 

    if argv_category in all_category_dictionnary :
        books_url_dictionnary = scrap_product_url(all_category_dictionnary[argv_category])
        books_dictionnary = books_url_dictionnary_scraping(books_url_dictionnary)
        
        save_books_to_csv(books_dictionnary)

    else :
        print(f"La catégorie {argv_category} n'existe pas. Pour avoir une liste des catégories : infos category")
        exit()

elif sys.argv[1] == "book" :
    argv_book_name = sys.argv[2]
    book_url = search_book_name_and_url(argv_book_name)
    book_data = scrap_book_data(book_url)

    save_books_to_csv(book_data)

else :
    exit()


