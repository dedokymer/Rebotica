import random

# 1. Создаем список слов для игры
WORDS = [
    "кошка", "собака", "машина", "дерево", "книга",
    "ручка", "карандаш", "парта", "окно", "дверь",
    "стол", "стул", "парта", "тетрадь", "учебник"
]

points = {
    "comp": 0,
    "player": 0,
}

# 2. Удаляем функцию проверки четности чисел, так как она больше не нужна правда не очень
# def generate_even_number(number:int):
#     if number%2== 0:
#         return False
#     else:
#         return True

while True:
    # 3. Изменяем генерацию случайных значений на выбор слов из списка
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)

    # 4. Меняем логику игры на сложение строк
    user = input(f"{word1}+{word2} = ")

    # 5. Изменяем проверку ответа на сравнение строк
    if user == word1 + word2:
        print("Верно.")
        points["player"] += 1
    else:
        print("Ты ошибся, попробуй еще раз.")
        points["comp"] += 1

    print(f"Счет: {points['player']}:{points['comp']}")
