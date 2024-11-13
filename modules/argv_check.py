"""
Ce module contient la fonction nécessaire pour vérifier les arguments passés au script.
Contient également deux fonctions d'aide pour afficher des informations sur l'utilisation du script.

Fonctions:
    - validate_script_arguments(argv_list)
    - print_help()
    - print_help_category()

"""

from etl.extract import extract_category


def validate_script_arguments(argv_list):
    """
    Valide les arguments passés au script.

    Parametres:
        argv_list (list): La liste des arguments en ligne de commande.
    Returns:
        bool: True si les arguments sont valides, sinon False.
    """

    valid_arguments = {"category", "book", "help", "search"}

    if len(argv_list) == 1:
        print(
            "Erreur : ce script nécessite au moins un argument supplémentaire.\n"
            "'python main.py help' pour plus d'informations ou consultez la documentation."
        )
        return False

    if len(argv_list) > 3:
        print(
            "Erreur : Trop d'arguments.\n"
            "'python main.py help' pour plus d'informations ou consultez la documentation."
        )
        return False

    if argv_list[1] not in valid_arguments:
        print(
            f"L'argument '{argv_list[1]}' est invalide.\n"
            "'python main.py help' pour plus d'informations ou consultez la documentation."
        )
        return False

    if len(argv_list) == 2 and argv_list[1] == "category":
        print(
            "Erreur : L'argument 'category' nécessite un argument supplémentaire.\n"
            "'python main.py help' pour plus d'informations ou consultez la documentation."
        )
        return False

    return True


def print_help():
    """Affiche une petite aide pour utiliser le script."""
    print(
        "\n"
        "Voici comment exécuter les différentes fonctions du script :\n\n"
        "main.py category 'nom_de_la_catégorie'\n"
        "-> Scrape les livres d'une catégorie spécifique.\n\n"
        "main.py category all\n"
        "-> Scrape tous les livres de toutes les catégories, cette opération est longue.\n\n"
        "main.py search 'nom_du_livre'\n"
        "-> Cherche le livre qui correspond, puis le scrap. Soyez le plus précis possible.\n"
        "-> Le premier livre trouvé sera scrapé.\n\n"
        "main.py book 'url_du_livre'\n"
        "-> Scrape un livre via son URL.\n\n"
        "main.py help category\n"
        "-> Affiche toutes les catégories du site dans la console.\n"
    )


def print_help_category():
    """Affiche toutes les catégories du site dans la console."""
    all_category_dictionnary = extract_category()
    print("\nVoici toutes les catégories du site :\n")
    for category in all_category_dictionnary:
        print(category.capitalize())
