def coin_with_path(d, k):
    N = len(d) #кількість стовпчиків, які має пройти коник
    dp = [-float('inf')] * N # зберігаю максимальну кількість монет до кожного стовпчика
    prev = [-1] * N #индекс
    dp[0] = d[0]
    prev[0] = None # бо це старт

    for i in range(1, N):
        # Перевіряю всі можливі стрибки назад на відстань від 1 до k
        for j in range(1, k + 1):
            if i - j >= 0:
                if dp[i - j] + d[i] > dp[i]:
                    dp[i] = dp[i - j] + d[i]
                    prev[i] = i - j  # записую, звідки я сюди прийшов

    # починаю з останнього стовпчика
    path = []
    pos = N - 1
    while pos is not None:
        path.append(pos)
        pos = prev[pos] # рухаюсь назад

    path.reverse()  # розвертаюся

    return dp[N - 1], path

d = list(map(int, input("Введи значення d через пробіл: ").split()))

k = int(input("Введи максимальну довжину стрибка k: "))

max_coins, path = coin_with_path(d, k)

print("Максимум монет:", max_coins)
print("Шлях коника:", path)