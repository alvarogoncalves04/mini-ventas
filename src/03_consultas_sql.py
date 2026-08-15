# 03_consultas_sql.py
# CONSULTAS ANALÍTICAS SOBRE EL DATA WAREHOUSE (OLAP)

import sqlite3
import pandas as pd

def conectar_olap():
    return sqlite3.connect('data/olap.db')

def ejecutar_consulta(query, descripcion):
    print(f"\n📊 {descripcion}")
    print("-"*60)
    conn = conectar_olap()
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)
    print(f"\nTotal registros: {len(df)}")
    return df

def consultas_analiticas():
    print("="*60)
    print("🔍 CONSULTAS ANALÍTICAS - VENTAS")
    print("="*60)
    
    # 1. Producto más vendido en cantidad
    query1 = """
    SELECT 
        producto,
        SUM(cantidad) as total_unidades,
        COUNT(*) as num_pedidos,
        AVG(precio_unitario) as precio_promedio
    FROM ventas_olap
    GROUP BY producto
    ORDER BY total_unidades DESC
    LIMIT 10
    """
    ejecutar_consulta(query1, "1. TOP 10 PRODUCTOS MÁS VENDIDOS (UNIDADES)")
    
    # 2. Ingresos por ciudad
    query2 = """
    SELECT 
        ciudad,
        COUNT(*) as pedidos,
        SUM(total_venta) as ingresos_totales,
        AVG(total_venta) as ticket_promedio
    FROM ventas_olap
    GROUP BY ciudad
    ORDER BY ingresos_totales DESC
    """
    ejecutar_consulta(query2, "2. INGRESOS POR CIUDAD")
    
    # 3. Top 5 clientes que más gastan
    query3 = """
    SELECT 
        cliente,
        COUNT(*) as pedidos,
        SUM(total_venta) as total_gastado,
        AVG(total_venta) as ticket_promedio
    FROM ventas_olap
    GROUP BY cliente
    ORDER BY total_gastado DESC
    LIMIT 10
    """
    ejecutar_consulta(query3, "3. TOP 10 CLIENTES QUE MÁS GASTAN")
    
    # 4. Ventas por mes
    query4 = """
    SELECT 
        año,
        mes,
        COUNT(*) as pedidos,
        SUM(total_venta) as ingresos,
        AVG(total_venta) as ticket_promedio
    FROM ventas_olap
    GROUP BY año, mes
    ORDER BY año, mes
    """
    ejecutar_consulta(query4, "4. VENTAS POR MES")
    
    # 5. Margen por categoría
    query5 = """
    SELECT 
        categoria,
        COUNT(*) as pedidos,
        SUM(total_venta) as ingresos,
        AVG(margen_porcentaje) as margen_promedio,
        SUM(margen_bruto) as margen_total
    FROM ventas_olap
    GROUP BY categoria
    ORDER BY margen_promedio DESC
    """
    ejecutar_consulta(query5, "5. MARGEN POR CATEGORÍA")
    
    # 6. Ventas fin de semana vs laboral
    query6 = """
    SELECT 
        CASE 
            WHEN es_fin_semana = 1 THEN 'Fin de Semana'
            ELSE 'Laboral'
        END as tipo_dia,
        COUNT(*) as pedidos,
        SUM(total_venta) as ingresos,
        AVG(total_venta) as ticket_promedio
    FROM ventas_olap
    GROUP BY es_fin_semana
    """
    ejecutar_consulta(query6, "6. VENTAS FIN DE SEMANA VS LABORAL")
    
    # 7. Métodos de pago más usados
    query7 = """
    SELECT 
        metodo_pago,
        COUNT(*) as pedidos,
        SUM(total_venta) as ingresos,
        AVG(total_venta) as ticket_promedio
    FROM ventas_olap
    GROUP BY metodo_pago
    ORDER BY pedidos DESC
    """
    ejecutar_consulta(query7, "7. MÉTODOS DE PAGO MÁS USADOS")

if __name__ == "__main__":
    consultas_analiticas()