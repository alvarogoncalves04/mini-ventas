# 05_automatizacion.py
# AUTOMATIZACIÓN DEL ETL DE VENTAS

import schedule
import time
from datetime import datetime
import subprocess
import os

def ejecutar_etl():
    """Ejecuta el pipeline ETL"""
    print(f"\n🚀 Ejecutando ETL de ventas a las {datetime.now()}")
    try:
        subprocess.run(["py", "src/02_etl_pipeline.py"], check=True)
        print("✅ ETL completado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error en ETL: {e}")
        return False

def generar_reporte():
    """Genera un reporte rápido de ventas del día"""
    import sqlite3
    import pandas as pd
    
    try:
        conn = sqlite3.connect('data/olap.db')
        
        # Obtener la fecha más reciente en los datos
        query_fecha = "SELECT MAX(fecha) as ultima_fecha FROM ventas_olap"
        df_fecha = pd.read_sql_query(query_fecha, conn)
        ultima_fecha = df_fecha['ultima_fecha'].iloc[0]
        
        # Reporte del último día disponible
        query = f"""
        SELECT 
            COUNT(*) as pedidos,
            SUM(total_venta) as ingresos,
            AVG(total_venta) as ticket_promedio
        FROM ventas_olap
        WHERE fecha = '{ultima_fecha}'
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        print(f"\n📊 Resumen del último día ({ultima_fecha}):")
        print(f"   - Pedidos: {df['pedidos'].iloc[0]}")
        print(f"   - Ingresos: ${df['ingresos'].iloc[0]:,.2f}")
        print(f"   - Ticket promedio: ${df['ticket_promedio'].iloc[0]:,.2f}")
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")

def trabajo_completo():
    """Ejecuta ETL + genera reporte"""
    if ejecutar_etl():
        generar_reporte()

def iniciar_programador():
    """Inicia el programador de tareas"""
    print("="*60)
    print("⏰ PROGRAMADOR DE VENTAS INICIADO")
    print("="*60)
    print("📅 Tareas programadas:")
    print("   - 8:00 AM: ETL diario")
    print("   - 8:00 PM: ETL diario")
    print("="*60)
    
    # Programar tareas
    schedule.every().day.at("08:00").do(trabajo_completo)
    schedule.every().day.at("20:00").do(trabajo_completo)
    
    # Ejecutar al inicio (para probar)
    print("\n🧪 Ejecutando tarea inicial...")
    trabajo_completo()
    
    print("\n⏳ Esperando siguientes tareas programadas...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    iniciar_programador()