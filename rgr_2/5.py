import random

# розмір поля
M = int(input('Довжина: '))
N = int(input("Ширина: "))

# матриця
cost = [[random.randint(1, 10) for _ in range(N)] for _ in range(M)]

dp = [[0]*N for _ in range(M)] # таблиця
dp[0][0] = cost[0][0] # позиція короля 

for j in range(1, N):
    dp[0][j] = dp[0][j-1] + cost[0][j] #перша строка

for i in range(1, M):
    dp[i][0] = dp[i-1][0] + cost[i][0] #перший стовбець

for i in range(1, M):
    for j in range(1, N):
        dp[i][j] = cost[i][j] + min(
            dp[i-1][j],    # сверху
            dp[i][j-1],    # слева
            dp[i-1][j-1]   # по диагонали
        )

print(cost)
print("\nМінімальна вартість шляху:", dp[M-1][N-1])


