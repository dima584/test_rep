import math
import matplotlib.pyplot as plt

def f1(x, y):
    """Варіант 10.а: y' = x + cos(y / sqrt(11))"""
    return x + math.cos(y / math.sqrt(11))

def f2(x, y):
    """Варіант 10.б: y' = x + sin(y / e)"""
    return x + math.sin(y / math.e)


def solve_euler(ode_function, a, b, h, y0):
    n = round((b - a) / h)
    X = [0] * (n + 1)
    Y = [0] * (n + 1)
    
    X[0] = a
    Y[0] = y0

    for i in range(n):
        # Проста формула Ейлера
        X[i+1] = X[i] + h
        Y[i+1] = Y[i] + h * ode_function(X[i], Y[i])
        
    return X, Y


def solve_euler_cauchy(ode_function, a, b, h, y0):
    n = round((b - a) / h)
    X = [0] * (n + 1)
    Y = [0] * (n + 1)
    
    X[0] = a
    Y[0] = y0

    for i in range(n):
        x_curr = X[i]
        y_curr = Y[i]

        k1 = ode_function(x_curr, y_curr)
        y_pred = y_curr + h * k1
        
        # Наступний x
        x_next = x_curr + h
        X[i+1] = x_next
        
        k2 = ode_function(x_next, y_pred)
        Y[i+1] = y_curr + (h / 2) * (k1 + k2)
        
    return X, Y


def run_analysis(ode_function, a, b, h, y0, title, method_type):
    
    if method_type == 1:
        method_name = "Метод Ейлера"
        X, Y = solve_euler(ode_function, a, b, h, y0)
    elif method_type == 2:
        method_name = "Метод Ейлера-Коші"
        X, Y = solve_euler_cauchy(ode_function, a, b, h, y0)
    else:
        return

    print(f"\n--- Таблиця значень ({method_name}) ---")
    print(f"Рівняння: {title}")
    print(f"{'i':<3} | {'x_i':<8} | {'y_i':<10}")
    print("-" * 25)
    
    n = len(X) - 1
    for i in range(n + 1):
        print(f"{i:<3} | {X[i]:<8.4f} | {Y[i]:<10.4f}")
    
    print(f"\nРозв'язок в кінцевій точці y({b}) ≈ {Y[n]:.4f}")

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(X, Y, 'bo-', label=f'Ламана ({method_name})') 
    
    plt.title(f'Графік розв\'язку ЗДР:\n{title}\n({method_name})', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    print("Чисельне розв'язання ЗДР")
    
    # Вибір рівняння
    print("\nОберіть рівняння:")
    print("  1) y' = x + cos(y / sqrt(11)) [Варіант 10.а]")
    print("  2) y' = x + sin(y / e)        [Варіант 10.б]")
    
    try:
        eq_choice = int(input("Ваш вибір (1 або 2): "))
    except ValueError:
        exit("Помилка введення.")

    print("\nОберіть метод:")
    print("  1) Метод Ейлера")
    print("  2) Метод Ейлера-Коші")
    
    try:
        method_choice = int(input("Ваш вибір (1 або 2): "))
    except ValueError:
        exit("Помилка введення.")

    if eq_choice == 1:
        func = f1
        title = "y' = x + cos(y / sqrt(11))"
        a, b, y0, h = 2.1, 3.1, 2.5, 0.1
    elif eq_choice == 2:
        func = f2
        title = "y' = x + sin(y / e)"
        a, b, y0, h = 1.4, 2.4, 2.5, 0.1
    else:
        exit("Невірний вибір рівняння.")

    if method_choice not in [1, 2]:
        exit("Невірний вибір методу.")

    print(f"\n--- Параметри ---")
    print(f"Проміжок: [{a}; {b}], Крок h={h}, y({a})={y0}")

    run_analysis(func, a, b, h, y0, title, method_choice)