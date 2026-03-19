def unbounded_knapsack(N, W, weights, values):
    dp = [0] * (W + 1)  # створили масив з нулів
    for w in range(W + 1):  # перебираємо вагу від 0 до W
        for i in range(N):  # перебираємо предмети
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i]) 
    return dp[W]  # максимальна вартість 

def zero_one_knapsack(N, W, weights, values):
    dp = [[0] * (W + 1) for _ in range(N + 1)]  # таблиця розміром N+1 на W+1
    for i in range(1, N + 1):  # перебираємо предмети
        for w in range(W + 1):  # перебираємо вагу
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[N][W]


N = int(input("Введіть кількість предметів (N): "))
W = int(input("Введіть максимальну вагу рюкзака (W): "))

weights = []
values = []

for i in range(N):
    w = int(input(f"Введіть вагу предмета {i+1}: "))
    v = int(input(f"Введіть цінність предмета {i+1}: "))
    weights.append(w)
    values.append(v)

print("Максимальна цінність (а):", unbounded_knapsack(N, W, weights, values))
print("Максимальна цінність (б):", zero_one_knapsack(N, W, weights, values))