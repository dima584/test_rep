
def func(x):
    return x**4 - 108*x + 7

def dif_func(x):
    return 4*x**3 - 108

def dif2_func(x):
    return 12*x**2


def newton_method(a, b, e):    
    if func(a) * dif2_func(a) > 0:
        x_n = a
    else:
        x_n = b

    print(f"\nУточнення кореня методом Ньютона")

    x_prev = x_n
    i = 0
    
    while True:
        derivative = dif_func(x_prev)
        if derivative == 0:
            print("Помилка: Похідна дорівнює нулю. Метод Ньютона не застосовується.")
            return None
        
        x_next = x_prev - func(x_prev) / derivative
        q = abs(x_next - x_prev)
        i += 1
        
        if q < e: 
            break
            
        x_prev = x_next
    
    print(f"Знайдений корінь: x = {x_next:.3f}")
    print(f"Кількість ітерацій: {i}")
    return x_next

def bisection_method(a, b, e):
    
    print(f"\nУточнення кореня методом Бісекції")
    
    if func(a) * func(b) > 0:
        print("Помилка: Функція не змінює знак на кінцях інтервалу.")
        return None
        
    i = 0
    while abs(b - a) > e: 
        c = (a + b) / 2
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c     
        i += 1
    
    root = (a + b) / 2
    print(f"Знайдений корінь: x = {root:.3f}")
    print(f"Кількість ітерацій: {i}")
    return root

def main():

    e = float(input('Введіть похибку e = '))

    print("\n[РОЗВ'ЯЗОК КОРЕНЯ x1 В ІНТЕРВАЛІ")
    a1 = float(input('Введіть a1 = '))
    b1 = float(input('Введіть b1 = '))
    x1_root = newton_method(a=a1, b=b1, e=e)
    
    print("\n[РОЗВ'ЯЗОК КОРЕНЯ x2 В ІНТЕРВАЛІ")
    a2 = float(input('Введіть a2 = '))
    b2 = float(input('Введіть b2 = '))
    x2_root = bisection_method(a=a2, b=b2, e=e)

if __name__ == "__main__":
    main()