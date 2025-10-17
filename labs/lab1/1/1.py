import numpy as np

# Матрица выигрышей (стратегии игрока 1 по строкам, игрока 2 по столбцам)
M = np.array([
    [1, 12, 11, 4, 12],
    [3, 1, 2, 7, 0],
    [12, 6, 10, 7, 10],
    [12, 10, 2, 0, 6],
    [9, 0, 10, 0, 3]
])

# Смешанные стратегии
a = [0.11, 0.0, 0.89, 0.0, 0.0]  # игрок А
b = [0.0, 0.33, 0.0, 0.67, 0.0]  # игрок B

# Поиск седловой точки (минимум в строке и максимум в столбце)
p = None
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i, j] == min(M[i, :]) and M[i, j] == max(M[:, j]):
            p = (i, j, M[i, j])
            break
    if p:
        break

if p:
    print(f"Седловая точка в позиции (строка, столбец): ({p[0]+1}, {p[1]+1}), значение: {p[2]}")
else:
    print("Седловой точки нет, считаем смешанные стратегии.")

if not p:
    # Вычисляем ожидаемый выигрыш при смешанных стратегиях
    exp = sum(
        prob_a * sum(val * prob_b for val, prob_b in zip(row, b))
        for prob_a, row in zip(a, M)
    )

    # Вычисляем средний выигрыш для каждого чистого выбора игрока B
    pure_pay = {
        f"H(P,B{k+1})": sum(prob_a * val for prob_a, val in zip(a, col))
        for k, col in enumerate(np.rot90(M))
    }

    print(f"Ответ выигрыш игрока А в ситуации H(P,Q) = {round(exp, 3)}")
    for key, val in pure_pay.items():
        print(f"Ответ выигрыш игрока А в ситуации {key} = {round(val, 3)}")
