import matplotlib.pyplot as plt

def graficar_picos_valles(data, picos_todos, fechas_picos, valores_picos, fechas_valles, valores_valles):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['close'], label='Precio', linewidth=1.2)

    # Todos los picos (rojo claro)
    plt.plot(data.index[picos_todos], data['close'].iloc[picos_todos], 'ro', alpha=0.3, label='Todos los picos')

    # Top 15 picos (verde)
    plt.plot(fechas_picos, valores_picos, 'go', markersize=8, label='Top 15 picos')

    # Top 15 valles (azul)
    plt.plot(fechas_valles, valores_valles, 'bo', markersize=8, label='Top 15 valles')

    plt.title("Fractales AAPL - Top 15 Picos y Valles Prominentes")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(axis='y')
    plt.legend()
    plt.tight_layout()
    plt.show()

