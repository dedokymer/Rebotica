#Сделай 5 новых строк в БД с помощью создания экземпляров класса Users.

#2. Создай ещё один класс Enemies, задай им параметры и впиши пару строчек данных.


import psycopg2
from  sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String


engine = create_engine("postgresql+psycopg2://postgres:MofenLuckBro@localhost/postgres")

Base = declarative_base()
class Users(Base):
    __tablename__ = ("users")
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=200)
    damage = Column(Integer, default=45)
class Enemies(Base):
    __tablename__ = ("enemies")
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    hp = Column(Integer, default=100)
    damage = Column(Integer, default=15)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

s = Session()

rep = Capi(id=678, name="Sharik")
s.add(rep)
s.commit()
# s.merge(rep)
# s.commit()