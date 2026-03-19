with open("C:/Users/nezol/Videos/in.txt", "r", encoding="utf-8-sig") as infile:
    content = infile.read()
lines = [int(item) for item in content.strip().split() if item]

count_ver = lines[0]
count_con = lines[1]

del lines[0]
del lines[0]
ch_s = 3

lines_t = [lines[i:i+ch_s]for i in range(0, len(lines), ch_s)]

u = []
w = []
v = []

for l in range(len(lines_t)):
    u.append(lines_t[l][0])
    w.append(lines_t[l][1])
    v.append(lines_t[l][2])

# будуємо граф
graph = {i: [] for i in range(1, count_ver + 1)}  # Ініціалізуємо всі вершини
for i in range(count_con):
    from_node = u[i]
    to_node = v[i]
    weight = w[i]
    graph[from_node].append((to_node, weight))

start = int(input("Введіть початкову вершину: "))
end = int(input("Введіть кінцеву вершину: "))

all_nodes = list(range(1, count_ver + 1))  # Усі можливі вершини
dist = {node: float('inf') for node in all_nodes}  # відстань від початку до кожного вузла
dist[start] = 0
visited = set()

while len(visited) < len(all_nodes):
    min_node = None
    min_dist = float('inf')
    for node in all_nodes:
        if node not in visited and dist[node] < min_dist:
            min_dist = dist[node]
            min_node = node

    if min_node is None:
        break  # всі досяжні вершини відвідані

    visited.add(min_node)

    if min_node in graph:  # Перевіряємо, чи є сусіди у поточної вершини
        for neighbor, weight in graph[min_node]:
            potential_new_distance = dist[min_node] + weight
            if potential_new_distance < dist[neighbor]:
                dist[neighbor] = potential_new_distance

if end not in dist or dist[end] == float('inf'):
    print(f"Шлях від {start} до {end} відсутній.")
else:
    print(f"Мінімальна відстань від {start} до {end}: {dist[end]}")