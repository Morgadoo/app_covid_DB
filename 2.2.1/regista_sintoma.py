import mysql.connector
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.exc import SQLAlchemyError
from sys import argv

from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

arg1 = argv[1]  #nif  
arg2 = argv[2]  #tipo_sintoma
arg3 = argv[3]  #data
arg4 = argv[4]  #notas



db = create_engine('mysql+mysqlconnector://SGBD:SGBD1920@localhost/App_Covid')

Base = declarative_base(bind=db)

class InfPes(Base):
    __tablename__ = 'infpes'
    nif = Column(Integer(), primary_key=True)
    nome = Column(String(45), nullable=False)
    data_de_nascimento = Column(String(10), nullable=False)
    email = Column(String(60), nullable=False)
    telefone = Column(Integer(), nullable=False)
    codigo_postal = Column(String(8), nullable=False)
    localidade = Column(String(50), nullable=False)

    consul_med = relationship("Consul_Med", back_populates="infpes")

class Consul_Med(Base):

    __tablename__ = 'consul_med'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    nif = Column(Integer(), ForeignKey('infpes.nif'), primary_key=True)
    medico_nome = Column(String(45), nullable=True)
    especialidade = Column(String(20), nullable=True)
    obser = Column(String(30), nullable=True)
    data = Column(String(10),nullable=True)

    infpes = relationship("InfPes", back_populates="consul_med")
    sintomas = relationship("Sintomas", back_populates="consul_med")


class Sintomas(Base):
    __tablename__ = 'sintomas'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    sintoma = Column(String(30), nullable=False)

    consul_med = relationship("Consul_Med", back_populates="sintomas")



Session = sessionmaker(bind=db)
s = Session()

ind = s.query(InfPes).get(arg1)

if ind != None:   
    consul_med1 = Consul_Med(nif = arg1 ,obser= arg4,data = arg3)
    s.add(consul_med1)
    s.commit()

    sintomas1 = Sintomas(id = consul_med1.id,sintoma=arg2)
    s.add(sintomas1)
    s.commit()

    print("novo sintoma registado para %s" % (argv[1]))

else:
    print("nif Invalido")



