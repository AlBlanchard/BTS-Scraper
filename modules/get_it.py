import requests
from bs4 import BeautifulSoup


def get_html(url) :
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code == 200 :
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        return soup
    
    else :
        print("Get Error : ", response.status_code, " aie aie aie")
        exit()


SITE = "https://books.toscrape.com/"
HOME_SOUP = get_html(SITE)