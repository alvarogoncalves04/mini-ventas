# 06_machine_learning.py
# PREDICCIÓN DE VENTAS CON MACHINE LEARNING

import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

def cargar_datos():
    conn = sqlite3.connect('data/olap.db')
    df = pd.read_sql_query("SELECT * FROM ventas_olap", conn)
    conn.close()
    return df

def preparar_datos(df):
    """Prepara datos para el modelo de regresión"""
    
    features = [
        'precio_unitario',
        'cantidad',
        'mes',
        'trimestre',
        'dia_semana',
        'es_fin_semana'
    ]
    
    target = 'total_venta'
    
    X = df[features].copy()
    y = df[target].copy()
    
    scaler = StandardScaler()
    X['precio_unitario'] = scaler.fit_transform(X[['precio_unitario']])
    X['cantidad'] = scaler.fit_transform(X[['cantidad']])
    
    return X, y, scaler

def entrenar_modelo(X, y):
    """Entrena modelo de Regresión Random Forest"""
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Datos de entrenamiento: {len(X_train)}")
    print(f"📊 Datos de prueba: {len(X_test)}")
    
    rf = RandomForestRegressor(
        n_estimators=50,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    
    print("\n" + "="*50)
    print("📊 EVALUACIÓN DEL MODELO")
    print("="*50)
    print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
    print(f"Error Absoluto Medio (MAE): ${mean_absolute_error(y_test, y_pred):,.2f}")
    print(f"Error Cuadrático Medio (RMSE): ${np.sqrt(mean_squared_error(y_test, y_pred)):,.2f}")
    
    print("\n📌 IMPORTANCIA DE VARIABLES:")
    for feature, importance in zip(X.columns, rf.feature_importances_):
        print(f"  - {feature}: {importance:.2%}")
    
    joblib.dump(rf, 'modelo_ventas.pkl')
    joblib.dump(scaler, 'scaler_ventas.pkl')
    print("\n✅ Modelo guardado: modelo_ventas.pkl")
    
    return rf, scaler

def predecir_venta(precio, cantidad, mes, trimestre, dia_semana, es_fin_semana):
    """Predice el total de una venta"""
    
    modelo = joblib.load('modelo_ventas.pkl')
    scaler = joblib.load('scaler_ventas.pkl')
    
    datos = np.array([[
        precio,
        cantidad,
        mes,
        trimestre,
        dia_semana,
        es_fin_semana
    ]])
    
    datos[0, 0] = scaler.transform([[precio]])[0, 0]
    datos[0, 1] = scaler.transform([[cantidad]])[0, 0]
    
    prediccion = modelo.predict(datos)[0]
    return prediccion

if __name__ == "__main__":
    print("="*60)
    print("🤖 PREDICCIÓN DE VENTAS CON MACHINE LEARNING")
    print("="*60)
    
    df = cargar_datos()
    print(f"📊 Datos cargados: {len(df)} registros")
    
    X, y, scaler = preparar_datos(df)
    modelo, scaler = entrenar_modelo(X, y)
    
    print("\n" + "="*50)
    print("🧪 PRUEBA CON NUEVA VENTA")
    print("="*50)
    
    prediccion = predecir_venta(
        precio=500,
        cantidad=3,
        mes=12,
        trimestre=4,
        dia_semana=5,
        es_fin_semana=1
    )
    
    print(f"🔍 Venta: 3 unidades a $500 cada una (diciembre, sábado)")
    print(f"📊 Total predicho: ${prediccion:,.2f}")
    print(f"📊 Total real esperado: $1,500.00")