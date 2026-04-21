import numpy as np
from params_estres import A_tanque, a_orificio, h0, g, calcular_k

print("--- INICIANDO PRUEBA DE ESTRÉS MODULAR ---")

try:
    # Intento de cálculo de constante k
    print("Calculando constante k...")
    k = calcular_k()
except ZeroDivisionError as e:
    print(f"\n[FALLO DETECTADO] Error de División: {e}")
    print("Explicación: El área del tanque A_tanque es 0.0, lo que hace que la fracción a/A sea infinita.")

try:
    # Intento de cálculo de tiempo (Raíz negativa)
    print("\nCalculando tiempo analítico...")
    # Forzamos ejecución manual para ver el error de dominio
    t_vacio = 2 * np.sqrt(h0) / 0.026 # Usando k genérico si falló el anterior
except Exception as e:
    print(f"[FALLO DETECTADO] Error de Dominio: {e}")
    print(f"Explicación: No se puede calcular la raíz cuadrada de h0={h0}.")

print("\n--- FIN DE LA DEMOSTRACIÓN DE FALLOS ---")
