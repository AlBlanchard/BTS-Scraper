import sys
from modules.scrap_it import scrap_product_url
from modules.get_it import SITE
from modules.scrap_it import all_category_dictionnary 
from urllib.parse import urljoin

def argv_lenght_filter(argv_list) :
        match len(argv_list) :
            case 1 :
                print("Scrap de tous les produits en cours...")
                scrap_product_url(SITE)
                exit()
            
            case 2 :
                if argv_list[1] not in ["category", "book", "infos"] :
                    print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation. 1")
                    exit()
                else :
                    print("Il manque un argument, veuillez vous repporter à la documentation.")
                    exit()

            case 3 :
                if argv_list[1] not in ["category", "book", "infos"] :
                    print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation. 2")
                    exit()
                else :
                    print("Scrap en cours...")

            case _ :
                print("Erreur : Trop d'arguments. Une belle documentation est là pour vous.")
                sys.exit(1)


def argv_check(argv_list) :

    match argv_list[1] :
        case "category" :
            if argv_list[2] in all_category_dictionnary :
                print("Scrap en cours de la categorie...")

                url_to_scrap = urljoin(SITE, all_category_dictionnary[argv_list[2]])
                products_dictionnary = scrap_product_url(url_to_scrap)

                print(products_dictionnary)
                exit()
            else :
                print(f"Erreur : la catégorie {argv_list[2]} n'existe pas. Pour avoir une liste des catégories : infos category.")
                exit()

        case "book" :
            print("Scrap en cours du livre...")
            exit()

        case "infos" :
            print("Voici les infos demandés...")
            exit()
        
        case _ :
            print(f"L'argument {argv_list[1]} est invalide. Rapprochez vous de la documentation.")
            exit()