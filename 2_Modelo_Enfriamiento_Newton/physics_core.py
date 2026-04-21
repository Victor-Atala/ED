import numpy as np
from scipy.integrate import odeint

def modelo_enfriamiento(T, t, k, Ta):
    """
    Ecuación diferencial de Enfriamiento de Newton.
    dT/dt = -k * (T - Ta)
    """
    dTdt = -k * (T[0] - Ta)
    return [dTdt]

def solucion_analitica(t, T0, Ta, k):
    """
    Solución analítica exacta de la EDO.
    T(t) = Ta + (T0 - Ta) * exp(-k * t)
    """
    return Ta + (T0 - Ta) * np.exp(-k * t)

def resolver_simulacion(T0, Ta, k, t_total, num_puntos=1000):
    """
    Resuelve el modelo tanto de forma numérica como analítica.
    """
    t = np.linspace(0, t_total, num_puntos)
    
    # Numérica
    T_numerica = odeint(modelo_enfriamiento, [T0], t, args=(k, Ta))
    T_numerica = T_numerica[:, 0]
    
    # Analítica
    T_analitica = solucion_analitica(t, T0, Ta, k)
    
    return t, T_numerica, T_analitica
