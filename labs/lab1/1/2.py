from scipy.optimize import linprog
import numpy as np
import time

start = time.time()

# Данные из задачи
supplies = [10, 30, 60, 10]  # Запасы поставщиков
demands = [30, 30, 30, 40, 60]  # Потребности потребителей
costs = [
    [3, 1, 3, 4, 3],  # A1 -> B1,B2,B3,B4,B5
    [5, 1, 2, 2, 6],  # A2 -> B1,B2,B3,B4,B5
    [2, 3, 4, 1, 1],  # A3 -> B1,B2,B3,B4,B5
    [6, 2, 5, 3, 2]   # A4 -> B1,B2,B3,B4,B5
]

# Проверяем задачу на закрытость
total_supply = sum(supplies)
total_demand = sum(demands)

print(f"Сумма запасов: {total_supply}")
print(f"Сумма потребностей: {total_demand}")

# Добавляем фиктивного поставщика если нужно
if total_supply < total_demand:
    print("Задача открытая. Добавляем фиктивного поставщика A5 с запасом 80")
    supplies.append(80)
    costs.append([0, 0, 0, 0, 0])  # Нулевые тарифы для фиктивного поставщика

# Преобразуем данные для scipy.optimize.linprog
m, n = len(supplies), len(demands)

# Целевая функция (минимизация стоимости)
c = [costs[i][j] for i in range(m) for j in range(n)]

# Ограничения равенства (баланс поставщиков и потребителей)
A_eq = []
b_eq = []

# Ограничения для поставщиков (сумма по строкам = supplies)
for i in range(m):
    row = [0] * (m * n)
    for j in range(n):
        row[i * n + j] = 1
    A_eq.append(row)
    b_eq.append(supplies[i])

# Ограничения для потребителей (сумма по столбцам = demands)
for j in range(n):
    row = [0] * (m * n)
    for i in range(m):
        row[i * n + j] = 1
    A_eq.append(row)
    b_eq.append(demands[j])

# Границы переменных (неотрицательность)
bounds = [(0, None) for _ in range(m * n)]

# Решаем задачу
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

print("\n" + "="*50)
print("Результаты решения транспортной задачи:")
print("="*50)

if result.success:
    print("Решение найдено успешно!")
    print("Минимальная стоимость перевозок:", result.fun)
    
    # Восстанавливаем матрицу перевозок из вектора решения
    plan = np.array(result.x).reshape(m, n)
    
    print("\nОптимальный план перевозок:")
    print("    B1   B2   B3   B4   B5  Запасы")
    for i in range(m):
        print(f"A{i+1} ", end="")
        for j in range(n):
            value = plan[i][j]
            if value > 1e-6:  # Учитываем численную погрешность
                print(f"{value:5.1f} ", end="")
            else:
                print("     - ", end="")
        supplier_name = f"A{i+1}" if i < 4 else "A5(фикт)"
        print(f"  {supplies[i]:6}")
    
    print("Потр.", end="")
    for j in range(n):
        print(f"{demands[j]:5} ", end="")
    print()
    
    print("\nДетализация перевозок:")
    total_cost = 0
    for i in range(m):
        for j in range(n):
            value = plan[i][j]
            if value > 1e-6:
                cost = value * costs[i][j]
                total_cost += cost
                supplier_name = f"A{i+1}" if i < 4 else "A5(фикт)"
                print(f"{supplier_name} -> B{j+1}: {value:5.1f} ед. × {costs[i][j]} = {cost:5.1f}")
    
    print(f"\nОбщая стоимость: {total_cost}")
    
    # Анализ фиктивных перевозок (недопоставки)
    if total_supply < total_demand:
        print("\nАнализ недопоставок (фиктивный поставщик A5):")
        for j in range(n):
            value = plan[4][j]  # Фиктивный поставщик A5
            if value > 1e-6:
                print(f"B{j+1} недополучено: {value:5.1f} ед.")
else:
    print("Решение не найдено!")
    print("Статус:", result.message)

stop = time.time()
print(f"\nВремя выполнения: {stop - start:.4f} секунд")
