# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:15:47 2024

@author: emeri
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 18:11:26 2023

@author: emeri
"""
#L'objectif de ce programme est de pouvoir évaluer le prix d'une option dans le modèle de Black & Scholes avec une méthode type monte-carlo
# le prix de l'option est calculé pour les différents type d'option et pour l'option napoléon on trouve également l'erreur à 99% et un graphique de convergence du monte-carlo
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, Canvas, Toplevel
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.stats import norm
from scipy.integrate import quad
from tkinter import ttk

# Fonctions de calcul

#1) option vanille

def option_vanille(type_option,K,r,T,sigma,S0,iteration):
   np.random.seed(45)
   dt= T/iteration
   W=np.random.normal(0,1,45)
   S= S0*np.exp(np.cumsum((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*W)) 
   # calcul du prix des actions à l'aide de l'équation de diffusion
   if type_option=="call" :
       payoff=max(S-K,0)
       
   elif type_option=="put":
       payoff=max(K-S,0)
   else:
       print("Error option")
   
   prix_option= np.exp(-r*T)*np.mean(payoff)
  
   return prix_option

# modele volatilité locale de Dupire

def solve_dupire_local_volatility(S0, K, T, r, market_prices, strikes, maturities):
    # Parameters
    M = len(strikes)
    N = len(maturities)

    # Discretization
    ds = strikes[1] - strikes[0]
    dt = maturities[1] - maturities[0]

    # Initialize the grid for option prices
    option_prices = np.zeros((M, N))

    # Market prices matrix
    market_matrix = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            market_matrix[i, j] = market_prices[i * N + j]

    # Time-stepping loop to solve the local volatility PDE
    for j in range(1, N):
        for i in range(1, M - 1):
            # Central finite difference for the second spatial derivative
            d2C_ds2 = (option_prices[i + 1, j - 1] - 2 * option_prices[i, j - 1] + option_prices[i - 1, j - 1]) / ds**2

            # Dupire's PDE for local volatility
            option_prices[i, j] = option_prices[i, j - 1] + r * S0 * (K - strikes[i]) / strikes[i] * option_prices[i, j - 1] * dt + \
                                  0.5 * S0**2 * strikes[i]**2 * (d2C_ds2 / option_prices[i, j - 1]) * dt

        # Apply boundary conditions
        option_prices[0, j] = 2 * option_prices[1, j] - option_prices[2, j]
        option_prices[M - 1, j] = 2 * option_prices[M - 2, j] - option_prices[M - 3, j]

    return option_prices

# Parameters
S0 = 100  # Initial stock price
K = 100  # Strike price
T = 1  # Time to maturity
r = 0.05  # Risk-free rate

# Market data (example)
strikes = np.linspace(80, 120, 11)
maturities = np.linspace(0.1, 1, 10)
market_prices = np.random.rand(len(strikes) * len(maturities)) * 10  # Random market prices for illustration

# Solve Dupire's local volatility PDE
option_prices = solve_dupire_local_volatility(S0, K, T, r, market_prices, strikes, maturities)

# Plot the results
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
M, N = np.meshgrid(strikes, maturities)
ax.plot_surface(M, N, option_prices, cmap='viridis')
ax.set_xlabel('Strike')
ax.set_ylabel('Maturity')
ax.set_zlabel('Option Price')
ax.set_title('Dupire\'s Local Volatility Model')

plt.show()


#2) option tunnel 

def tunnel_option_monte_carlo(type_option, S0, K, B1, B2, r, sigma, T, iteration):
    
    np.random.seed(45)
    dt= T/iteration
    W=np.random.normal(0,1,45)
    S= S0*np.exp(np.cumsum((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*W)) 
    in_barrier = np.logical_and(S > B1, S < B2)

    # Calculer les payoffs de l'option tunnel
    if type_option == "Call":
        payoff = np.where(in_barrier, np.maximum(S - K, 0), 0)
    elif type_option == "Put":
        payoff = np.where(in_barrier, np.maximum(K - S, 0), 0)
    else:
        print("error option")
    prix_option= np.exp(-r*T)*np.mean(payoff)

    return prix_option


#3) Option Himalaya
def himalaya_option_monte_carlo(type_option, S0, r, sigma, T, iteration):    
    np.random.seed(45)
    dt= T/iteration
    W=np.random.normal(0,1,45)
    S= S0*np.exp(np.cumsum((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*W)) 
    average_prices = np.mean(S, axis=1)

    # Calculer les payoffs de l'option Himalaya
    if type_option == 'Call':
        payoffs = np.maximum(average_prices - S, 0)
    elif type_option == 'Put':
        payoffs = np.maximum(S - average_prices, 0)
    else:
        print("Error option")

    # Calculer la valeur actuelle de l'option en prenant la moyenne des payoffs actualisés
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    return option_price   
    

#4) Option Napoléon

            
def napoleon_option_monte_carlo(S0, K, barrier, r, sigma, T, iteration):    
    np.random.seed(45)
    dt= T/iteration
    W=np.random.normal(0,1,45)
    option_prices = np.zeros(iteration)
    
    

   # Calculer le payoff de l'option Napoléon
    for i in range(iteration):
        W=np.random.normal(0,1,i+1)
        S= S0*np.exp(np.cumsum((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*W))
        activated = np.any(S > barrier)
        if activated:
           option_prices[i] = np.exp(-r * T) * np.maximum(S[-1] - K, 0)
        else:
           option_prices[i] = 0


   # Calculer la valeur actuelle de l'option en actualisant le payoff
    option_price = np.mean(option_prices)
    
    error = 2.576 * np.std(option_prices) / np.sqrt(iteration)
   
    return option_price, error, option_prices
#méthode calcul résolution EDP par différence finies 


def napoleon_option_differences_finies(S0, K, T, r, sigma, M, iteration):
    N=iteration
    dt = T / N
    ds = (2 * K) / M
    # Initialiser la matrice des prix de l'option
    option_prices = np.zeros((M + 1, N + 1))

    # Conditions aux limites pour l'option européenne
    option_prices[:, N] = np.maximum(np.linspace(0, 2 * K, M + 1) - K, 0)

    # Itération à rebours pour résoudre l'EDP
    for n in range(N - 1, -1, -1):
        for m in range(1, M):
            d1 = (np.log(np.linspace(0, 2 * K, M + 1)[m] / K) + (r + 0.5 * sigma**2) * (T - n * dt)) / (sigma * np.sqrt(T - n * dt))
            d2 = d1 - sigma * np.sqrt(T - n * dt)

            # Formule des différences finies pour l'option européenne
            option_prices[m, n] = np.exp(-r * dt) * (option_prices[m + 1, n + 1] * 0.5 * (np.exp(r * dt) + np.exp(-r * dt)) +
                                                    option_prices[m, n + 1] * 0.5 * (np.exp(-r * dt) + np.exp(r * dt)))

    return option_prices
""""
# Paramètres du modèle
S0 = 100  # Prix initial de l'actif sous-jacent
K = 100   # Prix d'exercice
T = 1     # Temps jusqu'à l'expiration (en années)
r = 0.05  # Taux d'intérêt sans risque
sigma = 0.2  # Volatilité

