import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_resultados(t, T_num, T_ana, Ta, T0):
    """
    Genera el set de 4 gráficas de análisis térmico.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    
    # --- Temperatura vs tiempo ---
    ax1 = axes[0, 0]
    ax1.plot(t, T_ana, 'b-',  linewidth=2.5, label='Solución analítica')
    ax1.plot(t, T_num,  'r--', linewidth=2.5,  label='Solución numérica (RK45)', alpha=0.6)
    ax1.axhline(Ta, color='gray', linestyle=':', label=f'Ta={Ta}°C')
    ax1.set_title('Temperatura vs Tiempo')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- Error ---
    ax2 = axes[0, 1]
    error = np.abs(T_ana - T_num)
    ax2.semilogy(t, error + 1e-12, 'g-')
    ax2.set_title('Error Absoluto (Escala Log)')
    ax2.grid(True, alpha=0.3)

    # --- Diferencia Térmica ---
    ax3 = axes[1, 0]
    ax3.fill_between(t, T_num - Ta, alpha=0.4, color='orange')
    ax3.set_title('Diferencia T - Ta')
    ax3.grid(True, alpha=0.3)

    # --- Velocidad de Enfriamiento ---
    ax4 = axes[1, 1]
    velocidad = -0.05 * (T_num - Ta) # Ejemplo simplificado para visualización
    ax4.plot(t, velocidad, 'm-')
    ax4.set_title('Velocidad dT/dt')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def generar_diagrama_esquematico(T0, Ta, k):
    """
    Crea el diagrama visual de la taza/cuerpo térmico.
    """
    fig2, ax_esq = plt.subplots(figsize=(6, 6))
    ax_esq.set_xlim(0, 10); ax_esq.set_ylim(0, 10); ax_esq.axis('off')
    
    # Taza (Simplificada para el Dashboard)
    cup = patches.FancyBboxPatch((3.5, 3), 3, 4, boxstyle="round,pad=0.2", color='#ff7f50', alpha=0.8)
    ax_esq.add_patch(cup)
    
    ax_esq.text(5, 5, f'Cuerpo\n{T0}°C', ha='center', color='white', fontweight='bold', fontsize=12)
    ax_esq.text(8.5, 8.5, f'Ambiente\n{Ta}°C', color='blue', fontweight='bold')
    
    # Ecuación
    ax_esq.text(5, 1, r'$\frac{dT}{dt} = -k(T - T_a)$', fontsize=15, ha='center', bbox=dict(facecolor='white', alpha=0.5))
    
    return fig2
