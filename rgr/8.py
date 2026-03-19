def rec(n, div=2):
    if n == div:
        return True
    if n % div == 0:
        return False
    if div * div > n:
        return True
    return rec(n, div + 1)

n = int(input())
if rec(n):
    print("YES")
else:
    print("NO")