
🧠 Imputation supervisée des valeurs manquantes : Year of Birth et Gender
📂 Présentation du projet
Ce projet vise à résoudre le problème de valeurs manquantes dans deux colonnes clés d’un jeu de données massif (~2 million de lignes) :

"yob" (year of birth / année de naissance)

"gender" (genre / sexe)

Plutôt que d’utiliser des méthodes classiques (suppression, moyenne, mode), j’ai appliqué une approche d’imputation supervisée en utilisant des modèles de machine learning. Chaque colonne a été traitée comme une variable cible à prédire à partir des autres colonnes disponibles.

🎯 Objectifs
Identifier et analyser les valeurs manquantes dans les colonnes "yob" et "gender".

Construire des modèles prédictifs pour estimer les valeurs manquantes.

Intégrer les prédictions dans le jeu de données pour améliorer sa qualité.

🛠️ Méthodologie
1. Exploration et nettoyage des données
Repérage des valeurs manquantes (yob == -1, gender == 'unknown' ou NaN).

Analyse des distributions, des corrélations, et de la qualité des features.

Prétraitement : encodage des variables catégorielles, normalisation si besoin.

2. Sélection des variables explicatives
Sélection de variables pertinentes pour prédire "yob" et "gender".

Suppression ou transformation de variables non informatives.

3. Modélisation supervisée
Imputation de "yob" :
➤ Modèle utilisé : LightGBM Classifier
➤ Prédiction de l’année de naissance comme un problème de classification multiclasses.

Imputation de "gender" :
➤ Modèle utilisé : Random Forest Classifier
➤ Prédiction binaire ou multiclasse du genre à partir d'autres attributs.

4. Évaluation des modèles
Séparation entraînement / validation.

Métriques utilisées : accuracy, matrice de confusion, analyse d’erreur.

5. Imputation finale
Prédiction des valeurs manquantes.

Remplacement dans le jeu de données original pour obtenir un dataset complet.

📈 Technologies utilisées
Python : pandas, numpy, scikit-learn, LightGBM, matplotlib, seaborn

Jupyter Notebook : pour le développement itératif

Random Forest & LightGBM : pour l’imputation supervisée

📊 Résultats
Colonnes imputées :

yob : ~40 % de valeurs manquantes remplacées (~800 000 lignes)

gender : ~40 % de valeurs manquantes remplacées (~800 000 lignes)

Performances des modèles :

yob : précision de ~2 % sur validation soit environ 2 fois plus que le remplissage au hasard des années de naissances

gender : précision de ~50 % soit également à une détermination au hasard du genre

Jeu de données final plus complet, cohérent et prêt pour l’analyse ou la modélisation.

🔍 Enseignements clés
L’imputation supervisée permet de mieux exploiter les données disponibles qu’une approche naïve.

Le choix des features est crucial pour obtenir des prédictions fiables.

Ce type d’approche est facilement généralisable à d’autres variables avec des valeurs manquantes.

