n = int(input())

def rec(n):
    if n <= 0:
        return False
    if n == 1:
        return True
    if n % 2 != 0:
        return False
    return rec(n // 2)

if rec(n):
    print("YES")
else:
    print("NO")