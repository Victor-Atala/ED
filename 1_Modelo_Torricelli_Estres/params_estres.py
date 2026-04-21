import numpy as np

# ============================================================
# PARÁMETROS SABOTEADOS (INDUCEN FALLOS)
# ============================================================

# 1. División por cero
A_tanque = 0.0       

# 2. Incongruencia física
a_orificio = 2.0     
g = 9.81             

# 3. Violación del dominio (Raíz negativa)
h0 = -5.0             

# Constantes derivadas (Falla aquí por división entre cero)
def calcular_k():
    return (a_orificio / A_tanque) * np.sqrt(2 * g)
