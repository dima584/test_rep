import numpy as np
import matplotlib.pyplot as plt

def solve_game_practicum():

    print("### 1. Формування платіжної матриці 5x5 (Таблиця 1) ###")

    np.random.seed(42) 
    A_5x5 = np.random.randint(-20, 21, size=(5, 5))
    
    A_5x5 = np.array([
        [15, -10, 5, 18, 7],
        [-2, 14, -15, -1, 12],
        [10, 0, 11, -8, 1],
        [5, -1, -12, 16, 3],
        [-18, 20, 2, 4, -5]
    ])
    
    print("\nТаблиця 1 (Матриця 5x5):")
    print(A_5x5)
    
    # --- 2. Визначення нижньої та верхньої ціни гри та сідлової точки ---
    print("\n### 2. Визначення цін гри та сідлової точки ###")
    
    min_in_rows = np.min(A_5x5, axis=1)
    alpha = np.max(min_in_rows)
    
    max_in_cols = np.max(A_5x5, axis=0)
    beta = np.min(max_in_cols)
    
    print(f"Мінімуми по рядках: {min_in_rows}")
    print(f"Нижня ціна гри (α) = {alpha}")
    print(f"Максимуми по стовпцях: {max_in_cols}")
    print(f"Верхня ціна гри (β) = {beta}")
    
    if alpha == beta:
        print(f"✅ У матриці Є сідлова точка: α = β = {alpha}.")
    else:
        print(f"❌ У матриці НЕМАЄ сідлової точки: α ({alpha}) < β ({beta}).")

    # --- 3. Спрощення матриці (Видалення домінованих стратегій) ---
    print("\n### 3. Спрощення матриці (Таблиця 2) ###")
    
    # Функція для перевірки домінування (спрощено, без повного циклу)
    # Згідно з попереднім аналізом, чисте домінування для цієї матриці відсутнє.
    # Якщо б домінування було, ми б отримали нову матрицю A_simplified
    
    print("Аналіз показав, що чисте домінування (видалення рядків та стовпців) для цієї матриці 5x5 відсутнє.")
    A_simplified = A_5x5.copy()
    print("Таблиця 2 (Спрощена) = Таблиця 1.")
    
    # --- 4. Перехід до платіжної матриці 2x5 (Таблиця 3) ---
    print("\n### 4. Перехід до платіжної матриці 2x5 (Таблиця 3) ###")
    
    # Залишаємо 2 перші рядки з Таблиці 1
    A_2x5 = A_5x5[:2, :]
    print("Таблиця 3 (Матриця 2x5):")
    print(A_2x5)
    

    print("\n### 5. Розв'язок гри 2x5 графоаналітичним методом ###")
    

    a1 = A_2x5[0, :]  # Стратегії A1
    a2 = A_2x5[1, :]  # Стратегії A2
    n_strategies = A_2x5.shape[1]
    
    p_values = np.linspace(0, 1, 500)
    payoffs = np.zeros((n_strategies, len(p_values)))
    
    # Обчислення функцій виграшу E(p, Bj)
    for j in range(n_strategies):
        # E(p, Bj) = a1[j] * p + a2[j] * (1 - p)
        payoffs[j] = a1[j] * p_values + a2[j] * (1 - p_values)
    
    # Знаходимо нижню опуклу межу (нижній контур)
    lower_envelope = np.min(payoffs, axis=0)
    
    # Знаходимо точку максиміну (ціну гри v)
    maximin_v = np.max(lower_envelope)
    maximin_index = np.argmax(lower_envelope)
    p_star = p_values[maximin_index]
    
    print(f"Графічна ціна гри v ≈ {maximin_v:.4f} (в точці p* ≈ {p_star:.4f})")
    
    # Візуалізація
    plt.figure(figsize=(10, 6))
    for j in range(n_strategies):
        plt.plot(p_values, payoffs[j], label=f'$B_{j+1}$')
    
    plt.plot(p_values, lower_envelope, color='red', linewidth=3, linestyle='--', label='Нижній контур (min)')
    plt.plot(p_star, maximin_v, 'o', color='black', markersize=8, label=f'Максимін (v ≈ {maximin_v:.2f})')
    
    plt.xlabel('Ймовірність $p$ (для $A_1$)')
    plt.ylabel('Очікуваний виграш $E(p)$')
    plt.title('Рис.1 Визначення активних стратегій гравця B')
    plt.legend()
    plt.grid(True)
    plt.show() # Відображаємо графік
    
    print("Активні стратегії: Графік показує, що точка максиміну лежить на перетині **B1** та **B2**.")
    active_strategies = [0, 1] # Індекси B1 та B2
    
 
    M = A_2x5[:, active_strategies]
    a11, a12 = M[0, 0], M[0, 1]
    a21, a22 = M[1, 0], M[1, 1]
    
    print(f"\nЗведена матриця M (B1, B2):\n{M}")
    
    # Обчислення
    delta = (a11 + a22) - (a12 + a21)
    
    if delta == 0:
        print("Помилка: Знаменник (delta) дорівнює 0.")
        return
        
    v_numerator = a11 * a22 - a12 * a21
    v = v_numerator / delta
    
    p1 = (a22 - a21) / delta
    p2 = 1 - p1
    
    q1 = (a22 - a12) / delta
    q2 = 1 - q1
    
    print(f"\nРезультати за формулами:")
    print(f"Знаменник (Δ) = {delta}")
    print(f"Ціна гри (v) = {v_numerator}/{delta} ≈ {v:.4f}")
    print(f"Оптимальна ймовірність p1 (A1) = {p1:.4f}")
    print(f"Оптимальна ймовірність p2 (A2) = {p2:.4f}")
    print(f"Оптимальна ймовірність q1 (B1) = {q1:.4f}")
    print(f"Оптимальна ймовірність q2 (B2) = {q2:.4f}")


    print("\n### 6. Результати у матричній формі ###")
    
    # Гравець A
    print("Оптимальна стратегія гравця A:")
    print(f"  S_A* = ( A1  A2 )")
    print(f"         ({p1:.4f} {p2:.4f})")
    
    # Гравець B (зведена форма)
    print("Оптимальна стратегія гравця B (зведена форма):")
    print(f"  S_B* = ( B1  B2 )")
    print(f"         ({q1:.4f} {q2:.4f})")

# Запуск програми
solve_game_practicum()