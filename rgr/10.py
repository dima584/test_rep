def palindrome(w):
    if len(w) <= 1:
        return True
    if w[0] != w[-1]:
        return False
    return palindrome(w[1:-1])

w = input()
if palindrome(w):
    print('yes')
else:
    print('no')