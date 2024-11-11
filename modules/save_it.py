"""

Ce module contient les fonctions qui permettent de sauvegarder les données scrapées.
Sauvegarde du csv et des images, création des dossiers.

"""

import csv
from pathlib import Path
import shutil
import requests
from modules.data_cleaner import clean_title


def save_books_to_csv(books_dictionary, filename="datas_scraped/books_data.csv"):
    """Sauvegarde les données scrapées dans un fichier CSV."""

    fieldnames = [
        "Lien vers le livre",
        "UPC",
        "Titre",
        "Prix TTC (en Livre)",
        "Prix HT (en Livre)",
        "Nombre en stock",
        "Description du livre",
        "Catégorie",
        "Note",
        "URL de la couverture",
        "Chemin vers la couverture",
    ]

    # Ouverture du fichier CSV pour écrire les informations
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for book in books_dictionary.values():
            writer.writerow(
                {
                    "Lien vers le livre": book.product_page_url,
                    "UPC": book.upc,
                    "Titre": book.title,
                    "Prix TTC (en Livre)": book.price_including_tax,
                    "Prix HT (en Livre)": book.price_excluding_tax,
                    "Nombre en stock": book.number_available,
                    "Description du livre": book.product_description,
                    "Catégorie": book.category,
                    "Note": book.review_rating,
                    "URL de la couverture": book.image_url,
                    "Chemin vers la couverture": book.image_path,
                }
            )

    print(f"Les données ont été enregistrées dans {filename}")


def download_image(book):
    """Télécharge l'image du livre et l'enregistre dans le dossier correspondant."""

    base_folder = Path("datas_scraped") / "images_books"

    # Dossier catégorie
    category_folder = base_folder / book.category
    category_folder.mkdir(parents=True, exist_ok=True)

    # Nettoie le titre du livre
    cleaned_title = clean_title(book.title)

    # Télécharge et enregistre la couverture
    image_path = category_folder / f"cover_{book.upc}_{cleaned_title}.jpg"

    if not image_path.exists():
        response = requests.get(book.image_url, timeout=10)

        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

    # Ajoute le chemin relatif comme donnée, cela fonctionne même si le champ n'existe pas dans la classe.
    # Mais la convention PEP recommande de garder un champ "None".
    book.image_path = str(image_path)


def clear_previous_data(folder_path="datas_scraped"):
    """Efface les données précédentes pour éviter les doublons."""

    if Path(folder_path).exists():
        shutil.rmtree(folder_path)

    Path(folder_path).mkdir(parents=True, exist_ok=True)
