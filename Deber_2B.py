# -*- coding: utf-8 -*-
"""
@author: Marcelo Curay
EJERCICIO DE ELEMENTOS DE MÁQUINAS - "SHIGLEY"
DIMENSIONAMIENTO DE UN PERNO QUE TRABAJE A FATIGA Y VIDA INFINITA
"""
import numpy as np
#%%
d_perno = 10E-3#m Asumir "Diametro del perno"
ld = 20E-3#m asumir #Longuitud entre placas"
lt = 20E-3#m asumir #Longuitud de roscado"
Ad = np.pi*(d_perno**2)/4 #Area de la parte sin roscar
At = 58E-6 #m^2 "Area de esfuerzo a tension -Taba 8.1"
E = 205E9 #Pa  "Modulo de Young del acero"
# dw = 20E-3 #m tabla A-33
dw = 1.5*d_perno #Espesor del perno
t = 10E-3 #m #Espesor
Sp = 650E6 #Esfuerzo de prueba minima [Pa] Tabla 8-11
#%%
def factor_kb(At,Ad,lt,ld,E): # Rigidez efectiva del perno de cabeza en la zona de sujetacion 
    kb = (At*Ad*E)/(Ad*lt + At*ld)
    return kb
def factor_km(E,t, dw,d_perno): #Rigidez del elemento
    l = 2*t
    alpha = np.radians(30)
    A = (l*np.tan(alpha) + dw - d_perno)*(dw + d_perno)
    B = (l*np.tan(alpha) + dw + d_perno)*(dw - d_perno)
    km = (np.pi*E*d_perno*np.tan(alpha))/(2*np.log(A/B))
    return km
def factor_C(kb, km): #Fraccion de carga del perno
    C = kb/(kb+km)
    return C
def nf(Se, Sut, sigma_i, sigma_a, sigma_m): #Factor de seguridad
    nf = (Se*(Sut-sigma_i))/(sigma_a*Sut + Se*(sigma_m - sigma_i))
    return nf
#%% Transformacion de unidades al SI
D_tubo = 100/1000 #m #Diametro del tubo
M = 2000 #N #Momento
Pmax = 1.25E6 #Pa Presion maxima
Pmin = 0.8E6 #Pa  Presion minima
D_empaque = 120/1000 #m Diametro de empaque
r_posicion= 0.075 #m distancia del eje del tubo a los pernos

#%%
A_empaque =np.pi * (D_empaque**2)/4 #   Area de Empaque
Fmin_empaque = A_empaque*Pmin       #Fuerza minima de Empaque
Fmax_empaque = A_empaque*Pmax        #Fuerza maxima de Empaque
#Alturas de cada par de pernos
h1= r_posicion
# h2 = r_posicion*np.sin(np.radians(60))
# h3 = r_posicion*np.sin(np.radians(30))
#
FM1 = M/(2*h1)
# FM2 = (h2/h1)*FM1
# FM3 = (h3/h1)*FM1
#Factor de carga
kb = factor_kb(At,Ad,lt,ld,E)
km = factor_km(E,t, dw,d_perno)
C = factor_C(kb, km)

#Carga de tensión en cada perno
P1 = FM1 + Fmax_empaque/12
# P2 = (FM2/2 + Fmax_empaque/12) #Porque hay 2 pernos
# P3 = (FM3/2 + Fmax_empaque/12) #Porque hay 2 pernos
#Carga tomada por cada perno
#Pb1 = P1*C
# Pb2 = P2*C
# Pb3 = P3*C

# Precarga
Fp = At*Sp #N
Fi = 0.9*Fp #N Para uniones permanentes

#Esfuerzos  para el perno crítico
Pb_max = FM1 + (Fmax_empaque/12)*C
Pb_min = FM1 + (Fmin_empaque/12)*C
sigmab_max = Pb_max/At
sigmab_min = Pb_min/At

#Esfuerzo de instalación
sigma_i = Fi/At

#Recalculo de esfuerzos Criticos 
sigmab_maxx = sigmab_max+sigma_i
sigmab_minn = sigmab_min+sigma_i

#Esfuerzo alternante
sigma_a = (sigmab_max-sigmab_min)/2
sigma_m = (sigmab_max + sigmab_min + 2*sigma_i)/2

#Factor de seguridad
Sut = 900E6 #Pa  Tabla 8-11
Se = 140E6 #Pa Tabla 8-17
nf = nf(Se, Sut, sigma_i, sigma_a, sigma_m)



