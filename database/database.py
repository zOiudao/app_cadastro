from sqlalchemy import String, Integer, Float, ForeignKey, create_engine, Column, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from pytz import timezone
from faker import Faker
from random import choice
from rich.table import Table
from rich import print


fake = Faker('pt_BR')
tmz = timezone('America/Sao_Paulo')
ftime = '%d/%m/%Y %H:%M:%S'

db = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    create_at = Column(DateTime, default=lambda: datetime.now(tmz))
    drivers = relationship('Driver', back_populates='user')  # Relacionamento bidirecional

    def __init__(self, name):
        self.name = name


class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cpf = Column(String(14))
    carrier = Column(String(50))
    plate = Column(String(50))
    details = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))  # Chave estrangeira
    user = relationship('User', back_populates='drivers')  # Relacionamento bidirecional
    create_at = Column(DateTime, default=lambda: datetime.now(tmz))

    def __init__(self, name, cpf, carrier, plate, details, user_id):
        self.name = name
        self.cpf = cpf
        self.carrier = carrier
        self.plate = plate
        self.details = details
        self.user_id = user_id


Base.metadata.create_all(db)

# users
def new_user(name):
    new = User(name)
    session.add(new)
    session.commit()
    print(new.name, new.create_at.strftime(ftime))

def _user():
    read = session.query(User).filter_by(id=2).all()
    for user in read:
        print(f"Usuário: {user.name}")
    # Itera sobre os motoristas relacionados
    if user.drivers:
        print("Motoristas cadastrados por ele:")
        for driver in user.drivers:
            print(f"  {driver.name} - {driver.cpf}")
    else:
        print("Nenhum motorista cadastrado.")

# drivers
def new_driver():
    name = fake.unique.name()
    cpf = fake.unique.cpf()
    carrier = fake.unique.bairro()
    plate = fake.unique.license_plate()
    details = fake.unique.country()
    user_id = choice([i.id for i in session.query(User).all()])

    new = Driver(name, cpf, carrier, plate, details, user_id)
    session.add(new)
    session.commit()
    print(new.name, new.create_at.strftime(ftime))
