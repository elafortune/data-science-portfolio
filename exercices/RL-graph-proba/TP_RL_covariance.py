import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity

# Paramètres du modèle
mu_0 = 2  # Moyenne de la distribution p0 (différente de zéro)
sigma_0 = 1  # Ecart type de la distribution p0
gamma_0 = mu_0**2 + sigma_0**2
# Générer un ensemble de données suivant p0 (distribution normale N(mu_0, sigma_0^2))
n = 1000  # Taille de l'échantillon
real_data = np.random.normal(mu_0, sigma_0**2, n) #donnée réelle gaussienne de moyenne mu_0 et variance sigma_0


mispecified_data = np.random.normal(0, gamma_0, n) #modèle mal spécificié car mu_0 non nul, gamma_0 paramètre pseudo vrai

# Calcul de l'estimateur gamma_mvm = 1/n * somme des xi²
gamma_mvm = np.mean(mispecified_data**2)




# Calcul de la MCRB pour gamma_0
mcrb = (2 * sigma_0**4 + 4 * sigma_0**2 * mu_0**2) / n


# 1) montrer que l'estimateur gamma_mvm est non biaisé

#Calcul de l'espérance de gamma_MVM pour retrouver le résultat théorique E0_gamma_mvm_theorique = mu_0**2 + sigma_0**2

N_simulations = 10000  # Nombre de simulations pour estimer l'espérance

# Initialisation d'une liste pour stocker les résultats des simulations
estimates = []

# Effectuer plusieurs simulations
for _ in range(N_simulations):
    # Générer un échantillon de taille n selon N(mu_0, gamma_0)
    data = np.random.normal(0, gamma_0, n)
    
    # Calculer l'estimateur gamma_MVM pour cet échantillon
    gamma_mvm2 = np.mean(data**2)
    
    # Ajouter l'estimateur à la liste des résultats
    estimates.append(gamma_mvm2)

# Convertir la liste en un tableau numpy pour les calculs
estimates = np.array(estimates)

# Calculer l'espérance empirique de gamma_MVM
E0_gamma_mvm_empirique = np.mean(estimates)

# Afficher l'espérance théorique et empirique
E0_gamma_mvm_theorique = mu_0**2 + sigma_0**2



# 2) montrer que la MCRB est une limite inférieure POUR L'EQM de gamma_mvm

n_values = np.arange(1, 1001, 10)  # Taille de l'échantillon (de 1 à 1000)

# Calcul de la MCRB pour différentes tailles d'échantillon
mcrb_values = (2 * sigma_0**4 + 4 * sigma_0**2 * mu_0**2) / n_values

# Calcul de l'EQM pour différentes tailles d'échantillon
eqm_values = (2 * sigma_0**4 / n_values) + (mu_0**2)**2  # Var + Biais^2

# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.plot(n_values, eqm_values, label='EQM de γ_MVM,n', color='blue')
plt.plot(n_values, mcrb_values, label='MCRB(γ_0)', color='red', linestyle='--')

# Ajouter des étiquettes et un titre
plt.xlabel('Taille de l\'échantillon (n)')
plt.ylabel('Erreur quadratique moyenne (EQM) / MCRB')
plt.title('Comparaison de l\'EQM de γ_MVM,n et de la MCRB(γ_0)')
plt.legend()

# Affichage du graphique
plt.grid(True)
plt.show()



# 3) montrer que l'estimateur est bien efficace ie qu'il atteint la borne de cramer rao


# 4) montrer que la valeur minimale de l'EQM et de la MCRB est trouvée pour mu_0=0

n = 1000  # Taille de l'échantillon

# Plage de valeurs pour mu_0
mu_0_values = np.linspace(-3, 3, 500)

# Calcul de l'EQM pour chaque valeur de mu_0
eqm_values = (2 * sigma_0**4 / n) + mu_0_values**4

# Calcul de la MCRB pour chaque valeur de mu_0
mcrb_values = (2 * sigma_0**4 + 4 * sigma_0**2 * mu_0_values**2) / n

# Tracer les deux courbes
plt.figure(figsize=(10, 6))
plt.plot(mu_0_values, eqm_values, label='EQM de γ_MVM,n', color='blue')
plt.plot(mu_0_values, mcrb_values, label='MCRB(γ_0)', color='red', linestyle='--')

# Ajouter des étiquettes et un titre
plt.xlabel('µ₀ (Moyenne de la distribution)')
plt.ylabel('Erreur quadratique moyenne (EQM) / MCRB')
plt.title('Comportement de l\'EQM et de la MCRB en fonction de µ₀')
plt.legend()