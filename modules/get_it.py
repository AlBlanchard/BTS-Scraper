"""

Ici une fonction get_html() est définie pour récupérer le contenu HTML d'une page web. 

Il y a aussi deux constante SITE et HOME_SOUP qui sont définies pour stocker l'URL 
du site et le contenu HTML de la page d'accueil du site.

"""

import sys
import requests
from bs4 import BeautifulSoup


def get_html(url, dont_stop=False):
    """
    Cette fonction utilise la librairie requests pour envoyer une requête HTTP à l'URL en paramètre.
    Si la requête est un succès, le contenu est retourné sous forme de soup (objet BeautifulSoup).
    Si la requête échoue, le script s'arrête et affiche un message d'erreur.

    """

    # Try/Except pour gérer les erreurs de connexion.
    # Important pour stabiliser le code.
    try:
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            return soup

        # Permet de ne pas arrêter le script quand l'argument dont_stop est True.
        # Par défault, il est False.
        if dont_stop is True:
            return False

        print("Get Error : ", response.status_code, " aie aie aie")
        sys.exit()

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}, aie aie aie")
        sys.exit()


SITE = "https://books.toscrape.com/"
HOME_SOUP = get_html(SITE)
