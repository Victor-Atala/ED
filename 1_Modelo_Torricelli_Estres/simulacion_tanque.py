"""
Simulación del Vaciado de un Tanque mediante la Ley de Torricelli
Ecuaciones Diferenciales Ordinarias - Universidad Politécnica de Chiapas
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin pantalla
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from scipy.integrate import odeint

# ============================================================
# PARÁMETROS DEL SISTEMA
# ============================================================
# Geometría del tanque
A_tanque = 0.50      # Área transversal del tanque [m²] (base 0.5 m x 1.0 m = 0.5 m²)
a_orificio = 0.003   # Área del orificio de salida [m²]
g = 9.81             # Aceleración gravitacional [m/s²]

# Constante de Torricelli:  k = (a/A) * sqrt(2g)
k = (a_orificio / A_tanque) * np.sqrt(2 * g)

# Condiciones iniciales
h0 = 2.0             # Altura inicial del fluido [m]

# ============================================================
# MODELO MATEMÁTICO: EDO de Torricelli
# ============================================================
# dh/dt = -(a/A)*sqrt(2g)*sqrt(h)  =  -k * sqrt(h)

def modelo_torricelli(h, t):
    """
    Ecuación diferencial de Torricelli.
    dh/dt = -k * sqrt(h)
    Se garantiza h >= 0 para evitar raíz de número negativo.
    """
    h_val = max(h[0], 0.0)
    dhdt = -k * np.sqrt(h_val)
    return [dhdt]

# ============================================================
# SOLUCIÓN ANALÍTICA
# ============================================================
# Separando variables e integrando:
#   dh / sqrt(h)  =  -k dt
#   2*sqrt(h)     =  -k*t + C
# Con h(0) = h0  =>  C = 2*sqrt(h0)
# Por lo tanto:
#   h(t) = (sqrt(h0) - k*t/2)^2
# El tanque queda vacío cuando h(t) = 0:
#   t_vacio = 2*sqrt(h0) / k

t_vacio_analitico = 2 * np.sqrt(h0) / k
print(f"Tiempo analítico de vaciado: {t_vacio_analitico:.2f} s")

def solucion_analitica(t, h0, k):
    """
    Solución analítica: h(t) = max(sqrt(h0) - k*t/2, 0)^2
    """
    val = np.sqrt(h0) - (k * t) / 2
    return np.maximum(val, 0) ** 2

# ============================================================
# SOLUCIÓN NUMÉRICA (scipy odeint - método RK)
# ============================================================
t_total = t_vacio_analitico * 1.2   # Un 20% extra para ver tanque vacío
t = np.linspace(0, t_total, 1000)

h_numerica = odeint(modelo_torricelli, [h0], t)
h_numerica = h_numerica[:, 0]
h_numerica = np.maximum(h_numerica, 0)   # Clamp >= 0

h_analitica = solucion_analitica(t, h0, k)

# Velocidad de salida  v(t) = sqrt(2g*h)
v_salida = np.sqrt(2 * g * np.maximum(h_numerica, 0))

# Caudal de salida  Q(t) = a * v(t)
Q_salida = a_orificio * v_salida

# ============================================================
# FIGURA 1: Comparación analítica vs numérica
# ============================================================
fig1, axes = plt.subplots(2, 2, figsize=(12, 9))
fig1.suptitle('Vaciado de Tanque – Ley de Torricelli', fontsize=15, fontweight='bold')

# --- Altura vs tiempo ---
ax1 = axes[0, 0]
ax1.plot(t, h_analitica, 'b-',  linewidth=2.5, label='Solución analítica')
ax1.plot(t, h_numerica,  'r--', linewidth=1.5, label='Solución numérica (RK45)')
ax1.axvline(t_vacio_analitico, color='gray', linestyle=':', linewidth=1.2,
            label=f'$t_{{vacío}}={t_vacio_analitico:.1f}$ s')
ax1.set_xlabel('Tiempo [s]', fontsize=11)
ax1.set_ylabel('Altura del fluido h(t) [m]', fontsize=11)
ax1.set_title('Altura vs Tiempo', fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.35)
ax1.set_xlim([0, t_total])
ax1.set_ylim([-0.05, h0 * 1.05])

# --- Error relativo ---
ax2 = axes[0, 1]
error = np.abs(h_analitica - h_numerica)
ax2.semilogy(t, error + 1e-12, 'g-', linewidth=1.8)
ax2.set_xlabel('Tiempo [s]', fontsize=11)
ax2.set_ylabel('Error absoluto [m]', fontsize=11)
ax2.set_title('Error Analítico vs Numérico', fontsize=12)
ax2.grid(True, which='both', alpha=0.35)
ax2.set_xlim([0, t_total])

# --- Velocidad de salida ---
ax3 = axes[1, 0]
ax3.plot(t, v_salida, 'm-', linewidth=2)
ax3.set_xlabel('Tiempo [s]', fontsize=11)
ax3.set_ylabel('Velocidad de salida v(t) [m/s]', fontsize=11)
ax3.set_title('Velocidad de Salida vs Tiempo', fontsize=12)
ax3.grid(True, alpha=0.35)
ax3.set_xlim([0, t_total])

# --- Caudal de salida ---
ax4 = axes[1, 1]
ax4.fill_between(t, Q_salida * 1e4, alpha=0.4, color='cyan', label='Caudal Q(t)')
ax4.plot(t, Q_salida * 1e4, 'c-', linewidth=2)
ax4.set_xlabel('Tiempo [s]', fontsize=11)
ax4.set_ylabel('Caudal Q(t) [cm²·m/s]  ×10⁻⁴', fontsize=10)
ax4.set_title('Caudal de Salida vs Tiempo', fontsize=12)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.35)
ax4.set_xlim([0, t_total])

plt.tight_layout()
plt.savefig('grafica_resultados.png', dpi=150, bbox_inches='tight')
print("Guardada: grafica_resultados.png")
plt.close()

# ============================================================
# FIGURA 2: Diagrama esquemático del sistema
# ============================================================
fig2, ax_esq = plt.subplots(figsize=(6, 7))
ax_esq.set_xlim(0, 10)
ax_esq.set_ylim(-1, 10)
ax_esq.set_aspect('equal')
ax_esq.axis('off')
ax_esq.set_title('Diagrama del Sistema: Ley de Torricelli', fontsize=13, fontweight='bold')

# Paredes del tanque
tank_x, tank_y = 2, 1
tank_w, tank_h = 6, 7
wall_kw = dict(linewidth=3, edgecolor='#333333', facecolor='none')
left_wall  = patches.Rectangle((tank_x, tank_y), 0.15, tank_h, **wall_kw)
right_wall = patches.Rectangle((tank_x + tank_w - 0.15, tank_y), 0.15, tank_h, **wall_kw)
bottom     = patches.Rectangle((tank_x, tank_y), tank_w, 0.15, **wall_kw)
ax_esq.add_patch(patches.Rectangle((tank_x, tank_y), 0.15, tank_h,
                                    linewidth=2, edgecolor='#333', facecolor='none'))
ax_esq.add_patch(patches.Rectangle((tank_x + tank_w - 0.15, tank_y), 0.15, tank_h,
                                    linewidth=2, edgecolor='#333', facecolor='none'))
ax_esq.add_patch(patches.Rectangle((tank_x, tank_y), tank_w, 0.15,
                                    linewidth=2, edgecolor='#333', facecolor='none'))

# Agua (60% lleno para el diagrama)
nivel = 0.6
h_agua = tank_h * nivel
agua = patches.Rectangle((tank_x + 0.15, tank_y + 0.15), tank_w - 0.30, h_agua,
                           facecolor='#4da6ff', alpha=0.7, edgecolor='none')
ax_esq.add_patch(agua)

# Superficie libre
ax_esq.plot([tank_x + 0.15, tank_x + tank_w - 0.15],
            [tank_y + 0.15 + h_agua, tank_y + 0.15 + h_agua],
            'b-', linewidth=2)

# Orificio y chorro
orif_y = tank_y + 0.15
ax_esq.plot([tank_x + tank_w - 0.15, tank_x + tank_w + 1.0],
            [orif_y, orif_y - 0.8], 'b-', linewidth=3.5, label='Flujo de salida')
ax_esq.annotate('', xy=(tank_x + tank_w + 1.2, orif_y - 1.0),
                xytext=(tank_x + tank_w + 0.85, orif_y - 0.65),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))

# Cotas
# Flecha altura h(t)
ax_esq.annotate('', xy=(tank_x + tank_w + 0.3, tank_y + 0.15),
                xytext=(tank_x + tank_w + 0.3, tank_y + 0.15 + h_agua),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.8))
ax_esq.text(tank_x + tank_w + 0.55, tank_y + 0.15 + h_agua / 2,
            r'$h(t)$', color='red', fontsize=13, va='center')

# Anotación orificio
ax_esq.annotate(f'Orificio\n$a = {a_orificio*1e4:.1f}$ cm²',
                xy=(tank_x + tank_w - 0.1, orif_y),
                xytext=(tank_x + tank_w - 2.5, orif_y - 2.0),
                arrowprops=dict(arrowstyle='->', color='#555'),
                fontsize=9, color='#333')

# Ecuación en el gráfico
ax_esq.text(tank_x + tank_w / 2, 9.5,
            r'$\dfrac{dh}{dt} = -\dfrac{a}{A}\sqrt{2gh}$',
            fontsize=14, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fffbe6', edgecolor='#ccc'))

ax_esq.text(tank_x + 0.3, tank_y + tank_h + 0.35,
            f'$A = {A_tanque}$ m²', fontsize=10, color='#333')

plt.tight_layout()
plt.savefig('diagrama_sistema.png', dpi=150, bbox_inches='tight')
print("Guardada: diagrama_sistema.png")
plt.close()

# ============================================================
# ANIMACIÓN GIF
# ============================================================
print("Generando animación GIF...")

fig_anim, (ax_tank, ax_plot) = plt.subplots(1, 2, figsize=(11, 6),
                                             gridspec_kw={'width_ratios': [1, 2]})
fig_anim.patch.set_facecolor('#f0f4f8')

# --- Panel izquierdo: tanque ---
ax_tank.set_xlim(0, 4)
ax_tank.set_ylim(-0.3, h0 + 0.8)
ax_tank.set_aspect('equal')
ax_tank.axis('off')
ax_tank.set_title('Tanque en tiempo real', fontsize=11, fontweight='bold')

tw = 3.0; tx = 0.5; ty = 0.0
# Paredes
ax_tank.add_patch(patches.Rectangle((tx, ty), 0.1, h0 + 0.3, color='#555'))
ax_tank.add_patch(patches.Rectangle((tx + tw - 0.1, ty), 0.1, h0 + 0.3, color='#555'))
ax_tank.add_patch(patches.Rectangle((tx, ty), tw, 0.1, color='#555'))

agua_patch = patches.Rectangle((tx + 0.1, ty + 0.1), tw - 0.2, h0 - 0.1,
                                 facecolor='#3399ff', alpha=0.85, edgecolor='none')
ax_tank.add_patch(agua_patch)

linea_sup, = ax_tank.plot([], [], 'b-', linewidth=2)
texto_h    = ax_tank.text(tx + tw + 0.15, h0 / 2, '', fontsize=10, color='red',
                           va='center')
tiempo_txt = ax_tank.text(tx + tw / 2, h0 + 0.55, '', fontsize=10,
                           ha='center', color='#333')

# Chorro (parabólico)
chorro_x = np.linspace(0, 0.6, 30)
chorro_line, = ax_tank.plot([], [], 'b-', linewidth=2.5, alpha=0.8)

# --- Panel derecho: gráfica ---
ax_plot.set_facecolor('#fafafa')
ax_plot.set_xlim(0, t_total)
ax_plot.set_ylim(-0.05, h0 * 1.05)
ax_plot.set_xlabel('Tiempo [s]', fontsize=11)
ax_plot.set_ylabel('Altura h(t) [m]', fontsize=11)
ax_plot.set_title('Altura del Fluido vs Tiempo', fontsize=11, fontweight='bold')
ax_plot.grid(True, alpha=0.35)

# Curva analítica de fondo
ax_plot.plot(t, h_analitica, '#aaaaaa', linewidth=1.5, linestyle='--',
             label='Referencia analítica')

linea_sim, = ax_plot.plot([], [], 'b-', linewidth=2.5, label='Simulación')
punto_sim, = ax_plot.plot([], [], 'ro', markersize=6)
ax_plot.legend(fontsize=9, loc='upper right')

# Número de fotogramas
n_frames = 120
t_frames = np.linspace(0, t_total, n_frames)
h_frames = solucion_analitica(t_frames, h0, k)

def init():
    agua_patch.set_height(max(h0 - 0.1, 0))
    linea_sup.set_data([], [])
    texto_h.set_text('')
    tiempo_txt.set_text('')
    chorro_line.set_data([], [])
    linea_sim.set_data([], [])
    punto_sim.set_data([], [])
    return agua_patch, linea_sup, texto_h, tiempo_txt, chorro_line, linea_sim, punto_sim

def animate(i):
    ti = t_frames[i]
    hi = max(h_frames[i], 0)

    # Agua en el tanque
    agua_patch.set_height(max(hi - 0.1, 0))
    linea_sup.set_data([tx + 0.1, tx + tw - 0.1],
                       [ty + 0.1 + hi, ty + 0.1 + hi])

    # Chorro parabólico
    v_chorro = np.sqrt(max(2 * g * hi, 0))
    chorro_y = ty + 0.1 - 0.5 * g * (chorro_x / max(v_chorro, 0.01)) ** 2
    chorro_line.set_data(tx + tw - 0.1 + chorro_x, chorro_y)

    # Textos
    texto_h.set_text(f'h={hi:.2f} m')
    texto_h.set_y(ty + max(hi / 2, 0.15))
    tiempo_txt.set_text(f't = {ti:.1f} s')

    # Color del agua según nivel
    frac = hi / h0
    r = int(0 + (1 - frac) * 100)
    g_c = int(100 + frac * 55)
    b_c = int(255)
    agua_patch.set_facecolor((r/255, g_c/255, b_c/255))

    # Gráfica dinámica
    mask = t_frames[:i+1] <= t_total
    linea_sim.set_data(t_frames[:i+1][mask], h_frames[:i+1][mask])
    punto_sim.set_data([ti], [hi])

    return agua_patch, linea_sup, texto_h, tiempo_txt, chorro_line, linea_sim, punto_sim

anim = animation.FuncAnimation(fig_anim, animate, init_func=init,
                                frames=n_frames, interval=80, blit=True)

plt.tight_layout(pad=1.5)

try:
    from matplotlib.animation import PillowWriter
    writer = PillowWriter(fps=15)
    anim.save('animacion_tanque.gif', writer=writer, dpi=100)
    print("Guardado: animacion_tanque.gif")
except Exception as e:
    print(f"Error al guardar GIF: {e}")
    plt.savefig('animacion_tanque_frame.png', dpi=120)
    print("Guardado frame estático: animacion_tanque_frame.png")

plt.close()

# ============================================================
# RESUMEN EN CONSOLA
# ============================================================
print("\n" + "="*55)
print("        RESUMEN DE RESULTADOS - LEY DE TORRICELLI")
print("="*55)
print(f"  Área del tanque (A):        {A_tanque:.4f} m²")
print(f"  Área del orificio (a):      {a_orificio*1e4:.2f} cm²  =  {a_orificio:.5f} m²")
print(f"  Constante k = (a/A)√(2g):  {k:.6f} m^(1/2)/s")
print(f"  Altura inicial h₀:          {h0:.2f} m")
print(f"  Tiempo de vaciado (analít): {t_vacio_analitico:.2f} s  ≈  {t_vacio_analitico/60:.2f} min")
print(f"  Velocidad inicial v₀:       {np.sqrt(2*g*h0):.4f} m/s")
print(f"  Caudal inicial Q₀:          {a_orificio*np.sqrt(2*g*h0)*1e4:.4f} ×10⁻⁴ m³/s")
print(f"  Error máx. numérico:        {np.max(np.abs(h_analitica - h_numerica)):.2e} m")
print("="*55)
print("\nArchivos generados:")
print("  - grafica_resultados.png")
print("  - diagrama_sistema.png")
print("  - animacion_tanque.gif")
