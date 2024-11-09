import re


def clean_price(price_text):
    """Retire le symbole £ des prix."""
    return price_text.replace("£", "").strip() if price_text else "Non renseigné(e)"


def clean_stock(stock_text):
    """Extrait le nombre de livres disponibles en stock."""
    match = re.search(r"\((\d+)", stock_text)
    return match.group(1) if match else "Non renseigné(e)"


def clean_rating(rating_text):
    """Convertit la notation en lettres en un chiffre correspondant."""
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return rating_map.get(rating_text, "Non renseigné(e)")


def clean_title(title):
    """
    Nettoie le titre du livre pour l'utiliser dans le nom de fichier.
    Remplace les caractères spéciaux par des underscores.
    """
    # Remplace les caractères non alphanumériques par des underscores
    cleaned_title = re.sub(r"\W+", "_", title)
    return cleaned_title
