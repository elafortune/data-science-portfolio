📁 Dataset

Chaque ligne correspond à un article présent dans une facture.
Variables principales utilisées :

-InvoiceDate : date et heure d'achat

-CustomerID : identifiant unique de client

-StockCode / Description : références produit

-Quantity : quantité commandée

-UnitPrice

-Price = Quantity × UnitPrice

-Country : pays du client

-InvoiceNo : identifiant facture (les annulations commencent par C)

🚀 1. Analyse RFM
Objectif : Comprendre la valeur client et préparer la segmentation.
✔️ Recency : Dernière date d’achat par client, Nombre de jours depuis le dernier achat
✔️ Frequency : Nombre total de factures, Nombre total d’articles achetés
✔️ Monetary : Montant total dépensé, Panier moyen / commande

🛒 2. Analyse du panier & valeur client
Objectif : Comprendre comment les clients achètent et identifier les profils à forte valeur.
✔️ KPI principaux : Panier moyen (€) par client, articles moyens par commande, taux de retour (quantités négatives), structure du panier,top clients (CA, quantité, marge)

🕒 3. Analyses temporelles
Basé sur InvoiceDate 
✔️ Saisonnalités : Ventes par jour, semaine, mois, année, impact du jour de la semaine, analyse par créneau horaire
✔️ Comportement de réachat : Délai moyen entre commandes, Variation annuelle du réachat, Identification des périodes chaudes / creuses

📦 4. Analyse produit
✔️ Performances produits : Top produits par CA, top produits par quantité vendue, produits générant le plus de marge, produits saisonniers, analyse de croissance (évolution des ventes dans le temps)

✔️ Market Basket Analysis : Produits fréquemment achetés ensemble, support de visualisation, intervalle de confiance

🌍 5. Analyse géographique
✔️ Avec la variable Country: Répartition du CA par pays (pie chart, bar chart), panier moyen par pays, taux de retour par pays, détection des pays premium vs low-cost, identification d’opportunités selon zones géographiques

👥 6. Analyse comportement d’achat
✔️ Fidélité : clients réguliers vs one-time buyers
✔️ Typologies comportementales : clients qui dépensent beaucoup mais achètent peu souvent, clients fréquents avec petit panier, clients inactifs (churn)
✔️ Churn Analysis : calcul de la recency, définition d’un seuil temporel (ex : > 90 jours), visualisation des clients churn / actifs
✔️ Clustering (KMeans) : Segmentation automatique basée sur RFM, KPIs client, variables comportementales

Exemples de clusters :
⭐ VIP (gros dépensiers, très actifs)
🔄 Clients réguliers
💸 Occasionnels
💤 Clients churn
🛍️ Gros paniers
🌍 Clusters géographiques

🚨 7. Analyse anomalies & fraudes
✔️ Détection : Factures annulées (InvoiceNo commençant par C), clients avec comportements atypiques, quantités anormalement élevées (fraude / erreur), prix aberrants (UnitPrice < 0 ou très élevé), produits avec taux de retour excessif

🧩 8. Feature Engineering (création de variables)
✔️ Variables client (quantité totale, quantité dépensée, nombre moyen d'articles par paniers,...)
✔️ Variables produit (retours moyens, produits les plus vendus,...)
✔️ Variables temporelles (Année,mois,jour de la semaine)

Résultat final : Segmentation client + insights business

Grâce à l’ensemble des analyses :

-Identification des clients à forte valeur
-Détection des clients churn
-Compréhension de la saisonnalité
-Mise en évidence des produits stratégiques
-Détection des opportunités de cross-sell (MBA)
-Construction de clusters client robustes

🛠️ Technologies utilisées : Python
 librairies : Pandas, Numpy, matplotlib, seaborn, plotly, mlxtend


📌 Améliorations possibles

-Modèle prédictif de churn (XGBoost / LightGBM)
-Imputation des valeurs manquantes
-Recommandation produit basée sur les profils (collaborative filtering)
-Dashboard interactif (Dash / Streamlit)
