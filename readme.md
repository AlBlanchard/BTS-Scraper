# BTS Scraper

## Table des matières

- [BTS Scraper](#bts-scraper)
  - [Table des matières](#table-des-matières)
  - [Installation](#installation)
  - [Utilisation](#utilisation)
    - [help](#help)
    - [category](#category)
    - [search](#search)
    - [book](#book)
    - [Notes importantes](#notes-importantes)
      - [Sauvegarde des données](#sauvegarde-des-données)
  - [Exemples d'utilisation](#exemples-dutilisation)

## Installation

1. **Clonez le dépôt :**

    ```bash
    git clone https://github.com/AlBlanchard/BTS-Scraper.git
    ```

2. **Accédez au répertoire du projet :**

    ```bash
    cd BTS-Scraper
    ```

3. **Créez un environnement virtuel :**

    - **Windows :**

        ```bash
        python -m venv env
        ```

    - **macOS et Linux :**

        ```bash
        python3 -m venv env
        ```

4. **Installez les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

5. **Activez l'environnement virtuel :**

    - **Windows :**

        ```bash
        env\Scripts\activate
        ```

    - **macOS et Linux :**

        ```bash
        source env/bin/activate
        ```

## Utilisation

### help

- **Afficher l'aide dans le terminal :**

    ```bash
    python main.py help
    ```

    > Un mémo de toutes les commandes disponibles sera affiché dans la console.

- **Afficher toutes les catégories du site :**

    ```bash
    python main.py help category
    ```

    > Les catégories disponibles seront listées dans la console. Utile pour s'assurer de la bonne syntaxe avant de scraper une catégorie.

### category

- **Scraper les livres d'une catégorie spécifique :**

    ```bash
    python main.py category 'nom de la catégorie'
    ```

    > Entourez le nom de la catégorie avec des apostrophes (`''`) s'il contient plusieurs mots.

- **Scraper toutes les catégories :**

    ```bash
    python main.py category all
    ```

    > Cette opération peut être longue.

### search

- **Rechercher un livre via son titre (partiel ou complet), puis le scraper :**

    ```bash
    python main.py search 'nom du livre'
    ```

    > La recherche s'arrête à la première correspondance trouvée. Soyez donc précis.  
    > La fonction recherche les mots complets, dans n'importe quel ordre.

### book

- **Scraper directement un livre via son URL :**

    ```bash
    python main.py book 'url'
    ```

    > L'URL doit commencer par :  
    `<https://books.toscrape.com/catalogue/...>`

### Notes importantes

#### Sauvegarde des données

- Les données sont enregistrées dans un fichier `.csv` situé dans le dossier `datas_scraped`.
- Les images des couvertures des livres sont enregistrées dans :  
  `datas_scraped/images_books/'catégorie_du_livre'/`.  
  Chaque couverture est placée dans le dossier correspondant à sa catégorie.

⚠️ **Attention** : Lancer un nouveau scraping effacera les fichiers existants dans `datas_scraped` !

## Exemples d'utilisation

```bash
python main.py category 'Historical Fiction'
```

Scrap tous les livre de la catégorie 'Historical Fiction'

```bash
python main.py search "Harry Potter"
```

Scrap les données du premier livre Harry Potter trouvé, d'où l'importance d'être précis.
Si vous recherchez la chambre des secrets "Harry Potter chamber of secrets" fonctionnera.
Fonctionne également dans le désordre "chamber of secrets Harry Potter".

```bash
python main.py book <https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html>
```

Scrap les données du livre "A Light in the Attic"

**IMPORTANT** : Les entrées sont insensibles à la casse, pas besoin de se soucier des majuscules.
