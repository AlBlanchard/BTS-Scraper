import requests
from bs4 import BeautifulSoup

SITE = "https://books.toscrape.com/"

def get_html(url) :
    response = requests.get(url)

    if response.status_code == 200 :
        print("Réponse : Statut 200, OK !")

        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        return soup
    
    else :
        print("Erreur : ", response.status_code, " aie aie aie")