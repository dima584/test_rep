n = int(input())

def rec(n):
    print(n %10, end=' ')
    if n >= 10:
        rec(n // 10)

reult = rec(n)
print(reult)