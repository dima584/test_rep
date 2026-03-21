def func(x):
    while x != 0:
        x = x*x
        x-=1
        print(x)
        func(x-1)

func(5)