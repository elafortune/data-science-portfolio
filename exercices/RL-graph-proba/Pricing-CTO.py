import numpy as np

def generate_X():
    return np.random.normal()

def generate_epsilon_i(n):
    return np.random.normal(size=n)

def compute_Zi(rho):
    return np.sqrt(rho)*generate+ np.sqrt(1-rho)*generate_epsilon_i(n)

def is_default(Z,B):
    return (Z<B)*np.ones(Z.size())
def compute_loss(D,EAD,LGD):
    D*EAD*LGD

def compute_loss_ptf(LOSS):
    return np.sum(LOSS)

def Monte_Carlo_ptf(rho,PD,EAD,LGD,ns):
    n=PD.size()
    B=np.random.normal()
    for i in range(ns):
        Z= compute_Zi(rho,n)
        D= is_default(Z,B)
        Loss_i= compute_loss(D,EAD,LGD)
        Loss_ptf= compute_loss_ptf(Loss_i)
