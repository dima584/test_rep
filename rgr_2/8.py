list_s = list(map(int, input("Введи список чисел через пробіл: ").split()))

a_0 = 0
a_n = 0
count = 0

for i in range(len(list_s) - 1):
    a_0 = max(a_0, i + list_s[i])
    if i == a_n:
        count += 1
        a_n = a_0

print(count)


        
