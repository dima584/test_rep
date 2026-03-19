def func(x):
    return x**4 - 108*x + 7

def dif_func(x):
    return 4*x**3 - 108

def dif2_func(x):
    return 12*x**2


def newton_method(a, b, e, max_iter=1000):

    starts = [a, b, (a + b) / 2]
    for start in starts:
        x_prev = start
        for i in range(max_iter):
            f_val = func(x_prev)
            derivative = dif_func(x_prev)
            if derivative == 0:
                break
            x_next = x_prev - f_val / derivative
            if abs(x_next - x_prev) < e:
                if a <= x_next <= b:
                    return round(x_next, 6)
                else:
                    break
            x_prev = x_next
    return None


def find_all_roots(x_min, x_max, step, e):

    roots = []
    x = x_min

    while x < x_max:
        x1 = x
        x2 = x + step
        if func(x1) * func(x2) < 0:  # зміна знаку ===== є корінь
            root = newton_method(x1, x2, e)
            if root is not None:
                # перевіряємо, щоб не було повторів близьких коренів
                if not any(abs(root - r) < e*5 for r in roots):
                    roots.append(root)
        x += step
    return roots


def main():
    print("Пошук усіх дійсних коренів рівняння f(x) = x⁴ - 108x + 7")
    x_min = float(input("Введіть початок проміжку x_min = "))
    x_max = float(input("Введіть кінець проміжку x_max = "))
    step = float(input("Введіть крок пошуку (рекомендовано 0.5 або менше): "))
    e = float(input("Введіть похибку e = "))

    roots = find_all_roots(x_min, x_max, step, e)

    print("\n=== РЕЗУЛЬТАТ ===")
    if roots:
        for i, r in enumerate(sorted(roots), 1):
            print(f"Корінь {i}: x = {r:.6f}, f(x) = {func(r):.3e}")
    else:
        print("На заданому проміжку коренів не знайдено.")


if __name__ == "__main__":
    main()
