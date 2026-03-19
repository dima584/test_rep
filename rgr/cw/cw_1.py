def reduce_fraction(fraction):
    l_ist = []
    a = int(fraction[0])
    b = int(fraction[1])
    
    while b != 0:
        a, b = b, a % b
    m = a
    
    a_n = a // m
    b_n = b // m
    
    
    l_ist.append(a_n)
    l_ist.append(b_n)
    print(l_ist)
    return l_ist

reduce_fraction([20, 60])