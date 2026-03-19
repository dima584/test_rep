def coin(N, k):
    d = len(N) #кількість стовпчиків
    dp = [-float('inf')] * d  # -∞ як початкове значення
    dp[0] = N[0]  # стартова позиція

    for i in range(1, d): #стовпчики
        for j in range(1, k+1): #стрибки
            if i - j >= 0:
                dp[i] = max(dp[i], dp[i - j] + N[i]) # макс кількість монет
    
    return dp[d - 1]

N = list(map(int, input("Введіть значення d через пробіл: ").split()))
k = int(input("Введіть максимальну довжину стрибка k: "))
print("Максимум монет:", coin(N, k))