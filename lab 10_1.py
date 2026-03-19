str_1 = "banana"
str_2 = "abn"

str_2 = list(str_2)
str_1 = list(str_1)
result = []

count = 0
for letter in range(len(str_2)):
    for item in range(1, len(str_1) + 1):
        if str_2[letter] == str_1[item - 1]:
            result.append(str_2[letter])
for n in range(len(str_1)):
    if str_1[n] not in str_2:
        result.append(str_1[n])
result = ''.join(result)
print(result)

def sort_string(str_1, str_2):
    str_2 = list(str_2)
    str_1 = list(str_1)
    result = []

    count = 0
    for letter in range(len(str_2)):
        for item in range(1, len(str_1) + 1):
            if str_2[letter] == str_1[item - 1] and str_2[letter] not in result:
                result.append(str_2[letter])
    for n in range(len(str_1)):
        if str_1[n] not in str_2:
            result.append(str_1[n])
    result = ''.join(result)
    return result

print(sort_string("apple", "pap"))