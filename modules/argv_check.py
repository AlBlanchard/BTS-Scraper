import sys
from modules.scrap_it import scrap_product_url
from modules.get_it import SITE
from modules.scrap_it import all_category_dictionnary 
from urllib.parse import urljoin
from modules.scrap_it import search_book_name_and_url

# Permet de vérifier si l'utilisateur a rentrer un nombre d'argument possible pour executer le script. Renvois le nombre d'arguments pour que le main sache quoi faire. 
def validate_script_arguments(argv_list):
    valid_arguments = ["category", "book", "infos"]
    
    if len(argv_list) == 1:
        return True

    if len(argv_list) > 3:
        print("Erreur : Trop d'arguments. Une belle documentation est là pour vous.")
        return False

    if argv_list[1] not in valid_arguments:
        print(f"L'argument {argv_list[1]} est invalide.")
        if len(argv_list) == 2:
            print("ET il manque un argument. Rapprochez-vous de la documentation.")
        return False

    if len(argv_list) == 2:
        print("Il manque un argument, veuillez vous reporter à la documentation.")
        return False

    return True


def argv_check(argv_list) :

    match argv_list[1] :
        case "category" :
            if argv_list[2] in all_category_dictionnary :
                print("Recherce en cours de la categorie...")

                url_to_scrap = urljoin(SITE, all_category_dictionnary[argv_list[2]])
                products_dictionnary = scrap_product_url(url_to_scrap)

                print(products_dictionnary)
                exit()
            else :
                print(f"Erreur : la catégorie {argv_list[2]} n'existe pas. Pour avoir une liste des catégories : infos category.")
                exit()

        case "book" :
            search_book_name_and_url(sys.argv[2])
            exit()

        case "infos" :
            print("Voici les infos demandés...")
            exit()
        
        case _ :
            print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation.")
            exit()