import random


# Изменение 1: Добавление функции для генерации задачи
def generate_task():
    a = random.randint(10, 90)
    b = random.randint(10, 90)
    op = random.choice(("+", "-"))
    return a, b, op


# Изменение 2: Добавление переменной для количества раундов
rounds = 5

# Изменение 3: Добавление счетчика раундов
current_round = 1

points = {
    "comp": 0,
    "player": 0,
}

while current_round <= rounds:
    # Изменение 4: Использование функции для генерации задачи
    a, b, op = generate_task()

    if op == "+":
        ans = a + b
        user = input(f"{a}+{b} = ")
    else:
        ans = a - b
        user = input(f"{a}-{b} = ")

    if user == str(ans):
        print("Верно.")
        points["player"] += 1
    else:
        print("Ты ошибся, попробуй еще раз.")
        points["comp"] += 1

    print(f"Счет: {points['player']}:{points['comp']}")

    # Изменение 5: Увеличение счетчика раундов
    current_round += 1