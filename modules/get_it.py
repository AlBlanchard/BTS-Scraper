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


def find_element(soup, tag, text=None, attributes=None, sibling=False):
    """
    Retourne un élément HTML en fonction des critères spécifiés : balise, texte, id, ou classe.
    Si sibling=True, retourne l'élément frère suivant.

    Arguments:
    soup -- L'objet BeautifulSoup.
    tag -- La balise HTML de l'élément.
    text -- Texte de l'élément (facultatif).
    attributes -- Dictionnaire contenant les attributs id et class (facultatif).
    sibling -- Si True, cherche l'élément frère suivant après l'élément trouvé (facultatif).

    Retourne:
    L'élément trouvé ou None si aucun élément ne correspond.
    """
    # Si le dictionnaire 'attributes' est None, on l'initialise comme un dictionnaire vide
    if attributes is None:
        attributes = {}

    # Recherche de l'élément en fonction de la balise, du texte, de l'id et de la classe
    element = soup.find(tag, text=text, **attributes)

    # Si sibling est True, retourne l'élément frère suivant
    if sibling and element:
        element = element.find_next_sibling()

    return element


def get_data_of_element(
    element, attr="text", default="Non renseigné(e)", sibling=False
):
    """
    Extrait les données d'un élément HTML,
    avec options pour récupérer un attribut spécifique ou un élément suivant.

    Arguments:
    element -- L'élément HTML trouvé.
    attr -- L'attribut à extraire (par défaut, texte de l'élément).
    default -- Valeur par défaut si l'élément ou l'attribut est introuvable.
    sibling -- Si True, extrait le texte de l'élément suivant.

    Retourne:
    La donnée extraite ou la valeur par défaut si l'élément est introuvable.
    """
    if not element:
        return default

    if sibling:
        element = element.find_next_sibling()
        return element.text.strip() if element else default

    return element.text.strip() if attr == "text" else element.get(attr, default)


def find_book_data_element(book_url):
    """
    Stock tous les éléments HTML en rapport avec les données du livre dans un dict.
    """

    soup = get_html(book_url)

    upc_element = find_element(soup, "th", text="UPC", sibling=True)
    title_element = find_element(soup, "h1")
    price_incl_tax_element = find_element(
        soup, "th", text="Price (incl. tax)", sibling=True
    )
    price_excl_tax_element = find_element(
        soup, "th", text="Price (excl. tax)", sibling=True
    )
    number_available_element = find_element(
        soup, "th", text="Availability", sibling=True
    )
    product_description_element = find_element(
        soup, "div", attributes={"id": "product_description"}, sibling=True
    )

    # Element de la categorie
    breadcrumb_element = find_element(soup, "ul", attributes={"class": "breadcrumb"})
    if breadcrumb_element:
        path_links = breadcrumb_element.find_all("a")
        category_element = path_links[2]
    else:
        category_element = None

    rating_element = find_element(soup, "p", attributes={"class": "star-rating"})

    image_element = find_element(soup, "img")

    return {
        "upc_element": upc_element,
        "title_element": title_element,
        "price_incl_tax_element": price_incl_tax_element,
        "price_excl_tax_element": price_excl_tax_element,
        "number_available_element": number_available_element,
        "product_description_element": product_description_element,
        "category_element": category_element,
        "rating_element": rating_element,
        "image_element": image_element,
    }
