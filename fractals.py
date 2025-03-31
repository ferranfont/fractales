import pandas as pd
import os
import numpy as np
import scipy.signal as signal
import config
from chart import graficar_picos_valles

# Ruta y nombre del archivo separados
carpeta = "DATA"
nombre_archivo = config.DATA_FILE
ruta_completa = os.path.join("..", carpeta, nombre_archivo)
df = pd.read_csv(ruta_completa)
print(df.columns)

# Limpiar la data
df['fecha'] = pd.to_datetime(df['date']).dt.normalize()
df = df.drop(columns=['date', 'unadjusted_close', 'Unnamed: 0', 'record_no', 'exchange'])
columnas = ['fecha'] + [col for col in df.columns if col != 'fecha']
df = df[columnas]
df = df.set_index('fecha')
df = df.sort_index()
print(df.dtypes)
print(df.head())

# Preparar columna 'close'
data = df[['close']]

# --- Picos ---
picos, props_picos = signal.find_peaks(data['close'], prominence=1)
top_picos = picos[np.argsort(props_picos['prominences'])[-15:]]
fechas_picos = data.index[top_picos]
valores_picos = data['close'].iloc[top_picos]

# --- Valles ---
valles, props_valles = signal.find_peaks(-data['close'], prominence=1)
top_valles = valles[np.argsort(props_valles['prominences'])[-15:]]
fechas_valles = data.index[top_valles]
valores_valles = data['close'].iloc[top_valles]

# --- Gráfico (llama módulo externo) ---
graficar_picos_valles(data, picos, fechas_picos, valores_picos, fechas_valles, valores_valles)

# --- Listado en consola ---
print("Top 15 Picos:")
for i in range(len(top_picos)):
    print(f"{i+1}. Fecha: {fechas_picos[i].date()} - Precio: {valores_picos.iloc[i]:.2f}")

print("\nTop 15 Valles:")
for i in range(len(top_valles)):
    print(f"{i+1}. Fecha: {fechas_valles[i].date()} - Precio: {valores_valles.iloc[i]:.2f}")

# --- Cálculo de distancias ---
fechas_picos = fechas_picos.sort_values()
fechas_valles = fechas_valles.sort_values()
distancias = []

for fecha_valle in fechas_valles:
    diferencias = abs(fechas_picos - fecha_valle)
    idx_mas_cercano = diferencias.argmin()
    fecha_pico = fechas_picos[idx_mas_cercano]
    valor_valle = data.loc[fecha_valle, 'close']
    valor_pico = data.loc[fecha_pico, 'close']
    dias = diferencias[idx_mas_cercano].days

    distancias.append({
        'fecha_valle': fecha_valle.date(),
        'precio_valle': valor_valle,
        'fecha_pico_mas_cercano': fecha_pico.date(),
        'precio_pico': valor_pico,
        'dias_diferencia': dias
    })

# Mostrar resultados
print("Distancia entre picos y valles:")
for d in distancias:
    print(f"Valle: {d['fecha_valle']} (${d['precio_valle']:.2f}) → "
          f"Pico más cercano: {d['fecha_pico_mas_cercano']} (${d['precio_pico']:.2f}) "
          f"| Δt = {d['dias_diferencia']} días")