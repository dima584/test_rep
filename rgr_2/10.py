money = list(map(int, input("Введи рівні покриття через пробіл: ").split()))
count_wat = 0


for i in range(1, len(money) - 1):

    if int(min(max(money[:i]), max(money[i+1:]))) - int(money[i]) > 0:
        print("Кількість води: ", int(min(max(money[:i]), max(money[i:]))) - int(money[i]))
        count_wat += int(min(max(money[:i]), max(money[i:]))) - int(money[i])

    elif int(min(max(money[:i+1]), max(money[i+1:]))) - int(money[i]) <= 0:
        print('Води немає!')

print("Сумарний об'єм: ", count_wat)

