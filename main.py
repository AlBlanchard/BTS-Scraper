"""
Le main comprend uniquement deux grandes conditions :

-> La première vérifie si les arguments constants entrés sont valides. 

-> La deuxième condition vérifie si les arguments variables sont valides, 
puis lance le script en fonction des arguments.

"""

import sys
from modules.argv_check import (
    validate_script_arguments,
    print_help,
    print_help_category,
)
from modules.scrap_it import (
    scrap_category,
    scrap_book_from_research,
    scrap_book_from_url,
)


def main():
    """Fonction principale du script."""
    # Vérifie si les arguments passés au script sont valides.
    if not validate_script_arguments(sys.argv):
        sys.exit()

    # Lance le script en fonction des arguments passés.
    if len(sys.argv) == 2:
        # Affiche une petite aide pour utiliser le script.
        if sys.argv[1].lower() == "help":
            print_help()
    elif len(sys.argv) == 3:
        if sys.argv[1].lower() == "help" and sys.argv[2].lower() == "category":
            print_help_category()
        elif sys.argv[1].lower() == "category":
            scrap_category(sys.argv[2])
        elif sys.argv[1].lower() == "search":
            scrap_book_from_research(sys.argv[2].lower())
        elif sys.argv[1].lower() == "book":
            scrap_book_from_url(sys.argv[2].lower())
        else:
            print(f"L'argument {sys.argv[2]} est invalide.")


if __name__ == "__main__":
    main()
