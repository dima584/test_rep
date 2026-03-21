def facktorial(n):
    if n == 1:
        return 1
    else:
        n = n * facktorial(n-1)
        return n
    
print(facktorial(600))