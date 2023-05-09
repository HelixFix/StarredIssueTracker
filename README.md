# StarredIssueTracker

StarredIssueTracker est un outil open-source qui permet aux utilisateurs de rechercher facilement les issues ayant une étiquette particulière dans leurs dépôts étoilés sur GitHub. Grâce à cette application, les utilisateurs peuvent filtrer les issues en fonction de leurs étiquettes, puis afficher une liste des résultats correspondants pour leurs dépôts étoilés. Cette application est particulièrement utile pour les développeurs qui souhaitent trouver des problèmes ouverts dans les projets qu'ils suivent, afin de contribuer ou de mieux comprendre le code source.

## Installation

1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances en exécutant `pip install -r requirements.txt`.
3. Créez un fichier `.env` à la racine du projet et ajoutez vos informations d'identification GitHub en utilisant les noms de variable `GITHUB_USERNAME` et `TOKEN`.
4. Exécutez le script `main.py`.

## Utilisation

1. Au lancement, l'application vous demandera le nom de l'étiquette à rechercher.
2. L'application récupérera ensuite les informations d'identification à partir du fichier `.env` et listera tous les dépôts étoilés associés au compte utilisateur.
3. L'utilisateur doit sélectionner les dépôts qu'il souhaite analyser pour trouver les issues avec l'étiquette demandée.
4. L'application affichera ensuite une liste des issues correspondantes pour chaque dépôt sélectionné.

## Contributions

Les contributions sont les bienvenues ! Si vous trouvez un bug ou souhaitez ajouter une fonctionnalité, n'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
