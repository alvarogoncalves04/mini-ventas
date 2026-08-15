# 02_etl_pipeline.py
# PIPELINE ETL PARA VENTAS: Extraer → Transformar → Cargar

import sqlite3
import pandas as pd
from datetime import datetime
import os

# ============================================
# 1. EXTRACCIÓN (E)
# ============================================
def extraer_de_oltp():
    conn = sqlite3.connect('data/oltp.db')
    df = pd.read_sql_query("SELECT * FROM pedidos_oltp", conn)
    conn.close()
    print(f"📤 Extraídos {len(df)} pedidos de OLTP")
    return df

# ============================================
# 2. TRANSFORMACIÓN (T)
# ============================================
def transformar_datos(df):
    print("🔄 Transformando datos...")
    df_clean = df.copy()
    
    # 1. Calcular total_venta
    df_clean['total_venta'] = df_clean['precio_unitario'] * df_clean['cantidad']
    
    # 2. Calcular costo estimado (60% del precio para márgenes)
    df_clean['costo_estimado'] = round(df_clean['precio_unitario'] * 0.60, 2)
    df_clean['margen_bruto'] = round(df_clean['total_venta'] - (df_clean['costo_estimado'] * df_clean['cantidad']), 2)
    df_clean['margen_porcentaje'] = round((df_clean['margen_bruto'] / df_clean['total_venta']) * 100, 2)
    
    # 3. Clasificar ventas por monto
    def clasificar_venta(total):
        if total < 100:
            return 'Baja'
        elif total < 500:
            return 'Media'
        else:
            return 'Alta'
    df_clean['categoria_venta'] = df_clean['total_venta'].apply(clasificar_venta)
    
    # 4. Extraer mes, trimestre y año
    df_clean['fecha'] = pd.to_datetime(df_clean['fecha'])
    df_clean['mes'] = df_clean['fecha'].dt.month
    df_clean['trimestre'] = df_clean['fecha'].dt.quarter
    df_clean['año'] = df_clean['fecha'].dt.year
    df_clean['dia_semana'] = df_clean['fecha'].dt.dayofweek  # 0=Lunes, 6=Domingo
    
    # 5. Clasificar día (fin de semana vs laboral)
    df_clean['es_fin_semana'] = df_clean['dia_semana'].isin([5, 6])
    
    # 6. Agregar fecha de procesamiento
    df_clean['fecha_procesamiento'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"✅ Transformación completada")
    print(f"   - Ingreso total: ${df_clean['total_venta'].sum():,.2f}")
    print(f"   - Margen promedio: {df_clean['margen_porcentaje'].mean():.2f}%")
    print(f"   - Ventas Alta categoría: {df_clean[df_clean['categoria_venta'] == 'Alta'].shape[0]}")
    
    return df_clean

# ============================================
# 3. CARGA (L) - Data Warehouse
# ============================================
def cargar_en_olap(df):
    print("📥 Cargando en Data Warehouse (OLAP)...")
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/olap.db')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS ventas_olap (
        id_pedido INTEGER PRIMARY KEY,
        fecha TEXT,
        cliente TEXT,
        producto TEXT,
        categoria TEXT,
        precio_unitario REAL,
        cantidad INTEGER,
        ciudad TEXT,
        metodo_pago TEXT,
        total_venta REAL,
        costo_estimado REAL,
        margen_bruto REAL,
        margen_porcentaje REAL,
        categoria_venta TEXT,
        mes INTEGER,
        trimestre INTEGER,
        año INTEGER,
        dia_semana INTEGER,
        es_fin_semana INTEGER,
        fecha_procesamiento TEXT
    )
    ''')
    
    df.to_sql('ventas_olap', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ {len(df)} registros cargados en OLAP")

# ============================================
# EJECUTAR
# ============================================
def ejecutar_etl():
    print("="*60)
    print("🚀 PIPELINE ETL - VENTAS")
    print("="*60)
    df_raw = extraer_de_oltp()
    df_clean = transformar_datos(df_raw)
    cargar_en_olap(df_clean)
    print("\n✅ PIPELINE ETL COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    ejecutar_etl()