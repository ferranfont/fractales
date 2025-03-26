import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from datetime import timedelta


# Ruta y nombre del archivo separados
carpeta = "DATA"
nombre_archivo = "AAPL_D_from2020.csv"
ruta_completa = os.path.join("..",carpeta, nombre_archivo)
df = pd.read_csv(ruta_completa)
print(df.columns)

# limpiar la data
df['fecha'] = pd.to_datetime(df['date']).dt.normalize()
df = df.drop(columns=['date','unadjusted_close','Unnamed: 0','record_no','exchange'])
columnas = ['fecha'] + [col for col in df.columns if col != 'fecha']
df = df[columnas]
df = df.set_index('fecha')
df = df.sort_index()
print(df.dtypes)
print(df.head())

'''
# Graficar columna 'close'
df['close'].plot(figsize=(12, 6), title='AAPL')
plt.xlabel('Fecha')
plt.ylabel('Precio de Cierre')
plt.grid(axis='y') 
plt.show()'
'''

# busqueda de los fractales
data = df.reset_index()
data = df[['close']]
print(data)

'''
plt.figure(figsize=(12, 6))
plt.plot(data)
plt.title("Fractales  AAPL")
plt.xlabel('Unidades de tiempo')
plt.ylabel('Precio')
plt.grid(axis='y') 
plt.show()
'''

'''
picos, props = signal.find_peaks(data['close'], width=1)
print(f"Picos: {(picos)}")

plt.figure(figsize=(12, 6))
plt.plot(data, label='Precio')
plt.plot(data.iloc[picos], 'ro', label='Picos')  # puntos rojos en picos
plt.title("Fractales AAPL - Picos detectados")
plt.xlabel('Unidades de tiempo')
plt.ylabel('Precio')
plt.grid(axis='y')
plt.legend()
plt.show()
'''


'''
picos, propiedades = signal.find_peaks(data['close'], prominence=1)
picos_prominentes = propiedades['prominences']
indice_pico1 = picos[np.argmax(picos_prominentes)]
indice_pico2 = picos[np.argpartition(picos_prominentes, -2)[-2]]

plt.figure(figsize=(12, 6))
plt.plot(data['close'], label='Precio')
plt.plot(picos, data['close'].iloc[picos], 'ro', alpha=0.5, label='Todos los picos')

# Marcar los dos más prominentes
plt.plot(indice_pico1, data['close'].iloc[indice_pico1], 'go', markersize=10, label='Pico + prominente')
plt.plot(indice_pico2, data['close'].iloc[indice_pico2], 'bo', markersize=10, label='2º más prominente')

plt.title("Fractales AAPL - Picos prominentes")
plt.xlabel('Unidades de tiempo')
plt.ylabel('Precio')
plt.grid(axis='y')
plt.legend()
plt.show()
'''

# NO usar reset_index() si ya está la fecha como índice
data = df[['close']]

# Detectar todos los picos con prominencia
picos, propiedades = signal.find_peaks(data['close'], prominence=1)
picos_prominentes = propiedades['prominences']

# Obtener los índices de los 5 picos más prominentes
indices_top15 = picos[np.argsort(picos_prominentes)[-15:]]

# Obtener fechas de esos picos
fechas_top15 = data.index[indices_top15]
valores_top15 = data['close'].iloc[indices_top15]


- data['close']
# --- Picos (máximos locales) ---
picos, props_picos = signal.find_peaks(data['close'], prominence=1)
top_picos = picos[np.argsort(props_picos['prominences'])[-15:]]
fechas_picos = data.index[top_picos]
valores_picos = data['close'].iloc[top_picos]

# --- Valles (mínimos locales) ---
valles, props_valles = signal.find_peaks(-data['close'], prominence=1)
top_valles = valles[np.argsort(props_valles['prominences'])[-15:]]
fechas_valles = data.index[top_valles]
valores_valles = data['close'].iloc[top_valles]

# --- Graficar ---
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['close'], label='Precio')

# Todos los picos (marcados en rojo claro)
plt.plot(data.index[picos], data['close'].iloc[picos], 'ro', alpha=0.3, label='Todos los picos')

# Top 15 picos prominentes (verde)
plt.plot(fechas_picos, valores_picos, 'go', markersize=8, label='Top 15 picos')

# Top 15 valles prominentes (azul)
plt.plot(fechas_valles, valores_valles, 'bo', markersize=8, label='Top 15 valles')

plt.title("Fractales AAPL - Top 15 Picos y Valles Prominentes")
plt.xlabel("Fecha")
plt.ylabel("Precio")
plt.grid(axis='y')
plt.legend()
plt.show()

# --- Imprimir los top 15 picos y valles ---
print("Top 15 Picos:")
for i in range(len(top_picos)):
    print(f"{i+1}. Fecha: {fechas_picos[i].date()} - Precio: {valores_picos.iloc[i]:.2f}")

print("\nTop 15 Valles:")
for i in range(len(top_valles)):
    print(f"{i+1}. Fecha: {fechas_valles[i].date()} - Precio: {valores_valles.iloc[i]:.2f}")

# Asegurar que fechas estén ordenadas
fechas_picos = fechas_picos.sort_values()
fechas_valles = fechas_valles.sort_values()

# Almacenar resultados
distancias = []

for fecha_valle in fechas_valles:
    # Calcular la diferencia de tiempo entre este valle y todos los picos
    diferencias = abs(fechas_picos - fecha_valle)
    
    # Encontrar el pico más cercano
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
    print(f"Valle: {d['fecha_valle']} (${d['precio_valle']:.2f})  →  "
    f"Pico más cercano: {d['fecha_pico_mas_cercano']} (${d['precio_pico']:.2f})  "
    f"| Δt = {d['dias_diferencia']} días")




