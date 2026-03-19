def rec(n):
    if n < 10:
        print(n, end=' ')
    else:
        rec(n // 10)
        print(n % 10, end=' ')

n = int(input())
rec(n)