# Discrétisation
M = 100  # Nombre de points en espace
N = 100  # Nombre de points en temps

# Calcul du prix de l'option avec une résolution plus fine
M_fine = 200  # Plus de points en espace
N_fine = 200  # Plus de points en temps

prix_option_fine = napoleon_option_differences_finies(S0, K, T, r, sigma, M_fine, N_fine)

# Calcul du prix de l'option avec la résolution standard
prix_option_standard = napoleon_option_differences_finies(S0, K, T, r, sigma, M, N)

# Estimation de l'erreur
erreur = np.max(np.abs(prix_option_fine - prix_option_standard))

# Affichage du résultat
plt.imshow(prix_option_standard, cmap='viridis', extent=[0, T, 0, 2 * K], aspect='auto', origin='lower')
plt.colorbar(label='Prix de l\'option')
plt.title(f'Prix de l\'option Napoléon (Erreur estimee: {erreur:.5f})')
plt.xlabel('Temps (années)')
plt.ylabel('Prix de l\'actif sous-jacent')
plt.show()
"""


def option_napoleon_transformee_fourier(S0, K, T, r, sigma, iteration, alpha):
    # Paramètres
    N=iteration
    dt = T / N
    delta = 0.1
    lambda_ = 2 * np.pi / (N * delta)

    # Discrétisation des points en fréquence
    n = np.arange(1, N + 1)
    xi_n = np.fft.fftfreq(N, delta)

    # Transformée de Fourier rapide (FFT) de la fonction de payoff
    f_tilde = np.fft.fft(payoff_napoleon(S0, K, T, r, sigma, xi_n, alpha, N))

    # Calcul du prix de l'option
    call_price = np.exp(-alpha * np.log(K)) / np.pi * np.sum(np.real(np.exp(-1j * alpha * np.log(S0)) * f_tilde) * delta)

    return call_price

def payoff_napoleon(S0, K, T, r, sigma, xi, alpha, N):
    # Calcul de la fonction de payoff
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    payoff = np.exp(-r * T) * (np.exp(1j * alpha * np.log(S0)) * np.exp(-1j * alpha * np.log(K)) *
                               norm.cdf(d1 + sigma * np.sqrt(T) * 1j) -
                               norm.cdf(d2 + sigma * np.sqrt(T) * 1j))

    return payoff

# Paramètres du modèle
S0 = 100  # Prix initial de l'actif sous-jacent
K = 100   # Prix d'exercice
T = 1     # Temps jusqu'à l'expiration (en années)
r = 0.05  # Taux d'intérêt sans risque
sigma = 0.2  # Volatilité

# Paramètres pour la transformée de Fourier
N = 4096  # Nombre de points de discrétisation en fréquence
alpha = 1.5  # Paramètre de régularisation

# Calcul du prix de l'option
prix_option_napoleon = option_napoleon_transformee_fourier(S0, K, T, r, sigma, N, alpha)

# Affichage du résultat
print(f'Le prix de l\'option Napoléon est : {prix_option_napoleon:.2f}')




def dupire_local_volatility_napoleon(S0, K, T, r, market_prices, strikes, maturities):
    # Parameters
    M = len(strikes)
    N = len(maturities)

    # Discretization
    ds = strikes[1] - strikes[0]
    dt = maturities[1] - maturities[0]

    # Initialize the grid for option prices
    option_prices = np.zeros((M, N))

    # Market prices matrix
    market_matrix = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            market_matrix[i, j] = market_prices[i * N + j]

    # Time-stepping loop to solve the local volatility PDE for Napoleon option
    for j in range(1, N):
        for i in range(1, M - 1):
            # Central finite difference for the second spatial derivative
            d2C_ds2 = (option_prices[i + 1, j - 1] - 2 * option_prices[i, j - 1] + option_prices[i - 1, j - 1]) / ds**2

            # Dupire's PDE for local volatility (modified for Napoleon option)
            option_prices[i, j] = option_prices[i, j - 1] + r * S0 * (K - strikes[i]) / strikes[i] * option_prices[i, j - 1] * dt + \
                                  0.5 * S0**2 * strikes[i]**2 * (d2C_ds2 / option_prices[i, j - 1]) * dt + \
                                  (strikes[i] - K) * option_prices[i, j - 1] * dt

        # Apply boundary conditions (modify as needed for Napoleon option)
        option_prices[0, j] = 2 * option_prices[1, j] - option_prices[2, j]
        option_prices[M - 1, j] = 2 * option_prices[M - 2, j] - option_prices[M - 3, j]

    return option_prices

# Parameters
S0 = 100  # Initial stock price
K = 100  # Strike price
T = 1  # Time to maturity
r = 0.05  # Risk-free rate

# Market data (example)
strikes = np.linspace(80, 120, 11)
maturities = np.linspace(0.1, 1, 10)
market_prices = np.random.rand(len(strikes) * len(maturities)) * 10  # Random market prices for illustration

# Solve Dupire's local volatility PDE for Napoleon option
option_prices_napoleon = dupire_local_volatility_napoleon(S0, K, T, r, market_prices, strikes, maturities)

# Plot the results
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
M, N = np.meshgrid(strikes, maturities)
ax.plot_surface(M, N, option_prices_napoleon, cmap='viridis')
ax.set_xlabel('Strike')
ax.set_ylabel('Maturity')
ax.set_zlabel('Option Price')
ax.set_title('Dupire\'s Local Volatility Model for Napoleon Option')

plt.show()


def heston_fd_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, M, N):
    # Parameters
    ds = (2 * K) / M
    dt = T / N

    # Grid
    S_vals = np.linspace(0, 2 * K, M + 1)
    t_vals = np.linspace(0, T, N + 1)

    # Initialize option values at maturity
    option_values = np.maximum(S_vals - K, 0)

    # Finite difference scheme for Heston model
    for n in range(N - 1, -1, -1):
        for m in range(1, M):
            # Update stock price values
            dS = r * S_vals[m] * dt + np.sqrt(option_values[m] * S_vals[m] * dt) * np.random.normal()
            S_vals[m] = S_vals[m] + dS

            # Update option values using finite differences
            dV = kappa * (theta - option_values[m]) * dt + sigma * np.sqrt(option_values[m] * dt) * np.random.normal()
            option_values[m] = option_values[m] + dV

        # Apply boundary conditions at each time step
        option_values[0] = 2 * option_values[1] - option_values[2]
        option_values[M] = 2 * option_values[M - 1] - option_values[M - 2]

    # Calculate option price at initial stock price
    option_price = np.interp(S0, S_vals, option_values)

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
kappa = 1.0  # Mean-reversion rate
theta = 0.04  # Long-term volatility mean
sigma = 0.2  # Volatility of volatility
rho = -0.7  # Correlation between stock price and volatility
v0 = 0.04  # Initial volatility
M = 100  # Number of stock price grid points
N = 1000  # Number of time steps

# Calculate option price using Heston model and finite differences
option_price = heston_fd_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, M, N)

# Display the result
print(f"The estimated price of the Napoleon option using Heston model and finite differences is: {option_price:.4f}")



def heston_characteristic_function(u, T, kappa, theta, sigma, rho, v0, r, K, S0):
    # Heston parameters
    xi = kappa - rho * sigma
    d = np.sqrt((rho * sigma * u * 1j - xi)**2 - sigma**2 * (2 * 1j * u - u**2))
    g = (xi - rho * sigma * 1j - d) / (xi - rho * sigma * 1j + d)

    # Function to integrate
    def integrand(v):
        phi = np.exp(-r * T) * np.exp(1j * u * np.log(S0 / K)) * np.exp(-v * T) * heston_characteristic_function(v, T, kappa, theta, sigma, rho, v0, r, K, S0)
        return np.real(np.exp(-1j * u * np.log(K)) * phi / (1j * u))

    # Perform numerical integration
    integral_value, _ = quad(lambda v: integrand(v), 0, np.inf, limit=1000, epsabs=1e-8)

    # Return the characteristic function value
    return integral_value

def heston_option_price_fourier(S0, K, T, r, kappa, theta, sigma, rho, v0):
    # Parameters
    u_max = 50
    du = 0.1

    # Generate u values
    u_values = np.arange(0, u_max, du)

    # Calculate option price using Fourier transform
    option_price = (1/2 + 1/np.pi * np.trapz(np.real(np.exp(-1j * u_values * np.log(K)) * heston_characteristic_function(u_values, T, kappa, theta, sigma, rho, v0, r, K, S0)), dx=du))

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
kappa = 1.0  # Mean-reversion rate
theta = 0.04  # Long-term volatility mean
sigma = 0.2  # Volatility of volatility
rho = -0.7  # Correlation between stock price and volatility
v0 = 0.04  # Initial volatility

# Calculate option price using Heston model and Fourier transform
option_price = heston_option_price_fourier(S0, K, T, r, kappa, theta, sigma, rho, v0)

# Display the result
print(f"The estimated price of the Napoleon option using Heston model and Fourier transform is: {option_price:.4f}")


def heston_mc_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, n_paths, n_steps):
    dt = T / n_steps
    sqrt_dt = np.sqrt(dt)

    # Generate correlated Brownian motions
    dW1 = np.random.normal(size=(n_paths, n_steps)) * sqrt_dt
    dW2 = rho * dW1 + np.sqrt(1 - rho**2) * np.random.normal(size=(n_paths, n_steps)) * sqrt_dt

    # Initialize arrays for stock prices and volatility
    S = np.zeros((n_paths, n_steps + 1))
    v = np.zeros((n_paths, n_steps + 1))

    # Set initial conditions
    S[:, 0] = S0
    v[:, 0] = v0

    # Euler-Maruyama scheme for Heston model
    for i in range(1, n_steps + 1):
        S[:, i] = S[:, i - 1] * np.exp((r - 0.5 * v[:, i - 1]) * dt + np.sqrt(v[:, i - 1]) * dW1[:, i - 1])
        v[:, i] = v[:, i - 1] + kappa * (theta - v[:, i - 1]) * dt + sigma * np.sqrt(v[:, i - 1]) * dW2[:, i - 1]

    # Calculate option payoff at maturity
    payoff = np.maximum(S[:, -1] - K, 0)

    # Calculate option price as the discounted average payoff
    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
kappa = 1.0  # Mean-reversion rate
theta = 0.04  # Long-term volatility mean
sigma = 0.2  # Volatility of volatility
rho = -0.7  # Correlation between stock price and volatility
v0 = 0.04  # Initial volatility
n_paths = 10000  # Number of Monte Carlo paths
n_steps = 252  # Number of time steps

# Calculate option price using Heston model
option_price = heston_mc_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, n_paths, n_steps)

# Display the result
print(f"The estimated price of the Napoleon option is: {option_price:.4f}")



def sabr_fd_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, M, N):
    # Parameters
    ds = (2 * K) / M
    dt = T / N

    # Grid
    S_vals = np.linspace(0, 2 * K, M + 1)
    t_vals = np.linspace(0, T, N + 1)

    # Initialize option values at maturity
    option_values = np.maximum(S_vals - K, 0)

    # Finite difference scheme for SABR model
    for n in range(N - 1, -1, -1):
        for m in range(1, M):
            # Update stock price values
            dS = r * S_vals[m] * dt + np.sqrt(option_values[m] * S_vals[m] * dt) * np.random.normal()
            S_vals[m] = S_vals[m] + dS

            # Update option values using finite differences
            dV = alpha * option_values[m]**((1 - beta) / 2) * np.sqrt(dt) * np.random.normal()
            option_values[m] = option_values[m] + dV

        # Apply boundary conditions at each time step
        option_values[0] = 2 * option_values[1] - option_values[2]
        option_values[M] = 2 * option_values[M - 1] - option_values[M - 2]

    # Calculate option price at initial stock price
    option_price = np.interp(S0, S_vals, option_values)

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
alpha = 0.2  # Initial volatility level (alpha in SABR)
beta = 0.5  # Beta parameter in SABR
rho = -0.7  # Rho parameter in SABR
vol_of_vol = 0.2  # Volatility of volatility parameter in SABR
M = 100  # Number of stock price grid points
N = 1000  # Number of time steps

# Calculate option price using SABR model and finite differences
option_price = sabr_fd_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, M, N)

# Display the result
print(f"The estimated price of the Napoleon option using SABR model and finite differences is: {option_price:.4f}")



def sabr_characteristic_function(u, T, alpha, beta, rho, vol_of_vol, r, K, S0):
    # SABR parameters
    z = vol_of_vol / alpha
    x = np.log(S0 / K)
    a = alpha * (S0**(1 - beta))
    b = (1 - beta) * np.log(S0 / K) + 0.5 * (rho * vol_of_vol * alpha * T)
    rho_bar = np.sqrt(1 - 2 * rho * rho + rho * rho)

    # Function to integrate
    def integrand(v):
        gamma = np.sqrt(alpha**2 - 2 * rho * vol_of_vol * alpha * v + vol_of_vol**2 * v**2)
        d1 = (np.log(S0 / (K * (np.exp(-x) + v * rho_bar))) + b) / gamma
        d2 = (np.log(S0 / (K * (np.exp(-x) + v * rho_bar))) + b - gamma * T) / gamma
        return np.exp(-1j * u * np.log(K)) * np.exp(1j * u * x) * np.exp(-v * T) * (np.exp(-r * T) * S0**beta * (1 - beta) / gamma) * (np.cosh(d1) + rho_bar * ((S0 / K)**(-rho) * np.sinh(d1) + np.cosh(d2)))

    # Perform numerical integration
    integral_value, _ = quad(lambda v: integrand(v), 0, np.inf, limit=1000, epsabs=1e-8)

    # Return the characteristic function value
    return np.exp(-r * T) * integral_value

def sabr_option_price_fourier(S0, K, T, r, alpha, beta, rho, vol_of_vol):
    # Parameters
    u_max = 50
    du = 0.1

    # Generate u values
    u_values = np.arange(0, u_max, du)

    # Calculate option price using Fourier transform
    option_price = (np.exp(-r * T) / np.pi) * np.trapz(np.real(np.exp(-1j * u_values * np.log(K)) * sabr_characteristic_function(u_values, T, alpha, beta, rho, vol_of_vol, r, K, S0)), dx=du)

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
alpha = 0.2  # Initial volatility level (alpha in SABR)
beta = 0.5  # Beta parameter in SABR
rho = -0.7  # Rho parameter in SABR
vol_of_vol = 0.2  # Volatility of volatility parameter in SABR

# Calculate option price using SABR model and Fourier transform
option_price = sabr_option_price_fourier(S0, K, T, r, alpha, beta, rho, vol_of_vol)

# Display the result
print(f"The estimated price of the Napoleon option using SABR model and Fourier transform is: {option_price:.4f}")



def sabr_mc_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, n_paths, n_steps):
    dt = T / n_steps
    sqrt_dt = np.sqrt(dt)

    # Generate correlated Brownian motions
    dW_S = np.random.normal(size=(n_paths, n_steps)) * sqrt_dt
    dW_vol = rho * dW_S + np.sqrt(1 - rho**2) * np.random.normal(size=(n_paths, n_steps)) * sqrt_dt

    # Initialize arrays for stock prices and volatilities
    S = np.zeros((n_paths, n_steps + 1))
    vol = np.zeros((n_paths, n_steps + 1))

    # Set initial conditions
    S[:, 0] = S0
    vol[:, 0] = alpha

    # Euler-Maruyama scheme for SABR model
    for i in range(1, n_steps + 1):
        Z_S = np.random.normal(size=n_paths)
        Z_vol = np.random.normal(size=n_paths)

        S[:, i] = S[:, i - 1] * np.exp((r - 0.5 * vol[:, i - 1]**2) * dt + vol[:, i - 1] * Z_S)
        vol[:, i] = vol[:, i - 1] * np.exp(-beta * np.log(vol[:, i - 1]) * dt + vol_of_vol * Z_vol)

    # Calculate option payoff at maturity
    payoff = np.maximum(S[:, -1] - K, 0)

    # Calculate option price as the discounted average payoff
    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
alpha = 0.2  # Initial volatility level (alpha in SABR)
beta = 0.5  # Beta parameter in SABR
rho = -0.7  # Rho parameter in SABR
vol_of_vol = 0.2  # Volatility of volatility parameter in SABR
n_paths = 10000  # Number of Monte Carlo paths
n_steps = 252  # Number of time steps

# Calculate option price using SABR model
option_price = sabr_mc_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, n_paths, n_steps)

# Display the result
print(f"The estimated price of the Napoleon option using SABR model is: {option_price:.4f}")


import numpy as np



def dupire_characteristic_function(u, T, S0, local_volatility):
    # Local volatility function
    sigma_t = local_volatility(T)

    # Function to integrate
    def integrand(x):
        d = np.log(S0) - x
        return np.exp(1j * u * d) * np.exp(-0.5 * (u**2) * sigma_t**2 * T) / (1j * u)

    # Perform numerical integration
    integral_value, _ = quad(lambda x: integrand(x), -np.inf, np.inf, limit=1000, epsabs=1e-8)

    # Return the characteristic function value
    return integral_value

def dupire_option_price_fourier(S0, K, T, local_volatility):
    # Parameters
    u_max = 50
    du = 0.1

    # Generate u values
    u_values = np.arange(0, u_max, du)

    # Calculate option price using Fourier transform
    option_price = (1/2 + 1/np.pi * np.trapz(np.real(np.exp(-1j * u_values * np.log(K)) * dupire_characteristic_function(u_values, T, S0, local_volatility)), dx=du))

    return option_price

# Example of a local volatility function
def local_volatility(T):
    # Example: constant local volatility
    return 0.2

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity

# Calculate option price using Dupire model and Fourier transform
option_price = dupire_option_price_fourier(S0, K, T, local_volatility)

# Display the result
print(f"The estimated price of the Napoleon option using Dupire model and Fourier transform is: {option_price:.4f}")


def dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, n_paths, n_steps):
    dt = T / n_steps
    sqrt_dt = np.sqrt(dt)

    # Generate correlated Brownian motions
    dW = np.random.normal(size=(n_paths, n_steps)) * sqrt_dt

    # Initialize arrays for stock prices
    S = np.zeros((n_paths, n_steps + 1))
    S[:, 0] = S0

    # Euler-Maruyama scheme for Dupire's local volatility model
    for i in range(1, n_steps + 1):
        dS = r * S[:, i - 1] * dt + local_volatility(S[:, i - 1], K, T - i * dt) * S[:, i - 1] * dW[:, i - 1]
        S[:, i] = S[:, i - 1] + dS

    return S[:, -1]

def calculate_napoleon_option_price(S_T, K):
    return np.maximum(S_T - K, 0)

def monte_carlo_dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, n_paths, n_steps):
    option_prices = np.zeros(n_paths)

    for i in range(n_paths):
        # Simulate stock price path
        S_T = dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, 1, n_steps)[0, -1]

        # Calculate option payoff
        option_prices[i] = calculate_napoleon_option_price(S_T, K)

    # Calculate option price as the discounted average payoff
    option_price = np.exp(-r * T) * np.mean(option_prices)

    return option_price

# Example of a local volatility function
def local_volatility(S, K, T):
    # Example: constant local volatility
    return 0.2

# Parameters
S0 = 100  # Initial stock price
K = 100   # Strike price
T = 1     # Time to maturity
r = 0.05  # Risk-free rate
n_paths = 10000  # Number of Monte Carlo paths
n_steps = 252  # Number of time steps

# Calculate option price using Dupire's local volatility model and Monte Carlo
option_price = monte_carlo_dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, n_paths, n_steps)

# Display the result
print(f"The estimated price of the Napoleon option using Dupire's local volatility model is: {option_price:.4f}")



def napoleon_option(S0, K, barrier, r, sigma, T, iteration,modele,methode):
        if methode=="Monte-Carlo":
            if modele=="Black & Scholes":
                napoleon_option_monte_carlo(S0, K, barrier, r, sigma, T, iteration)
            elif modele=="SABR":
                sabr_mc_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, n_paths, n_steps)
            elif modele=="Heston volatility":
                heston_mc_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, n_paths, n_steps)
            elif modele=="Dupire local volatility":
                dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, n_paths, n_steps)
                
        elif methode=="résolution EDP par différences finies":
              if modele=="Black & Scholes":
                  napoleon_option_differences_finies(S0, K, T, r, sigma, iteration, iteration)
              elif modele=="Dupire local volatility":
                  dupire_local_volatility_napoleon(S0, K, T, r, local_volatility, n_paths, n_steps)
              elif modele==" Heston volatility":
                  heston_fd_napoleon(S0, K, T, r, kappa, theta, sigma, rho, v0, M, N)
              elif modele=="SABR":
                  sabr_fd_napoleon(S0, K, T, r, alpha, beta, rho, vol_of_vol, M, N)
                  
        elif methode=="Transformée de Fourier":
              if modele=="Black & Scholes":
                  option_napoleon_transformee_fourier(S0, K, T, r, sigma, iteration, 0.5)
              elif modele=="SABR":
                sabr_option_price_fourier(S0, K, T, r, alpha, beta, rho, vol_of_vol)
              elif modele=="Heston volatility":
                  heston_option_price_fourier(S0, K, T, r, kappa, theta, sigma, rho, v0)
              elif modele=="Dupire local volatility":
                  dupire_option_price_fourier(S0, K, T, local_volatility)
                  
                
                
                
# Paramètres de l'option Napoléon
S0 = 100   # Prix initial de l'action
K = 105    # Prix d'exercice de l'option
barrier = 120  # Seuil d'activation de l'option
r = 0.05   # Taux d'intérêt sans risque
sigma = 0.2   # Volatilité
T = 1      # Maturité de l'option en années
iteration = 1000  # Nombre d'itérations pour la simulation
# Calcul du prix de l'option Napoléon avec estimation de l'erreur
napoleon_price, error, option_price = napoleon_option_monte_carlo(S0, K, barrier, r, sigma, T, iteration)

plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, iteration+1), option_price, label='Estimations de l\'option')

plt.axhline(y=napoleon_price, color='r', linestyle='--', label='Prix estimé de l\'option')
plt.xlabel('Nombre d\'itérations')
plt.ylabel('Estimations de l\'option')
plt.title('Convergence de l\'algorithme Monte Carlo pour l\'option Napoléon')
plt.legend()
plt.grid(True)
plt.show()  
   


# Fonction pour le bouton de calcul
def calculer_option(type_option_var, K_var, r_var, T_var, sigma_var, S0_var, iteration_var, resultat_label,modele_var,methode_var):
    # Obtenir les valeurs des variables
    type_option = type_option_var.get()
    K = float(K_var.get())
    r = float(r_var.get())
    T = float(T_var.get())
    sigma = float(sigma_var.get())
    S0 = float(S0_var.get())
    iteration = int(iteration_var.get())
    methode=str(methode_var.get())
    modele=str(modele_var.get())

    # Appeler la fonction de calcul appropriée en fonction du type d'option
    if type_option == "Vanille":
        resultat = option_vanille(type_option, K, r, T, sigma, S0, iteration)
    elif type_option == "Tunnel":
        # Ajoutez les champs B1 et B2 pour l'option Tunnel
        B1 = float(B1_var.get())
        B2 = float(B2_var.get())
        resultat = tunnel_option_monte_carlo(type_option, S0, K, B1, B2, r, sigma, T, iteration)
    elif type_option == "Himalaya":
        resultat = himalaya_option_monte_carlo(type_option, S0, r, sigma, T, iteration)
    elif type_option == "Napoléon":
        # Ajoutez le champ barrier pour l'option Napoléon
            barrier = float(barrier_var.get())
            resultat = napoleon_option(S0, K, barrier, r, sigma, T, iteration,modele,methode)
        
       
    else:
        resultat = "Type d'option non pris en charge."

    # Afficher le résultat dans l'étiquette
    resultat_label.config(text=resultat)




def black_scholes_greeks(option_type, S, K, T, r, sigma):
    """
    Calculate the greeks (Delta, Gamma, Theta, Vega, Rho) for a European option using Black-Scholes formula.

    Parameters:
    - option_type: 'call' for a call option, 'put' for a put option
    - S: Current stock price
    - K: Option strike price
    - T: Time to expiration (in years)
    - r: Risk-free interest rate
    - sigma: Volatility of the underlying stock

    Returns:
    - Delta: Sensitivity of the option price to changes in stock price
    - Gamma: Rate of change of Delta
    - Theta: Sensitivity of the option price to time decay
    - Vega: Sensitivity of the option price to changes in volatility
    - Rho: Sensitivity of the option price to changes in interest rate
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        Delta = norm.cdf(d1)
    elif option_type == 'put':
        Delta = -norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    Gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    Theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    Vega = S * np.sqrt(T) * norm.pdf(d1)
    Rho = K * T * np.exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return Delta, Gamma, Theta, Vega, Rho


    


