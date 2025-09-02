import math
import socket
import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pygame
from russian_names import RussianNames
import random

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
main_socket.bind(("localhost", 10000))  # IP и порт привязываем к порту
main_socket.setblocking(False)  # Непрерывность, не ждём ответа
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных подключений
print("Сокет создался")
engine = create_engine("postgresql+psycopg2://postgres:MofenLuckBro@localhost/Reboticatable")
session = sessionmaker(bind=engine)
base = declarative_base()
s = session()


class Player(base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    absspeed = Column(Integer, default=2)
    speedx = Column(Integer, default=2)
    speedy = Column(Integer, default=2)
    color = Column(String(250), default="red")
    w_vision = Column(Integer, default=800)
    h_vision = Column(Integer, default=600)

    def __init__(self, name, address):
        self.name = name

        self.address = address


class Localplayer():
    def change_speed(self, vector: str):
        vector = find(vector)
        if vector[0] == 0 and vector[1] == 0:
            self.speedx = 0
            self.speedy = 0
        else:
            vector = vector[0] * self.absspeed, vector[1] * self.absspeed
            self.speedx = vector[0]
            self.speedy = vector[1]

    def sync(self):
        self.db.size = self.size
        self.db.absspeed = self.absspeed
        self.db.speedx = self.speedx
        self.db.speedy = self.speedy
        self.db.errors = self.errors
        self.db.x = self.x
        self.db.y = self.y
        self.db.color = self.color
        self.db.w_vision = self.w_vision
        self.db.h_vision = self.h_vision
        s.merge(self.db)
        s.commit()

    def load(self):
        self.size = self.db.size
        self.absspeed = self.db.absspeed
        self.speedx = self.db.speedx
        self.speedy = self.db.speedy
        self.errors = self.db.errors
        self.x = self.db.x
        self.y = self.db.y
        self.color = self.db.color
        self.w_vision = self.db.w_vision
        self.h_vision = self.db.h_vision
        return self

    def __init__(self, id, address, name, sock):
        self.x = 500
        self.y = 500
        self.id = id
        self.address = address
        self.name = name
        self.sock = sock
        self.db: Player = s.get(Player, self.id)
        self.size = 50
        self.speedx = 0
        self.speedy = 0
        self.errors = 0
        self.absspeed = 1
        self.color = "red"
        self.w_vision = 800
        self.h_vision = 600

    def update(self):
        # х координата
        if self.x - self.size <= 0:  # Если игрок вылазит за левую стенку
            if self.speedx >= 0:  # Но при этом двигается право
                self.x += self.speedx  # то двигаем его
        elif self.x + self.size >= WIDHT_ROOM:  # Если игрок вылазит за правую стенку
            if self.speedx <= 0:  # Но при этом двигается влево
                self.x += self.speedx  # то двигаем его
        else:  # Если игрок находится в границе комнаты
            self.x += self.speedx

        # y координата
        if self.y - self.size <= 0:  # Если игрок вылазит за левую стенку
            if self.speedy >= 0:  # Но при этом двигается право
                self.y += self.speedy  # то двигаем его
        elif self.y + self.size >= HEIGHT_ROOM:  # Если игрок вылазит за правую стенку
            if self.speedy <= 0:  # Но при этом двигается влево
                self.y += self.speedy  # то двигаем его
        else:  # Если игрок находится в границе комнаты
            self.y += self.speedy


base.metadata.create_all(engine)
pygame.init()
WIDHT_ROOM, HEIGHT_ROOM = 4000, 4000
WIDHT_SERVER, HEIGHT_SERVER = 300, 300
screen = pygame.display.set_mode((WIDHT_SERVER, HEIGHT_SERVER))
pygame.display.set_caption("Сервер")
clock = pygame.time.Clock()
FPS = 100
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']
mob_quality = 25
names = RussianNames(count=mob_quality * 2, surname=False, patronymic=False, rare=True)
names = list(set(names))


def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(map(float, vector[first + 1:second].split(",")))
            return result


def find_color(info: str):
    first = None
    for num, sign in enumerate(info):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = info[first + 1:second].split(",")
            return result
    return ""


players = {}
serverwork = True
for i in range(mob_quality):
    servermob = Player(names[i], None)
    servermob.color = random.choice(colors)
    servermob.x = random.randint(0, WIDHT_ROOM)
    servermob.y = random.randint(0, HEIGHT_ROOM)
    servermob.speedx = random.randint(-1, 1)
    servermob.speedy = random.randint(-1, 1)
    servermob.size = random.randint(10, 100)
    s.add(servermob)
    s.commit()
    localmob = Localplayer(servermob.id, None, servermob.name, None).load()
    players[servermob.id] = localmob
# Игровой цикл
tick = -1
while serverwork:
    clock.tick(FPS)
    tick += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            serverwork = False
    if tick %200 == 0:
        try:
            # проверяем желающих войти в игру
            new_socket, addr = main_socket.accept()  # принимаем входящие
            print('Подключился', addr)
            new_socket.setblocking(False)
            login = new_socket.recv(1024).decode()
            player = Player("Сеня", addr)
            if login.startswith("color"):
                data = find_color(login[6:])
                player.name, player.color = data
            s.merge(player)
            s.commit()
            addr = f"({addr[0]},{addr[1]})"
            data = s.query(Player).filter(Player.address == addr)
            for user in data:
                player = Localplayer(user.id, addr, "Сеня", new_socket).load()
                players[user.id] = player


        except BlockingIOError:
            pass
    visible_bacteries = {}
    for id in list(players):
        visible_bacteries[id] = []

    pairs = list(players.items())
    for i in range(0, len(pairs)):
        for j in range(i + 1, len(pairs)):
            hero_1: Localplayer = pairs[i][1]
            hero_2: Localplayer = pairs[j][1]
            dist_x = hero_2.x - hero_1.x
            dist_y = hero_2.y - hero_1.y

            # i-й игрок видит j-того
            if abs(dist_x) <= hero_1.w_vision // 2 + hero_2.size and abs(dist_y) <= hero_1.h_vision // 2 + hero_2.size:
                if hero_1.address is not None:
                    distance = math.sqrt(dist_x**2+dist_y**2)
                    if distance <= hero_1.size and hero_1.size > hero_2.size*1.1:
                        hero_2.size, hero_2.speedx, hero_2.speedy = 0,0,0

                    x_ = str(round(dist_x))
                    y_ = str(round(dist_y))  # временные
                    size_ = str(round(hero_2.size))
                    color_ = hero_2.color
                    data = x_ + " " + y_ + " " + size_ + " " + color_
                    visible_bacteries[hero_1.id].append(data)

                # j-й игрок видит i-того
            if abs(dist_x) <= hero_2.w_vision // 2 + hero_1.size and abs(
                    dist_y) <= hero_2.h_vision // 2 + hero_1.size:

                distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
                if distance <= hero_2.size and hero_2.size > hero_1.size * 1.1:
                    hero_1.size, hero_1.speedx, hero_1.speedy = 0, 0, 0

                if hero_2.address is not None:
                    x_ = str(round(-dist_x))
                    y_ = str(round(-dist_y))  # временные
                    size_ = str(round(hero_1.size))
                    color_ = hero_1.color
                    data = x_ + " " + y_ + " " + size_ + " " + color_
                    visible_bacteries[hero_2.id].append(data)

    for id in list(players):
        visible_bacteries[id] = "<" + ",".join(visible_bacteries[id]) + ">"

    ########################################################################################################################
    for id in list(players):
        if players[id].errors >= 500 or players[id].size == 0:
            if players[id].sock is not None:
                players[id].sock.close()
            del players[id]
            s.query(Player).filter(Player.id == id).delete()
            s.commit()
    # Считываем команды игроков
    for id in list(players):
        if players[id].sock is not None:
            try:
                data = players[id].sock.recv(1024).decode()
                print("Получил", data)
                players[id].change_speed(data)
            except:
                pass
        else:
            if tick %400 == 0:
                vector = f"<{random.uniform(-1, 1)},{random.uniform(-1, 1)}>"
                players[id].change_speed(vector)

    # Отправка игрокам поля
    for id in list(players):
        if players[id].sock is not None:
            try:
                players[id].sock.send(visible_bacteries[id].encode())
            except:
                players[id].sock.close()
                del players[id]
                s.query(Player).filter(Player.id == id).delete()
                s.commit()
                print("Сокет закрыт")
    screen.fill("black")
    for id in players:
        player = players[id]
        x = player.x * WIDHT_SERVER // WIDHT_ROOM
        y = player.y * HEIGHT_SERVER // HEIGHT_ROOM
        size = player.size * WIDHT_SERVER // WIDHT_ROOM
        pygame.draw.circle(screen, player.color, (x, y), size)
    for id in list(players):
        player = players[id]
        players[id].update()
    pygame.display.update()

pygame.quit()
main_socket.close()
s.query(Player).delete()
s.commit()
