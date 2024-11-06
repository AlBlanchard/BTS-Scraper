"""

Module comportant deux fonctions de validation des arguments.

"""


def validate_script_arguments(argv_list):
    """
    Valide les arguments passés au script.

    Parametres:
        argv_list (list): La liste des arguments en ligne de commande.
    Returns:
        bool: True si les arguments sont valides, sinon False.
    """

    valid_arguments = {"category", "book", "infos"}

    if len(argv_list) == 1:
        print(
            "Erreur : ce script nécessite au moins un argument supplémentaire.\n"
            "'python main.py infos' pour plus d'informations ou consultez la documentation."
        )
        return False

    if len(argv_list) > 3:
        print(
            "Erreur : Trop d'arguments.\n"
            "'python main.py infos' pour plus d'informations ou consultez la documentation."
        )
        return False

    if argv_list[1] not in valid_arguments:
        print(
            f"L'argument '{argv_list[1]}' est invalide.\n"
            "'python main.py infos' pour plus d'informations ou consultez la documentation."
        )
        return False

    if argv_list[1] in {"category", "book"} and len(argv_list) == 2:
        print(
            f"L'argument '{argv_list[1]}' nécessite un argument supplémentaire.\n"
            "'python main.py infos' pour plus d'informations ou consultez la documentation."
        )
        return False

    return True
