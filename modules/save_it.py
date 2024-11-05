import csv
from pathlib import Path
import requests
import shutil


def save_books_to_csv(books_dictionary, filename="datas_scraped/books_data.csv"):

    fieldnames = [
        "Lien vers le livre", "UPC", "Titre", "Prix TTC (en Livre)", 
        "Prix HT (en Livre)", "Nombre en stock", "Description du livre", 
        "Catégorie", "Note", "URL de la couverture", "Chemin vers la couverture"
    ]

    # Ouverture du fichier CSV pour écrire les informations
    with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for book in books_dictionary.values():
            writer.writerow({
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
                "Chemin vers la couverture": book.image_path
            })

    print(f"Les données ont été enregistrées dans {filename}")


def download_image(book) :

    base_folder = Path("datas_scraped") / "images_books"

    # Dossier catégorie
    category_folder = base_folder / book.category
    category_folder.mkdir(parents=True, exist_ok=True)

    # Sous-dossier nommé par l'UPC du livre
    book_folder = category_folder / book.upc
    book_folder.mkdir(parents=True, exist_ok=True)

    # Télécharge et enregistre la couverture
    image_path = book_folder / f"cover_{book.upc}.jpg"

    if not image_path.exists() :
        response = requests.get(book.image_url)

        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

    # Ajoute le chemin relatif comme donnée, cela fonctionne même si le champs n'existe pas dans la class. Mais la convention PEP recommande de garder un champs "None". 
    book.image_path = str(image_path)


def clear_previous_data(folder_path="datas_scraped") :

    if Path(folder_path).exists() :
        shutil.rmtree(folder_path)

    Path(folder_path).mkdir(parents=True, exist_ok=True)

def save_it(books_dictionnary) :

    clear_previous_data()
    
    for book in books_dictionnary.values() :
        download_image(book)

    save_books_to_csv(books_dictionnary)