def black_scholes_greeks(option_type, S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        Delta = norm.cdf(d1)
    elif option_type == 'put':
        Delta = -norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    Gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    Theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    Vega = S * np.sqrt(T) * norm.pdf(d1)
    Rho = K * T * np.exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return Delta, Gamma, Theta, Vega, Rho

def calculate_greeks(type_option):
    type_option = type_option_var.get()
    S = float(entry_S.get())
    K = float(entry_K.get())
    T = float(entry_T.get())
    r = float(entry_r.get())
    sigma = float(entry_sigma.get())

    greeks = black_scholes_greeks(type_option, S, K, T, r, sigma)

    result_label.config(text=f"Delta: {greeks[0]:.4f}\nGamma: {greeks[1]:.4f}\nTheta: {greeks[2]:.4f}\nVega: {greeks[3]:.4f}\nRho: {greeks[4]:.4f}")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Calcul options et Grecques")

# Création des widgets dans la fenêtre principale
# Libellés et champs de saisie pour les paramètres
Label(fenetre, text="Type d'option:").grid(row=0, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=type_option_var).grid(row=0, column=3, padx=5, pady=5)


Label(fenetre, text="K:").grid(row=1, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=K_var).grid(row=1, column=4, padx=5, pady=5)

Label(fenetre, text="r:").grid(row=2, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=r_var).grid(row=2, column=4, padx=5, pady=5)

Label(fenetre, text="T:").grid(row=3, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=T_var).grid(row=3, column=4, padx=5, pady=5)

Label(fenetre, text="sigma:").grid(row=4, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=sigma_var).grid(row=4, column=4, padx=5, pady=5)

Label(fenetre, text="S0:").grid(row=5, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=S0_var).grid(row=5, column=4, padx=5, pady=5)

Label(fenetre, text="Iterations:").grid(row=6, column=3, padx=5, pady=5)
Entry(fenetre, textvariable=iteration_var).grid(row=6, column=4, padx=5, pady=5)

# Création du bouton "Calcul Grecques" dans la fenêtre principale


calculate_button = ttk.Button(fenetre, text="Calcul Grecques", command=calculate_greeks)
calculer_button.grid(row=12, column=3, columnspan=2, pady=10)

result_label = ttk.Label(fenetre, text="Résultats des Grecques"

# Placement des widgets dans la grille pour la fenêtre principale







# Variables pour stocker les valeurs des champs de saisie
type_option_var = tk.StringVar()
K_var = tk.StringVar()
r_var = tk.StringVar()
T_var = tk.StringVar()
sigma_var = tk.StringVar()
S0_var = tk.StringVar()
iteration_var = tk.StringVar()
B1_var = tk.StringVar()
B2_var = tk.StringVar()
barrier_var = tk.StringVar()
modele_var=tk.StringVar()
methode_var=tk.StringVar()

# Libellés et champs de saisie pour les paramètres
Label(fenetre, text="Type d'option:").grid(row=0, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=type_option_var).grid(row=0, column=1, padx=5, pady=5)


Label(fenetre, text="K:").grid(row=1, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=K_var).grid(row=1, column=1, padx=5, pady=5)

Label(fenetre, text="r:").grid(row=2, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=r_var).grid(row=2, column=1, padx=5, pady=5)

Label(fenetre, text="T:").grid(row=3, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=T_var).grid(row=3, column=1, padx=5, pady=5)

Label(fenetre, text="sigma:").grid(row=4, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=sigma_var).grid(row=4, column=1, padx=5, pady=5)

Label(fenetre, text="S0:").grid(row=5, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=S0_var).grid(row=5, column=1, padx=5, pady=5)

Label(fenetre, text="Iterations:").grid(row=6, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=iteration_var).grid(row=6, column=1, padx=5, pady=5)

# Ajoutez des champs pour B1, B2 et barrier si nécessaire
Label(fenetre, text="B1:").grid(row=7, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=B1_var).grid(row=7, column=1, padx=5, pady=5)

Label(fenetre, text="B2:").grid(row=8, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=B2_var).grid(row=8, column=1, padx=5, pady=5)

Label(fenetre, text="Barrier:").grid(row=9, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=barrier_var).grid(row=9, column=1, padx=5, pady=5)

# Ajouter des champs de saisie pour Méthode et Modèle
Label(fenetre, text="Méthode:").grid(row=10, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=methode_var).grid(row=10, column=1, padx=5, pady=5)

Label(fenetre, text="Modèle:").grid(row=11, column=0, padx=5, pady=5)
Entry(fenetre, textvariable=modele_var).grid(row=11, column=1, padx=5, pady=5)



# Étiquette pour afficher le résultat
resultat_label = Label(fenetre, text="")
resultat_label.grid(row=11, column=0, columnspan=2, pady=10)

#créer de nouvelles fonctions différentes selon le choix de modèle et de méthode
#créer une fonction pour le calcul des grecques 

    
        

# Bouton de calcul
calculer_button = Button(fenetre, text="Calculer", command=partial(calculer_option, type_option_var, K_var, r_var, T_var, sigma_var, S0_var, iteration_var, resultat_label))
calculer_button.grid(row=12, column=0, columnspan=2, pady=10)



# Lancement de la boucle principale de la fenêtre
fenetre.mainloop()









