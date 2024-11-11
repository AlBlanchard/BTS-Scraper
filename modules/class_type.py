"""
La classe Book est un objet de données qui stocke les informations d'un livre.
"""


class Book:
    """
    Stocke les informations d'un livre.
    """

    # Code de la classe Bookclass Book:
    def __init__(
        self,
        product_page_url,
        upc,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url,
        image_path=None,
    ):
        self.product_page_url = product_page_url
        self.upc = upc
        self.title = title
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url
        self.image_path = image_path

    def __str__(self):
        return f"Book(title={self.title}, url={self.product_page_url}, upc={self.upc})"
