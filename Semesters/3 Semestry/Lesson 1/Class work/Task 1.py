# Практика: Решение задания 1
# Напиши программу, которая будет открывать калькулятор и нажимать на нём следующие кнопки
# подряд: "5", "+", "5", "=". Для открытия приложения и управления мышкой используй модуль PyAutoGUI.

import pyautogui as p
import time
p.hotkey("win", "r")
p.write("calc", 0.2)
p.press("enter")
time.sleep(1)
p.moveTo(166, 434)
p.click()
p.moveTo(314, 482)
p.click()
p.moveTo(166, 434)
p.click()
p.moveTo(315, 531)
p.click()

#############
while True:
    time.sleep(5)
    print(p.position())
    