# Практика: Решение задания 2
# Напиши программу, которая открывает файл, сериализует его в строку и выводит длину этой строки
# в консоль. Для открытия файла используй функцию open(), для сериализации используй модуль pickle.

import pickle

class Cat:
    def __init__(self):
        self.health = 9
        self.food = 10
        self.sleep = 5
    def sleep(self):
        self.sleep += 10
    def eat(self):
        self.food += 5

champ = Cat()
cat_in_the_bag = pickle.dumps(champ)

print(cat_in_the_bag)
print(len(cat_in_the_bag))


