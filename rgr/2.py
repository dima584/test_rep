def recursive(a, b):
    if a == b:
        print(a)
    elif a < b:
        print(a)
        recursive(a + 1, b)
    else:
        print(a)
        recursive(a - 1, b)

a = int(input())
b = int(input())

recursive(a, b)