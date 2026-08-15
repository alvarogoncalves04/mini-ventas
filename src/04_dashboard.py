# 04_dashboard.py
# DASHBOARD DE VENTAS CON STREAMLIT

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Ventas - Tienda Online")
st.markdown("---")

# ============================================
# CARGAR DATOS
# ============================================
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect('data/olap.db')
    df = pd.read_sql_query("SELECT * FROM ventas_olap", conn)
    conn.close()
    
    # Convertir fecha
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Crear columna de año-mes para filtros
    df['ano_mes'] = df['fecha'].dt.strftime('%Y-%m')
    
    return df

df = cargar_datos()

# ============================================
# FILTROS LATERALES
# ============================================
st.sidebar.header("🔍 Filtros")

# Filtro de fechas
st.sidebar.subheader("📅 Rango de Fechas")
fecha_min = df['fecha'].min().date()
fecha_max = df['fecha'].max().date()
fecha_inicio = st.sidebar.date_input("Fecha Inicio", fecha_min, min_value=fecha_min, max_value=fecha_max)
fecha_fin = st.sidebar.date_input("Fecha Fin", fecha_max, min_value=fecha_min, max_value=fecha_max)

# Filtro por categoría
categorias = st.sidebar.multiselect(
    "Categoría",
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

# Filtro por ciudad
ciudades = st.sidebar.multiselect(
    "Ciudad",
    options=df['ciudad'].unique(),
    default=df['ciudad'].unique()
)

# Aplicar filtros
df_filtrado = df[
    (df['fecha'].dt.date >= fecha_inicio) &
    (df['fecha'].dt.date <= fecha_fin) &
    (df['categoria'].isin(categorias)) &
    (df['ciudad'].isin(ciudades))
]

# ============================================
# FILA 1: MÉTRICAS
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Ingresos Totales",
        f"${df_filtrado['total_venta'].sum():,.2f}"
    )

with col2:
    st.metric(
        "📦 Pedidos Totales",
        f"{len(df_filtrado):,}"
    )

with col3:
    st.metric(
        "🧾 Ticket Promedio",
        f"${df_filtrado['total_venta'].mean():,.2f}"
    )

with col4:
    st.metric(
        "📈 Margen Promedio",
        f"{df_filtrado['margen_porcentaje'].mean():.1f}%"
    )

st.markdown("---")

# ============================================
# FILA 2: GRÁFICOS
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Ventas por Categoría")
    fig, ax = plt.subplots()
    df_cat = df_filtrado.groupby('categoria')['total_venta'].sum().sort_values(ascending=True)
    ax.barh(df_cat.index, df_cat.values, color='#3498db')
    ax.set_xlabel("Ingresos ($)")
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("🏙️ Ventas por Ciudad")
    fig, ax = plt.subplots()
    df_ciudad = df_filtrado.groupby('ciudad')['total_venta'].sum().sort_values(ascending=False).head(8)
    ax.bar(df_ciudad.index, df_ciudad.values, color='#2ecc71')
    ax.set_ylabel("Ingresos ($)")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close()

# ============================================
# FILA 3: GRÁFICOS
# ============================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Tendencia de Ventas (Últimos 6 meses)")
    fig, ax = plt.subplots()
    df_tendencia = df_filtrado.groupby('fecha')['total_venta'].sum().reset_index()
    # Filtrar últimos 6 meses
    fecha_limite = df_filtrado['fecha'].max() - pd.DateOffset(months=6)
    df_tendencia_filtrado = df_tendencia[df_tendencia['fecha'] >= fecha_limite]
    ax.plot(df_tendencia_filtrado['fecha'], df_tendencia_filtrado['total_venta'], color='#e74c3c', linewidth=2)
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Ingresos ($)")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("💳 Métodos de Pago")
    fig, ax = plt.subplots()
    df_pago = df_filtrado.groupby('metodo_pago')['total_venta'].sum()
    ax.pie(df_pago.values, labels=df_pago.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
    plt.close()

# ============================================
# FILA 4: TABLA DE DATOS
# ============================================
st.subheader("📋 Datos Filtrados")

columnas_mostrar = ['fecha', 'cliente', 'producto', 'categoria', 'cantidad', 'total_venta', 'ciudad', 'metodo_pago']
df_mostrar = df_filtrado[columnas_mostrar].copy()
df_mostrar['fecha'] = df_mostrar['fecha'].dt.strftime('%Y-%m-%d')
st.dataframe(df_mostrar, use_container_width=True)

# ============================================
# DESCARGA DE DATOS
# ============================================
st.markdown("---")
if st.button("📥 Descargar datos filtrados (CSV)"):
    csv = df_filtrado.to_csv(index=False)
    st.download_button(
        label="Click para descargar",
        data=csv,
        file_name=f"ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )   