def max__count(grid):
    if not grid: #  Якщо матриця порожня
        return 0, 0

    n = len(grid)
    visited = [[False] * n for _ in range(n)] # масив для перебору клітинок матриці

    def dfs(x, y):
        if x < 0 or x >= n or y < 0 or y >= n or grid[x][y] == 0 or visited[x][y]: #перевірка на межі матриці
            return 0
        visited[x][y] = True
        area = 1 #Початкова площа острова
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #обходимо сусідні клітини
            area += dfs(x + dx, y + dy)
        return area

    max_area = 0 # макс площа
    island_count = 0 # макс кількість

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]: #якщо є клітина не відвідувана то перезапускаємо вивід
                area = dfs(i, j)
                max_area = max(max_area, area)
                island_count += 1

    return max_area, island_count



sizes = [2, 3, 1, 1, 4] # розміри

grid = [
    [0,0,1,0,1,1],
    [0,1,1,0,0,0],
    [0,0,1,0,1,0],
    [1,1,0,1,1,0],
    [1,0,0,0,0,0],
    [0,0,0,0,0,0],
] 
#матрця

max_area, island_count = max__count(grid)
print("Макс площа острова:", max_area)
print("Кіл-ть островів:", island_count)