# 01_generar_datos.py
# Genera 100,000 pedidos falsos para una tienda online (OLTP)

import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# ============================================
# CONFIGURACIÓN
# ============================================
fake = Faker('es_ES')
NUM_PEDIDOS = 100000

# Listas para generar datos realistas
PRODUCTOS = [
    ('Laptop', 'Electrónicos', 800, 1500),
    ('Smartphone', 'Electrónicos', 400, 900),
    ('Auriculares', 'Electrónicos', 50, 200),
    ('Monitor', 'Electrónicos', 200, 500),
    ('Teclado', 'Electrónicos', 30, 120),
    ('Mouse', 'Electrónicos', 15, 60),
    ('Silla', 'Muebles', 150, 400),
    ('Mesa', 'Muebles', 100, 350),
    ('Estantería', 'Muebles', 80, 250),
    ('Lámpara', 'Hogar', 20, 80),
    ('Sofá', 'Muebles', 300, 800),
    ('TV 50"', 'Electrónicos', 500, 1200),
    ('Tablet', 'Electrónicos', 200, 600),
    ('Reloj Inteligente', 'Electrónicos', 100, 350),
    ('Cafetera', 'Hogar', 50, 150),
    ('Aspiradora', 'Hogar', 80, 250),
    ('Licuadora', 'Hogar', 30, 100),
    ('Microondas', 'Hogar', 80, 200),
    ('Refrigerador', 'Hogar', 500, 1200),
    ('Lavadora', 'Hogar', 400, 900),
]

CIUDADES = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Bucaramanga', 'Pereira', 'Manizales']
METODOS_PAGO = ['Tarjeta Crédito', 'Tarjeta Débito', 'PayPal', 'Transferencia', 'Efectivo']

# ============================================
# FUNCIONES
# ============================================
def generar_pedidos(n):
    """Genera n pedidos falsos"""
    pedidos = []
    
    for i in range(n):
        # Seleccionar producto aleatorio
        producto = random.choice(PRODUCTOS)
        nombre_producto = producto[0]
        categoria = producto[1]
        precio_min = producto[2]
        precio_max = producto[3]
        
        # Precio unitario dentro del rango
        precio_unitario = round(random.uniform(precio_min, precio_max), 2)
        
        # Cantidad (1 a 5 unidades)
        cantidad = random.randint(1, 5)
        
        # Fecha en los últimos 6 meses
        fecha = fake.date_between(start_date='-180d', end_date='today')
        
        # Cliente
        cliente = fake.name()
        
        # Ciudad
        ciudad = random.choice(CIUDADES)
        
        # Método de pago
        metodo_pago = random.choice(METODOS_PAGO)
        
        pedidos.append({
            'id_pedido': i + 1,
            'fecha': fecha.strftime('%Y-%m-%d'),
            'cliente': cliente,
            'producto': nombre_producto,
            'categoria': categoria,
            'precio_unitario': precio_unitario,
            'cantidad': cantidad,
            'ciudad': ciudad,
            'metodo_pago': metodo_pago
        })
    
    return pd.DataFrame(pedidos)

def guardar_en_oltp(df):
    """Guarda los datos en la base de datos OLTP"""
    import os
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/oltp.db')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS pedidos_oltp (
        id_pedido INTEGER PRIMARY KEY,
        fecha TEXT,
        cliente TEXT,
        producto TEXT,
        categoria TEXT,
        precio_unitario REAL,
        cantidad INTEGER,
        ciudad TEXT,
        metodo_pago TEXT
    )
    ''')
    
    df.to_sql('pedidos_oltp', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ {len(df)} pedidos guardados en OLTP (data/oltp.db)")

# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    print("="*60)
    print("🚀 GENERANDO DATOS DE VENTAS (OLTP)")
    print("="*60)
    print(f"📊 Generando {NUM_PEDIDOS} pedidos...")
    
    df = generar_pedidos(NUM_PEDIDOS)
    
    print("\n📋 Ejemplo de datos generados:")
    print(df.head())
    
    guardar_en_oltp(df)
    
    print("\n🔍 Resumen de datos:")
    print(f"Total pedidos: {len(df):,}")
    print(f"Categorías: {df['categoria'].unique()}")
    print(f"Ciudades: {df['ciudad'].unique()}")
    print(f"Precio promedio: ${df['precio_unitario'].mean():,.2f}")
    print(f"Ingreso total estimado: ${(df['precio_unitario'] * df['cantidad']).sum():,.2f}")
    print("="*60)