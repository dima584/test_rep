def ackerman(n, m):
    if n == 0:
        return m + 1
    if m == 0:
        return ackerman(n - 1, 1)
    return ackerman(n - 1, ackerman(n, m - 1))

n = int(input())
m = int(input())

if n < 0 or m < 0:
    print('Error')

else:
    result = ackerman(n,m)
    print(result) 