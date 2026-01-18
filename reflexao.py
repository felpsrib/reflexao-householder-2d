import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. CONFIGURAÇÃO DE ESTILO "DARK MODE" ---
fig, ax = plt.subplots(figsize=(7, 7), facecolor='black')
ax.set_facecolor('black')

# Configuração dos Eixos
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
for spine in ax.spines.values():
    spine.set_edgecolor('white')

# Grid
ax.grid(True, linestyle=':', color='gray', alpha=0.4)
ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
ax.axvline(0, color='white', linewidth=0.8, alpha=0.5)

# Limites
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

# --- 2. DADOS DO OBJETO ---
original_coords = np.array([
    [2, 4, 2, 2],
    [0, 0, 1, 0]
])

# --- 3. ELEMENTOS VISUAIS ---
# Original (Ciano)
ax.plot(original_coords[0, :], original_coords[1, :], color='cyan', linewidth=2, label='Original')
ax.fill(original_coords[0, :], original_coords[1, :], color='cyan', alpha=0.2)

# Espelho (Amarelo)
linha_espelho, = ax.plot([], [], color='yellow', linestyle='-.', linewidth=2, label='Espelho')

# Refletido (Magenta)
linha_refletida, = ax.plot([], [], color='magenta', linestyle='--', linewidth=2, label='Refletido')

# Título e Legenda
titulo = ax.set_title("Iniciando...", color='white', fontsize=14, pad=20)
legenda = ax.legend(loc='upper left', facecolor='black', edgecolor='white')
plt.setp(legenda.get_texts(), color='white')

# --- 4. LÓGICA DA ANIMAÇÃO (FUNÇÕES) ---
def init():
    linha_espelho.set_data([], [])
    linha_refletida.set_data([], [])
    return linha_espelho, linha_refletida, titulo

def update(frame_angulo):
    theta_rad = np.radians(frame_angulo)

    # Householder
    v_angle = theta_rad + np.pi/2
    v = np.array([np.cos(v_angle), np.sin(v_angle)]).reshape(2, 1)
    I = np.eye(2)
    H = I - 2 * (v @ v.T)

    # Novos pontos
    coords_refletidas = H @ original_coords

    # Atualiza gráficos
    # Evita erro de divisão por zero na tangente desenhando uma linha longa
    x_espelho = np.array([-6, 6]) 
    y_espelho = x_espelho * np.tan(theta_rad)

    linha_espelho.set_data(x_espelho, y_espelho)
    linha_refletida.set_data(coords_refletidas[0, :], coords_refletidas[1, :])

    titulo.set_text(f"Reflexão de Householder | Ângulo: {frame_angulo:.1f}°")

    return linha_espelho, linha_refletida, titulo

# --- 5. RODAR ANIMAÇÃO ---
anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 2),
                     init_func=init, blit=False, interval=50)

plt.show()