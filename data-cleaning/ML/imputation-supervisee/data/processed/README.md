
# 📂 data/processed

Ce dossier contient les **données traitées** à partir des données brutes. Il comprend notamment :

- La version **complétée du dataset** après imputation supervisée des valeurs manquantes.
- Le **notebook Jupyter** utilisé pour effectuer l'imputation.

## Contenu

- `dataset_impute.csv` : version nettoyée et enrichie du dataset, sans valeurs manquantes dans les colonnes `"yob"` et `"gender"`.
- `imputation-supervisee.ipynb` : notebook contenant le code d’imputation supervisée à l’aide de modèles machine learning (LightGBM, RandomForest...).

## Détails des transformations

- Les valeurs `-1` dans `"yob"` ont été imputées par un modèle de classification multi-classes.
- Les valeurs `unknown` ou manquantes dans `"gender"` ont été prédictes par un modèle binaire/multiclasse.
- Les autres variables explicatives ont été nettoyées, encodées et normalisées si nécessaire.

## Bonnes pratiques

- Ce dossier est destiné à l’analyse finale ou à l’entraînement de modèles sur un dataset complet.
- Le notebook peut être relancé à tout moment pour reproduire les étapes d’imputation.
