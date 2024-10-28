from modules.get_it import SITE

def scrap_product_page_url(soup) :
    
    all_products_h3 = soup.find_all("h3")

    all_products_url = []

    for product in all_products_h3 :
        product_link = product.find("a")

        if product_link and "href" in product_link.attrs :
            product_url = SITE + product_link["href"]

            all_products_url.append(product_url)

    print(all_products_url)

