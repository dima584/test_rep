import numpy as np
import matplotlib.pyplot as plt


N = 100        # Кількість кандидатів
M0 = 2000      # Кількість експериментів (більше = точніші графіки)
X_MIN = 0.0    # Нижня межа
X_MAX = 100.0  # Верхня межа


def generate_experiments(m0, n, x_min, x_max):
    return np.random.uniform(x_min, x_max, size=(m0, n))


def evaluate_stop_prob(Xm, t, N, Delta_val):
    M0, n = Xm.shape
    success_count = 0

    for m in range(M0):
        # 1. Глобальний лідер (еталон)
        x_global_best = np.max(Xm[m, :]) 

        # 2. Спостереження [0, t-1]
        if t == 1:
            x_observation_max = -np.inf
        else:
            x_observation_max = np.max(Xm[m, :t-1])

        x_d_star = Xm[m, -1] # Якщо нікого не знайшли, беремо останнього
        
        future_candidates = Xm[m, t-1:]
        better_indices = np.where(future_candidates > x_observation_max)[0]
        
        if len(better_indices) > 0:
            x_d_star = future_candidates[better_indices[0]]
            
        if np.abs(x_global_best - x_d_star) <= Delta_val:
            success_count += 1

    return success_count / M0

def find_optimal_stopping_time(Xm, N, Delta_val):
    probabilities = []
    for t in range(1, N):
        P_t = evaluate_stop_prob(Xm, t, N, Delta_val)
        probabilities.append(P_t)
        
    probabilities = np.array(probabilities)
    P_max = np.max(probabilities)
    t_star = np.argmax(probabilities) + 1 
    
    return t_star, P_max, probabilities

print(f"Генерація {M0} експериментів...")
X_experiments = generate_experiments(M0, N, X_MIN, X_MAX)

delta_percents = [0.0, 0.05, 0.10, 0.15] 

results_Pmax = []
results_tstar = []
results_Delta_labels = []

plt.figure(figsize=(12, 12))
plt.suptitle('Результати моделювання методу оптимальної зупинки', fontsize=16)

plt.subplot(3, 1, 1)
for dp in delta_percents:
    absolute_delta = dp * X_MAX 
    t_star, P_max, P_t_array = find_optimal_stopping_time(X_experiments, N, absolute_delta)
    
    results_Pmax.append(P_max)
    results_tstar.append(t_star)
    results_Delta_labels.append(dp * 100)
    
    plt.plot(range(1, N), P_t_array, label=f'$\Delta$={dp*100:.0f}%', linewidth=2)

plt.title('Ймовірність успіху $P(t)$ від кроку $t$')
plt.xlabel('Крок зупинки $t$')
plt.ylabel('$P(t)$')
plt.legend()
plt.grid(True, alpha=0.5)

plt.subplot(3, 1, 2)
plt.plot(results_Delta_labels, results_Pmax, marker='o', color='green', linewidth=2)
plt.title('Максимальна ймовірність успіху $P_{max}$ від поступки $\Delta$')
plt.xlabel('Поступ $\Delta$ (%)')
plt.ylabel('$P_{max}$')
plt.xticks(results_Delta_labels)
plt.grid(True, alpha=0.5)

plt.subplot(3, 1, 3)
plt.plot(results_Delta_labels, results_tstar, marker='s', color='purple', linewidth=2)
plt.title('Оптимальний час зупинки $t^*$ від поступки $\Delta$')
plt.xlabel('Поступ $\Delta$ (%)')
plt.ylabel('Крок $t^*$')
plt.xticks(results_Delta_labels)
plt.grid(True, alpha=0.5)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()

# --- АНАЛІЗ ---
print("\n--- АНАЛІТИЧНИЙ ВИСНОВОК ---")
theory_t = N / np.e
theory_p = 1 / np.e
print(f"Теорія (1/e): t* ≈ {theory_t:.1f}, P ≈ {theory_p:.3f}")
print(f"Експеримент (Delta=0%): t* = {results_tstar[0]}, P = {results_Pmax[0]:.3f}")

if abs(results_tstar[0] - theory_t) < 5 and abs(results_Pmax[0] - theory_p) < 0.05:
    print(">> Висновок: Результати збігаються з теоретичними в межах похибки.")
else:
    print(">> Висновок: Спостерігається відхилення (спробуйте збільшити M0).")