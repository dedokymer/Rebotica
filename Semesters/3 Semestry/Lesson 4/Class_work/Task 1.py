#Пусть игра продолжается только с чётными числами. Напиши функцию, которая будет отсеивать нечётные числа из игры. Закоммить свои изменения и загрузи их в GitHub.


import random

points = {
    "comp": 0,
    "player": 0,
}
def generate_even_number(number:int):
    if number%2== 0:
        return False
    else:
        return True

while True:

    a = random.randint(10,90)
    if generate_even_number(a):
        continue
    b = random.randint(10, 90)
    if generate_even_number(b):
        continue
    op = random.choice(("+", "-"))
    if op == "+":
        ans = a+b
        user = input(f"{a}+{b} = ")
    else:
        ans = a-b
        user = input(f"{a}-{b} = ")
    if user == str(ans):
        print("Верно.")
        points["player"] += 1
    else:
        print("Ты ошибся, попробуй еще раз.")
        points["comp"] += 1
    print(f"Счет: {points["player"]}:{points["comp"]}")
