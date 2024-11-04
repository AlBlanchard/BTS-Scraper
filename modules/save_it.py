import csv

def save_books_to_csv(books_dictionnary, filename="books_data.csv"):
    # Définir les noms de colonnes
    fieldnames = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax", 
                  "number_available", "product_description", "category", "review_rating", "image_url"]

    # Ouvrir le fichier en mode écriture
    with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire les en-têtes
        writer.writeheader()
        
        # Écrire les données de chaque objet Book dans le fichier CSV
        for book in books_dictionnary.values():
            writer.writerow({
                "product_page_url": book.product_page_url,
                "upc": book.upc,
                "title": book.title,
                "price_including_tax": book.price_including_tax,
                "price_excluding_tax": book.price_excluding_tax,
                "number_available": book.number_available,
                "product_description": book.product_description,
                "category": book.category,
                "review_rating": book.review_rating,
                "image_url": book.image_url
            })

    print(f"Les données ont été enregistrées dans {filename}")