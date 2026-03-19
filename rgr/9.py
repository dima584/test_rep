def rec(n, div=2):
    if div * div > n:
        if n > 1:
            print(n, end=' ')
        return
    if n % div == 0:
        print(div, end=' ')
        rec(n // div, div)
    else:
        rec(n, div + 1)

n = int(input())
rec(n)