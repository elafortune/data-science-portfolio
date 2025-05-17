
# 📁 data-cleaning/processed

Ce dossier contient les **données transformées et prêtes à être utilisées** après le processus de nettoyage initial effectué sur le dataset brut situé dans `data-cleaning/data/raw/`.

## 📄 Contenu

- Données FIFA nettoyées (`.csv` ou autre format)
- Index cohérents, types de données standardisés
- Variables texte nettoyées (ex : salaires convertis en entiers, unités unifiées)
- Valeurs manquantes traitées
- Colonnes numériques cohérentes (ex : normalisées, converties, etc.)

## 🧹 Origine

Les fichiers ici sont générés à partir du notebook :  
👉 [`notebook/data_cleaning.ipynb`](../notebook/data_cleaning.ipynb)

Le nettoyage inclut :
- Suppression ou traitement des valeurs manquantes
- Conversion des formats monétaires (`€`, `M`, `K`) en entiers
- Création de nouvelles colonnes utiles (ex : `score global`)
- Uniformisation des noms de colonnes

## 📌 Utilisation recommandée

Utilisez ces fichiers pour :
- L’analyse exploratoire (data-analysis)
- L’entraînement de modèles (machine-learning)
- La visualisation ou les dashboards (visualisation) dont des exemples ont été réalisé en fin de notebook

## ✅ Format des fichiers

| Fichier                          | Description                                 |
|----------------------------------|---------------------------------------------|
| `fifa_cleaned.csv`               | Données nettoyées prêtes à l’analyse        |
| `fifa_top_players.csv`           | (optionnel) Top joueurs filtrés ou scorés   |


## 🔄 Reproductibilité

Les données de ce dossier sont générées automatiquement à partir du script / notebook de nettoyage.  
Toute modification manuelle est à éviter :  
> 🔁 Relancer le notebook si mise à jour du dataset brut.


