class Book:
    def __init__(self, product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
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

    def __str__(self):
        return f"Book(title={self.title}, price tax={self.price_including_tax}, price no tax={self.price_excluding_tax}, available={self.number_available}, upc={self.upc}, category={self.category}, rating={self.review_rating}, img url={self.image_url})"