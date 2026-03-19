import math

def f_simpson(x):
    return (math.tan(x*x + 0.5))/(1 + 2*x*x)

def f_trap(x):
    return 1 / math.sqrt(2 * x * x + 0.3)

def simp_method(a, b, n):
    if n % 2 != 0:
        print("Кількість інтервалів (n) для методу Сімпсона має бути парною!")
        return None
    
    h = (b - a) / n
    s1 = 0.0 
    s2 = 0.0 
    

    x = a + h
    for i in range(1, n, 2):
        s1 += f_simpson(x)
        x += 2 * h
        
    x = a + 2 * h
    for i in range(2, n, 2):
        s2 += f_simpson(x)
        x += 2 * h

    s = f_simpson(a) + f_simpson(b) + 4 * s1 + 2 * s2
    return s * h / 3

def trapezoidal_method(a, b, n):

    h = (b - a) / n
    sum_val = 0.0
    
    x = a
    for i in range(1, n):
        x += h
        sum_val += f_trap(x)
        
    s = (f_trap(a) / 2 + f_trap(b) / 2 + sum_val)
    return s * h



def validate_input(a, b, n):

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        print("Границі інтегрування (a та b) повинні бути числами.")
        return False
    
    if not isinstance(n, int) or n <= 0:
        print("Кількість інтервалів (n) повинна бути додатним цілим числом.")
        return False
    
    if a >= b:
        print("Нижня границя (a) повинна бути менше верхньої границі (b).")
        return False
        
    return True


def main():

    while True:
        try:
            print("\nМетод Сімпсона: ")
            a_s = float(input(" a = "))
            b_s = float(input(" b = "))
            n_s = int(input(" Введіть парну кількість інтервалів n = "))
            
            if validate_input(a_s, b_s, n_s):
                result_s = simp_method(a_s, b_s, n_s)
                if result_s is not None:
                    print(" З методом Сімпсона S = ", result_s)
                break
        except ValueError:
            print("Будь ласка, введіть числові значення.")
    
    while True:
        try:
            print("\nМетод трапецій: ")
            a_t = float(input(" a = "))
            b_t = float(input(" b = "))
            n_t = int(input(" Введіть кількість інтервалів n = "))
            
            if validate_input(a_t, b_t, n_t):
                result_t = trapezoidal_method(a_t, b_t, n_t)
                print(" З методом трапецій S = ", result_t)
                break
        except ValueError:
            print("Будь ласка, введіть числові значення.")

if __name__ == "__main__":
    main()