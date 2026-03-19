#читання тексту інпут
def read_input_file(filename="C:/Users/nezol/Downloads/input_10000.txt"):
    with open(filename, "r", encoding="utf-8-sig") as infile:
        content = infile.read()
    return [int(item) for item in content.strip().split() if item]

#беремо останній елемент
def part_last(lis, low, high, comparisons):
    pivot = lis[high] #last in list
    i = low - 1
    for j in range(low, high):
        comparisons[0] += 1 # считаем сравнения
        if lis[j] <= pivot:
            i += 1
            lis[i], lis[j] = lis[j], lis[i]
    lis[i + 1], lis[high] = lis[high], lis[i + 1]
    return i + 1

#беремо 0 елемент
def part_first(lis, low, high, comparisons):
    lis[low], lis[high] = lis[high], lis[low]
    pivot = lis[high]
    i = low - 1
    for j in range(low, high):
        comparisons[0] += 1
        if lis[j] <= pivot:
            i += 1
            lis[i], lis[j] = lis[j], lis[i]
    lis[i + 1], lis[high] = lis[high], lis[i + 1]
    return i + 1

#беремо mid
def part_median(lis, low, high, comparisons):
    mid = (low + high) // 2
    trio = [(lis[low], low), (lis[mid], mid), (lis[high], high)] #(val, index)
    trio.sort()

    median_index = trio[1][1]# Берем индекс медианного элемента
    lis[high], lis[median_index] = lis[median_index], lis[high]
    pivot = lis[high]

    i = low - 1
    for j in range(low, high):
        comparisons[0] += 1
        if lis[j] <= pivot:
            i += 1
            lis[i], lis[j] = lis[j], lis[i]

    lis[i + 1], lis[high] = lis[high], lis[i + 1]
    return i + 1

#sort
def quick_sort(lis, low, high, partition_func, comparisons):
    if low < high: # если больше 1 елем
        pi = partition_func(lis, low, high, comparisons) # индекс пивот после разделения
        quick_sort(lis, low, pi - 1, partition_func, comparisons) # сорт слева от оп
        quick_sort(lis, pi + 1, high, partition_func, comparisons) # сорт справа от оп


original_list = read_input_file()

print("Сортування з останнім елементом")
list_last = original_list[:]
comparisons_last = [0]
quick_sort(list_last, 0, len(list_last) - 1, part_last, comparisons_last)
print("Відсортований список:", list_last)
print("Кількість порівнянь:", comparisons_last[0])
print("\nСортування з першим елементом")
list_first = original_list[:]
comparisons_first = [0]
quick_sort(list_first, 0, len(list_first) - 1, part_first, comparisons_first)
print("Відсортований список:", list_first)
print("Кількість порівнянь:", comparisons_first[0])
print("\nСортування з медіаною")
list_median = original_list[:]
comparisons_median = [0]
quick_sort(list_median, 0, len(list_median) - 1, part_median, comparisons_median)
print("Відсортований список:", list_median)
print("Кількість порівнянь:", comparisons_median[0])

with open("C:/Users/nezol/Downloads/sorted_output.txt", "w", encoding="utf-8") as outfile:
    outfile.write("Сортування з останнім елементом")
    for num in list_last:
        outfile.write(f"{num}\n")
    outfile.write("Сортування з першим елементом")
    for num in list_first:
        outfile.write(f"{num}\n")
    outfile.write("Сортування з медіаною")
    for num in list_median:
        outfile.write(f"{num}\n")
