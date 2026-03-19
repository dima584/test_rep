import tkinter as tk
import random
import time

N = 5

def generate_matrix():
    matrix = []
    for i in range(N):
        row = []
        for j in range(N):
            number = random.randint(-9, 9)
            row.append(number)
        matrix.append(row)
    return matrix

def find_optimal_path(matrix):
    dp = []
    path = []
    for i in range(N):
        dp_row = []
        path_row = []
        for j in range(N):
            dp_row.append(float('-inf'))
            path_row.append(None)
        dp.append(dp_row)
        path.append(path_row)

    dp[N-1][0] = matrix[N-1][0]  # стартова точка

    for i in range(N-1, -1, -1):
        for j in range(N):
            # Рух вгору
            if i < N-1:
                if dp[i][j] < dp[i+1][j] + matrix[i][j]:
                    dp[i][j] = dp[i+1][j] + matrix[i][j]
                    path[i][j] = (i+1, j)
            # Рух вправо
            if j > 0:
                if dp[i][j] < dp[i][j-1] + matrix[i][j]:
                    dp[i][j] = dp[i][j-1] + matrix[i][j]
                    path[i][j] = (i, j-1)
            # Рух діагоналлю
            if i < N-1 and j > 0:
                if dp[i][j] < dp[i+1][j-1] + matrix[i][j]:
                    dp[i][j] = dp[i+1][j-1] + matrix[i][j]
                    path[i][j] = (i+1, j-1)

            for x in range(N):
                for y in range(N):
                    labels[x][y].config(text=str(dp[x][y]), bg="white", fg="black")
            root.update()
            time.sleep(0.1)

    route = []
    i, j = 0, N-1  
    while True:
        route.append((i, j))
        if path[i][j] is None:
            break
        i, j = path[i][j]


    for (i, j) in route:
        labels[i][j].config(bg="lightgreen")
    root.update()

    return dp, route, dp[0][N-1]

root = tk.Tk()
root.title("Динамічне оновлення dp-матриці")

labels = []
for i in range(N):
    row_labels = []
    for j in range(N):
        lbl = tk.Label(
            root,
            text="0",
            width=5,
            height=2,
            font=("Arial", 16),
            borderwidth=2,
            relief="groove",
            highlightthickness=1,
            bg="white"
        )
        lbl.grid(row=i, column=j, padx=2, pady=2)
        row_labels.append(lbl)
    labels.append(row_labels)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.grid(row=N+1, column=0, columnspan=N, pady=5)

def start_algorithm():

    matrix_global = generate_matrix()


    for i in range(N):
        for j in range(N):
            labels[i][j].config(text=str(matrix_global[i][j]), bg="white", fg="black")
    root.update()
    time.sleep(3)  # невелика пауза перед запуском алгоритму

    dp, route, max_sum = find_optimal_path(matrix_global)
    result_label.config(text=f"Максимальна сума: {max_sum}")

# Кнопка для запуску алгоритму
button = tk.Button(root, text="Запустити алгоритм", command=start_algorithm, font=("Arial", 12))
button.grid(row=N, column=0, columnspan=N, pady=10)

root.mainloop()