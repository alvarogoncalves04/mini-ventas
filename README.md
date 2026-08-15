# Analisis de mini-ventas
# 📊 Mini Ventas - Análisis de Ventas de Tienda Online

## 📌 Descripción
Proyecto completo de análisis de datos para una tienda online. Incluye:

- Generación de 100,000 pedidos sintéticos
- Pipeline ETL (Extraer, Transformar, Cargar)
- Data Warehouse para análisis
- Dashboard interactivo con Streamlit
- Automatización de tareas
- Modelo de Machine Learning para predicción de ventas

## 🛠️ Tecnologías
- Python 3.x
- Pandas (manipulación de datos)
- SQLite (OLTP + OLAP)
- Streamlit (dashboard)
- Matplotlib (visualizaciones)
- Scikit-learn (Machine Learning)
- Schedule (automatización)

## 📁 Estructura del Proyecto
mini-ventas/
├── data/
│ ├── oltp.db # Base de datos transaccional
│ └── olap.db # Data Warehouse
├── src/
│ ├── 01_generar_datos.py # Genera 100,000 pedidos
│ ├── 02_etl_pipeline.py # Pipeline ETL
│ ├── 03_consultas_sql.py # Consultas analíticas
│ ├── 04_dashboard.py # Dashboard Streamlit
│ ├── 05_automatizacion.py # Automatización
│ └── 06_machine_learning.py # Predicción de ventas
├── requirements.txt
└── README.md

## 📊 Análisis Realizado

### Métricas de Negocio
- Ingresos totales por categoría y ciudad
- Productos más vendidos
- Clientes que más gastan
- Ticket promedio
- Margen de ganancia por categoría
- Métodos de pago más usados

### Reglas de Negocio
- Clasificación de ventas: Baja, Media, Alta
- Margen bruto y porcentaje
- Análisis de fin de semana vs días laborales

## 🤖 Machine Learning
- **Modelo:** Random Forest Regressor
- **Variables:** precio unitario, cantidad, mes, trimestre, día de semana, fin de semana
- **Métrica principal:** R² Score
- **Aplicación:** Predicción del monto total de una venta

## ⏰ Automatización
- Tareas programadas a las 8:00 AM y 8:00 PM
- Ejecución automática del ETL
- Generación de reportes del último día

👤 Autor
Alvaro Goncalves
https://mini-ventas.streamlit.app/      