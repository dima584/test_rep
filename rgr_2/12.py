figure_1_x = list(map(int, input("Координати кутів (x) першої фігури: ").split()))
figure_1_y = list(map(int, input("Координати кутів (y) першої фігури: ").split()))

figure_2_x = list(map(int, input("Координати кутів (x) другої фігури: ").split()))
figure_2_y = list(map(int, input("Координати кутів (y) другої фігури: ").split()))

width_1 = abs(figure_1_x[1] - figure_1_x[0])
height_1 = abs(figure_1_y[1] - figure_1_y[0])
S_1 = width_1 * height_1 # Площа першої фігури

width_2 = abs(figure_2_x[1] - figure_2_x[0])
height_2 = abs(figure_2_y[1] - figure_2_y[0])
S_2 = width_2 * height_2 # Площа другої фігури


x_p = max(0, min(max(figure_1_x), max(figure_2_x)) - max(min(figure_1_x), min(figure_2_x)))

y_p = max(0, min(max(figure_1_y), max(figure_2_y)) - max(min(figure_1_y), min(figure_2_y)))

# Площа перекриття
S_p = x_p * y_p

# Загальна площа
S_t = S_1 + S_2 - S_p

print("Площа прямокутника 1:", S_1)
print("Площа прямокутника 2:", S_2)
print("Площа перекриття:", S_p)
print("Загальна покрита площа:", S_t)