import sys
from modules.scrap_it import scrap_product_url
from modules.get_it import SITE
from modules.scrap_it import all_category_dictionnary 
from urllib.parse import urljoin
from modules.scrap_it import search_book_name

# Permet de vérifier si l'utilisateur a rentrer un nombre d'argument possible pour executer le script. Renvois le nombre d'arguments pour que le main sache quoi faire. 
def entry_correct(argv_list) :
        match len(argv_list) :
            case 1 :
                return True
            
            case 2 :
                if argv_list[1] not in ["category", "book", "infos"] :
                    print(f"L'argument {argv_list[1]} est invalide ET il manque un argument. Rapprochez vous de la documentation.")
                    return False
                else :
                    print("Il manque un argument, veuillez vous repporter à la documentation.")
                    return False

            case 3 :
                if argv_list[1] not in ["category", "book", "infos"] :
                    print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation. 2")
                    return False
                    
                else :
                    return True

            case _ :
                print("Erreur : Trop d'arguments. Une belle documentation est là pour vous.")
                return False


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
            search_book_name(sys.argv[2], SITE)
            exit()

        case "infos" :
            print("Voici les infos demandés...")
            exit()
        
        case _ :
            print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation.")
            exit()