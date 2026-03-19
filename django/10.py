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
    w.append(lines_t[l][2])
    v.append(lines_t[l][1])

# будуємо
graph = {}
for i in range(count_con):
    from_node = u[i]
    to_node = v[i]
    weight = w[i]
    if from_node not in graph:
        graph[from_node] = [] # список сусідів вершини
    graph[from_node].append((to_node, weight)) # в цей же список запхнули кінець та вагу
    if to_node not in graph: # Переконуємось, що кожна вершина є ключем у graph
        graph[to_node] = []

start = int(input("Введіть початкову вершину: "))
end = int(input("Введіть кінцеву вершину: "))

all_nodes = list(set(u + v)) #список вершин
dist = {node: float('inf') for node in all_nodes} # відстань від початку до кожного вузла

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
        break  # все знайшли шо треба

    visited.add(min_node)

# перевірка на потенцальну нову мін відстань
    for neighbor, weight in graph[min_node]:
        potential_new_distance = dist[min_node] + weight
        if potential_new_distance < dist[neighbor]:
            dist[neighbor] = potential_new_distance


if end not in dist or dist[end] == float('inf'):
    print(f"Шлях від {start} до {end} відсутній.")
else:
    print(f"Мінімальна відстань від {start} до {end}: {dist[end]}")
