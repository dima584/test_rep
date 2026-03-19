import numpy as np
import matplotlib.pyplot as plt

# --- НАЛАШТУВАННЯ ---
N = 100        
M0 = 2000      
X_MIN = 0.0    
X_MAX = 100.0  
DELTAS = [0.0, 0.05, 0.10, 0.15]
COLORS = ['blue', 'orange', 'green', 'red'] # Кольори як на зведеному графіку

# --- ФУНКЦІЇ ---
def generate_experiments(m0, n, x_min, x_max):
    return np.random.uniform(x_min, x_max, size=(m0, n))

def get_prob_array(Xm, N, Delta_val):
    probabilities = []
    # Розрахунок для кожного t від 1 до N-1
    for t in range(1, N):
        success_count = 0
        for m in range(Xm.shape[0]):
            x_global_best = np.max(Xm[m, :])
            
            if t == 1:
                x_obs_max = -np.inf
            else:
                x_obs_max = np.max(Xm[m, :t-1])
            
            future = Xm[m, t-1:]
            better = np.where(future > x_obs_max)[0]
            
            if len(better) > 0:
                choice = future[better[0]]
            else:
                choice = Xm[m, -1]
                
            if np.abs(x_global_best - choice) <= Delta_val:
                success_count += 1
        
        probabilities.append(success_count / Xm.shape[0])
    return np.array(probabilities)

# --- ГЕНЕРАЦІЯ ---
print("Генерація даних... Будь ласка, зачекайте.")
X_experiments = generate_experiments(M0, N, X_MIN, X_MAX)

plt.style.use('bmh') # Стиль графіків

# Генеруємо 4 окремих графіки
for i, dp in enumerate(DELTAS):
    abs_delta = dp * X_MAX
    P_t_array = get_prob_array(X_experiments, N, abs_delta)
    
    # Знаходимо максимум для підпису
    max_p = np.max(P_t_array)
    best_t = np.argmax(P_t_array) + 1
    
    # Створення нового вікна для кожного графіка
    plt.figure(figsize=(10, 6))
    
    # Побудова кривої
    plt.plot(range(1, N), P_t_array, label=f'$\Delta$={dp*100:.0f}%', color=COLORS[i], linewidth=2.5)
    
    # Позначення максимуму точкою
    plt.plot(best_t, max_p, 'o', color='black')
    plt.annotate(f'Max: t*={best_t}, P={max_p:.3f}', 
                 xy=(best_t, max_p), 
                 xytext=(10, 10), textcoords='offset points',
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Налаштування
    plt.title(f'Залежність ймовірності успіху $P(t)$ при $\Delta = {int(dp*100)}\%$', fontsize=14)
    plt.xlabel('Крок зупинки $t$', fontsize=12)
    plt.ylabel('Ймовірність $P(t)$', fontsize=12)
    plt.grid(True, alpha=0.7)
    plt.legend(fontsize=12)
    
    # Збереження (опціонально) або просто показ
    filename = f"Graph_Pt_Delta_{int(dp*100)}.png"
    # plt.savefig(filename, dpi=300) # Розкоментуйте, щоб зберегти у файл
    
    print(f"Відображаю графік для Delta = {int(dp*100)}%...")
    plt.show()

print("Готово!")