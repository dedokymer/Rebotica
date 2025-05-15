# Практика: Подключение
#
# Для начала, импортируем в наш код два модуля: SQLAlchemy и Psycopg2.
# Так как модуль SQLAlchemy довольно большой, мы будем импортировать из него только необходимые функции.

import psycopg2
from  sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

# Далее нужно установить соединение. Делается это специально импортированной функцией create_engine по следующему шаблону:

# engine = create_engine("postgresql+psycopg2://postgres:<Пароль>@localhost/<Название БД>")

engine = create_engine("postgresql+psycopg2://postgres:MofenLuckBro@localhost/postgres")

# При использовании ORM придерживаются системы: одна таблица — один класс.
# Но создавать обычный класс не имеет смысла, его нужно связать с таблицей. Это делается с помощью наследования.

# Сделаем класс, который потом будем наследовать. Для этого импортируем следующую функцию:

Base = declarative_base()


# Теперь классы таблиц нужно наследовать от класса Base.

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=100)
    damage = Column(Integer, default=20)


# Далее нам нужно включить соединение. Делается это после создания классов специальной командой:
Base.metadata.create_all(engine)

# Теперь наши классы успешно связаны с базой данных.
# Чтобы управлять данными в них, создадим сессию.
#
# Сессия — специальное соединение с БД, позволяющее читать и записывать данные.

# Создаём класс сессии и сохраняем его в переменную, например Session. В аргумент bind кладём
# переменную engine.

Session = sessionmaker(bind=engine)
# Теперь создадим экземпляр класса Session и сохраним его в переменную session.
s = Session()

# С помощью этого экземпляра мы сможем взаимодействовать с БД.
#
# Давай создадим экземпляр класса Users и заполним обязательные аргументы.
# После, добавим экземпляр в сессию с помощью s.add(hero) и сделаем коммит изменений в БД.
hero = Users(id=123, name="Keks")
# s.add(hero)
# s.commit()
# Запустим код и вернёмся в pgAdmin.
s.merge(hero)
s.commit()

# Практика: Создание новой таблицы
class Cats(Base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(150), nullable=False)
    hp = Column(Integer, default = 100)
    damage = Column(Integer, default = 5)
# Для создания новой таблицы больше не придётся пользоваться pgAdmin. Теперь достаточно создать новый
# класс, а ORM сам создаст таблицу, соответствующую этому классу.

Base.metadata.create_all(engine)


