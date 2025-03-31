import matplotlib.pyplot as plt
import os

def graficar_picos_valles(data, picos_todos, fechas_picos, valores_picos, fechas_valles, valores_valles):

    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['close'], label='Precio', linewidth=1.2)
    plt.xticks(rotation=45)
    
    # Todos los picos (rojo claro)
    plt.plot(data.index[picos_todos], data['close'].iloc[picos_todos], 'ro', alpha=0.3, label='minor fractal')

    # Top 15 picos (verde)
    plt.plot(fechas_picos, valores_picos, 'go', markersize=8, label='Top 15 fractal')

    # Top 15 valles (azul)
    plt.plot(fechas_valles, valores_valles, 'bo', markersize=8, label='Top 15 fractal')

    plt.title("Fractales - Top 15 Picos y Valles ")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(axis='y')
    plt.legend()
    plt.tight_layout()

    # Ruta de guardado
    output_folder = "output_charts"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "picos_valles.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {output_path}")  

    plt.show()

