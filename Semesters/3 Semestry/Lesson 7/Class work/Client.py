import socket
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
name = ""
color = ""
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DarkTurquoise', 'DeepSkyBlue', 'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']
class Grid:
    def __init__(self, screen, color):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size
        self.color = color
    def draw(self):
        for i in range(WIDTH // self.size + 2):
            pygame.draw.line(self.screen, self.color, (self.x + i * self.size, 0 ), (self.x + i * self.size, HEIGHT), 1)
        for i in range(HEIGHT // self.size + 2):
            pygame.draw.line(self.screen, self.color, (0, self.y + i * self.size,), (WIDTH, self.y + i * self.size), 1)
    def update(self, parameters):
        x,y,L = parameters
        self.size = self.start_size // L
        self.x = -self.size + (-x) % self.size
        self.y = -self.size + (-y) % self.size

def scroll(event):
    global color
    color = color_box.get()
    style.configure("TCombobox", fieldbackground = color, background = "white")
def Vxod():
    global name
    name = row.get()
    if name and color and len(name) >= 4:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Введите имя и цвет")

def find(vector: str):
  global buffer
  first = None
  for num, sign in enumerate(vector):
      if sign == "<":
          first = num
      if sign == ">" and first is not None:
          second = num
          result = vector[first + 1:second]  # Поменяли
          return result
  buffer = int(buffer * 1.5)
  return ""
def draw_bacteries(data: list[str]):
  for num, bact in enumerate(data):
      data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
      x = CC[0] + int(data[0])
      y = CC[1] + int(data[1])
      size = int(data[2])
      color = data[3]
      pygame.draw.circle(screen, color, (x, y), size)
      if len(data) > 4:
          draw_text(x,y, size // 2, data[4], "black")
def draw_text(x,y,r, text, color):
    font = pygame.font.Font(None, r)
    text = font.render(text, True, color)
    rect = text.get_rect(center = (x,y))
    screen.blit(text, rect)
root = tk.Tk()
root.title("Логин")
root.geometry("300x200")
style = ttk.Style()
style.theme_use("clam")
namelabel = ttk.Label(root, text="Введите ваше имя")
namelabel.pack()
row = ttk.Entry(root, width = 30, justify="center")
row.pack()
color_label = ttk.Label(root, text="Выберите цвет")
color_label.pack()
color_box = ttk.Combobox(root, values=colors)
color_box.bind("<<ComboboxSelected>>", scroll)
color_box.pack()
login = ttk.Button(root, text="Вход",command = Vxod)
login.pack()
root.mainloop()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
sock.send(("color:<" +name + "," + color + ">").encode())
pygame.init()

WIDTH = 800
HEIGHT = 600
radius = 50
buffer = 1024
old = (0, 0)
CC = (WIDTH//2, HEIGHT//2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактериэе😎😭")
run = True

grid = Grid(screen, "seashell4")
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - CC[0], pos[1] - CC[1]
        lenv = math.sqrt(vector[0]**2 + vector[1]**2)
        vector = vector[0] / lenv, vector[1] / lenv
        if lenv <= radius:
            vector = 0, 0
        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            sock.send(msg.encode())
    data = sock.recv(buffer).decode()
    data = find(data).split(",")
    screen.fill("grey25")
    if data != ['']:
        parameters = list(map(int, data[0].split(" ")))
        radius = parameters[0]
        grid.update(parameters[1:])
        grid.draw()
        draw_bacteries(data[1:])

    pygame.draw.circle(screen, color, CC, radius)
    draw_text(CC[0], CC[1], radius // 2, name, "black")

    pygame.display.flip()


pygame.quit()