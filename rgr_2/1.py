def fun(N, k):
    numb = ([0] * (N +1)) #створюємо масив з нулів
    numb[0] = 1 #базовий випадок 0
    numb[1] = 1 # можлива комбинация

    for i in range(2, N+1):
        numb[i] = numb[i - k] + numb[i-1]
    return numb[N]

N = int(input('N: '))
k = int(input('k: '))
print(fun(N, k))