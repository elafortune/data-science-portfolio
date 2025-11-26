📁 Dataset

Chaque ligne correspond à un article présent dans une facture.
Variables principales utilisées :

InvoiceDate : date et heure d'achat

CustomerID : identifiant unique de client

StockCode / Description : références produit

Quantity : quantité commandée

UnitPrice

Price = Quantity × UnitPrice

Country : pays du client

InvoiceNo : identifiant facture (les annulations commencent par C)

🚀 1. Analyse RFM

Objectif : Comprendre la valeur client et préparer la segmentation.

✔️ Recency

Dernière date d’achat par client

Nombre de jours depuis le dernier achat

✔️ Frequency

Nombre total de factures

Nombre total d’articles achetés

✔️ Monetary

Montant total dépensé

Panier moyen / commande

🛒 2. Analyse du panier & valeur client
✔️ KPI principaux

Panier moyen (€) par client

Articles moyens par commande

Taux de retour (quantités négatives)

Structure du panier

Top clients (CA, quantité, marge)

Objectif : Comprendre comment les clients achètent et identifier les profils à forte valeur.

🕒 3. Analyses temporelles

Basé sur InvoiceDate :

✔️ Saisonnalités

Ventes par jour, semaine, mois, année

Impact du jour de la semaine

Analyse par créneau horaire

✔️ Comportement de réachat

Délai moyen entre commandes

Variation annuelle du réachat

Identification des périodes chaudes / creuses

📦 4. Analyse produit
✔️ Performances produits

Top produits par CA

Top produits par quantité vendue

Produits générant le plus de marge

Produits saisonniers

Analyse de croissance : évolution des ventes dans le temps

✔️ Market Basket Analysis

Apriori

Produits fréquemment achetés ensemble

Visualisation support / confidence / lift

🌍 5. Analyse géographique
✔️ Avec la variable Country:

Répartition du CA par pays (pie chart, bar chart)

Panier moyen par pays

Taux de retour par pays

Détection des pays premium vs low-cost

Identification d’opportunités selon zones géographiques

👥 6. Analyse comportement d’achat
✔️ Fidélité

Clients réguliers vs one-time buyers

✔️ Typologies comportementales

Clients qui dépensent beaucoup mais achètent peu souvent

Clients fréquents avec petit panier

Clients inactifs (churn)

✔️ Churn Analysis

Calcul de la recency

Définition d’un seuil (ex : > 90 jours)

Visualisation des clients churn / actifs

✔️ Clustering (KMeans)

Segmentation automatique basée sur :

RFM

KPIs client

Variables comportementales

Exemples de clusters :

⭐ VIP (gros dépensiers, très actifs)

🔄 Clients réguliers

💸 Occasionnels

💤 Clients churn

🛍️ Gros paniers

🌍 Clusters géographiques

🚨 7. Analyse anomalies & fraudes
✔️ Détection :

Factures annulées (InvoiceNo commençant par C)

Clients avec comportements atypiques

Quantités anormalement élevées (fraude / erreur)

Prix aberrants (UnitPrice < 0 ou très élevé)

Produits avec taux de retour excessif

🧩 8. Feature Engineering (création de variables)
✔️ Variables client

Total_Spent

Total_Quantity

Avg_Basket_Value

Avg_Items_Per_Basket

Return_Rate

Days_Since_First_Purchase

Days_Since_Last_Purchase

✔️ Variables produit

Revenue_per_Product

Avg_Price_per_Product

Return_Rate_per_Product

✔️ Variables temporelles

Month, Week, Day_of_Week

Season (Winter, Spring, Summer, Fall)

Ces features sont utilisées pour les analyses avancées & le clustering.

🎯 Résultat final : Segmentation client + insights business

Grâce à l’ensemble des analyses :

Identification des clients à forte valeur

Détection des clients churn

Compréhension de la saisonnalité

Mise en évidence des produits stratégiques

Détection des opportunités de cross-sell (MBA)

Construction de clusters client robustes

🛠️ Technologies utilisées

Python (Pandas, NumPy)

Matplotlib / Seaborn / Plotly

Scikit-Learn (KMeans, PCA)

mlxtend (Apriori)

Jupyter Notebook

📌 Améliorations futures

Modèle prédictif de churn (XGBoost / LightGBM)

Recommandation produit basée sur les profils (collaborative filtering)

Dashboard interactif (Dash / Streamlit)
