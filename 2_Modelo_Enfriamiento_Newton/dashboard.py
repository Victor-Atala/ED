import streamlit as st
import time
import numpy as np
import pandas as pd
import os
from physics_core import resolver_simulacion, solucion_analitica
from graphics_lib import plot_resultados, generar_diagrama_esquematico

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Simulación Enfriamiento de Newton",
    page_icon="🔥",
    layout="wide"
)

# --- Estilos Personalizados ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #555555 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Parámetros del Sistema ---
st.sidebar.header("🛠️ Configuración del Sistema")
st.sidebar.markdown("Ajusta los parámetros físicos para ver el efecto en tiempo real.")

T0 = st.sidebar.slider("Temperatura Inicial ($T_0$)", 0.0, 150.0, 90.0, step=1.0)
Ta = st.sidebar.slider("Temperatura Ambiente ($T_a$)", -10.0, 50.0, 25.0, step=1.0)
k = st.sidebar.slider("Constante de Enfriamiento ($k$)", 0.01, 0.20, 0.05, step=0.01)

t_max = 5.0 / k  # Tiempo de estabilización sugerido
num_puntos = 120

# --- Título Principal ---
st.title("🌡️ Ley de Enfriamiento de Newton")
st.markdown("Explora de forma interactiva la disipación térmica de un sistema hacia su entorno.")
st.markdown("---")

# --- Métricas Principales ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Temp. Inicial ($T_0$)", value=f"{T0} °C", delta=f"Δ {T0 - Ta:.1f} °C vs Ambiente", delta_color="inverse")
with col_m2:
    st.metric(label="Temp. Ambiente ($T_a$)", value=f"{Ta} °C")
with col_m3:
    st.metric(label="Constante k", value=f"{k}")
with col_m4:
    st.metric(label="Tiempo Estabilización", value=f"{t_max:.1f} s")

st.markdown("---")

# --- Dashboard Principal ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Esquema del Sistema")
    fig_esq = generar_diagrama_esquematico(T0, Ta, k)
    st.pyplot(fig_esq)
    
    img_esq_path = os.path.join(os.path.dirname(__file__), "diagrama_sistema_termico.png")
    if os.path.exists(img_esq_path):
        st.image(img_esq_path, caption="Diagrama Estático del Sistema", use_container_width=True)
    
    st.info(f"""
    **Análisis Teórico:**
    Con una constante $k={k}$, el sistema alcanzará el equilibrio térmico en aproximadamente **{t_max:.1f} segundos**.
    """)
    
    with st.expander("📚 Fundamento Teórico", expanded=False):
        st.markdown(r"""
        La **Ley de Enfriamiento de Newton** postula que la tasa de cambio de temperatura de un cuerpo es proporcional a la diferencia de temperatura entre el cuerpo y su entorno:
        
        $$ \frac{dT}{dt} = -k(T - T_a) $$
        
        Integrando esta ecuación diferencial obtenemos su solución analítica:
        
        $$ T(t) = T_a + (T_0 - T_a) e^{-kt} $$
        """)

with col2:
    st.subheader("Evolución de la Temperatura")
    
    gif_path = os.path.join(os.path.dirname(__file__), "animacion_enfriamiento.gif")
    if os.path.exists(gif_path):
        st.image(gif_path, caption="Animación del Proceso de Enfriamiento", use_container_width=True)
    
    # Simulación en "Vivo"
    if st.button("🚀 Iniciar Simulación en Tiempo Real"):
        progress_bar = st.progress(0, text="Inicializando motor de cálculo...")
        plot_placeholder = st.empty()
        
        # Generar datos
        t_full, T_num, T_ana = resolver_simulacion(T0, Ta, k, t_max, num_puntos)
        
        # Instanciar gráfica una sola vez con el primer punto de datos
        df_init = pd.DataFrame({
            "Tiempo [s]": [t_full[0]],
            "Temperatura [°C]": [T_ana[0]]
        }).set_index("Tiempo [s]")
        chart = plot_placeholder.line_chart(df_init, color="#ff4b4b")
        
        for i in range(1, len(t_full)):
            # Inyectar únicamente el nuevo punto en cada iteración
            df_new = pd.DataFrame({
                "Tiempo [s]": [t_full[i]],
                "Temperatura [°C]": [T_ana[i]]
            }).set_index("Tiempo [s]")
            
            chart.add_rows(df_new)
            # Actualizar barra de progreso
            progreso = int((i / (len(t_full) - 1)) * 100)
            progress_bar.progress(progreso, text=f"Renderizando T={T_ana[i]:.1f} °C al t={t_full[i]:.1f}s")
            time.sleep(0.01) # Simular proceso
            
        progress_bar.progress(100, text="✨ Simulación completada con éxito.")
    else:
        # Gráfica estática inicial
        t_full, T_num, T_ana = resolver_simulacion(T0, Ta, k, t_max, num_puntos)
        df_init = pd.DataFrame({
            "Tiempo [s]": t_full,
            "Temperatura [°C]": T_ana
        }).set_index("Tiempo [s]")
        st.line_chart(df_init, color="#ff4b4b")

# --- Análisis Detallado ---
st.markdown("---")
st.subheader("📈 Análisis de Resultados Científicos")
tab1, tab2 = st.tabs(["📊 Comparativa de Soluciones", "📋 Tabla de Datos"])

with tab1:
    fig_res = plot_resultados(t_full, T_num, T_ana, Ta, T0, k)
    st.pyplot(fig_res)
    
    res_img_path = os.path.join(os.path.dirname(__file__), "grafica_resultados_termicos.png")
    if os.path.exists(res_img_path):
        st.image(res_img_path, caption="Gráfica Estática de Resultados Guardada", use_container_width=True)

with tab2:
    st.write("Datos generados por el integrador numérico:")
    st.dataframe(pd.DataFrame({
        "Tiempo (s)": t_full,
        "T. Numérica (°C)": T_num,
        "T. Analítica (°C)": T_ana,
        "Error (°C)": np.abs(T_num - T_ana)
    }), use_container_width=True)

# Footer
st.markdown("<br><hr><center>Desarrollado para el Proyecto de Ecuaciones Diferenciales</center>", unsafe_allow_html=True)
