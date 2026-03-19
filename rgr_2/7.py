def counts(n):
    if n > 1000000 or n < 1:
        print('Erorrrrr')
    else:
        if n == 1:
            return 2
        if n == 2:
            return 4 
        if n == 3:
            return 7 

        a, b, c = 2, 4, 7 
        for _ in range(4, n + 1):
            a, b, c = b, c, a + b + c # змінюємо с як суму
        return c

n = int(input())
print(counts(n))