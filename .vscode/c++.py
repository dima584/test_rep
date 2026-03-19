import matplotlib.pyplot as plt
import numpy as np

# --- ДАНІ ---
X_DATA = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] 
Y_SERIES = [1.07177346, 1.14869834, 1.23114407, 1.31950791, 1.41421356, 1.51571656, 1.62450478, 1.74110113, 1.86606596, 2.00000000] 

BASE = 2.0

# --- ПОБУДОВА ГРАФІКА ---
plt.figure(figsize=(8, 5))
# Використовуємо '^' (трикутник) для точок
plt.plot(X_DATA, Y_SERIES, marker='^', linestyle='--', color='green', label='Значення з програми') 

plt.title(f'Графік функції $f(x) = {BASE}^x$, отриманими в програмі', fontsize=12)
plt.xlabel('Аргумент X')
plt.ylabel('f(x)')
plt.xticks(np.arange(0.1, 1.1, 0.1))
plt.grid(True)
plt.show()