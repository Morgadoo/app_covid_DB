import sys 

import mysql.connector
import sqlalchemy as db#
from sqlalchemy import create_engine 
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship





#criar engine ligação à bd
engine = create_engine('mysql+mysqlconnector://SGBD:SGBD1920@localhost/App_Covid')

#se não existir bd, cria
if not database_exists(engine.url):
    create_database(engine.url)


#declarative base
Base = declarative_base(bind=engine)

#obter fabrica de sessões
Session = sessionmaker(bind=engine)

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
    medicacao = relationship("Medicacao", back_populates="consul_med")
    examcompl = relationship("ExamCompl", back_populates="consul_med")


class Sintomas(Base):
    __tablename__ = 'sintomas'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    sintoma = Column(String(30), nullable=False)

    consul_med = relationship("Consul_Med", back_populates="sintomas")


class Medicacao(Base):
    __tablename__ = 'medicacao'
    med_id = Column(Integer(), primary_key=True, autoincrement=True)
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    nome = Column(String(30), nullable=False)
    dose = Column(String(20), nullable=True)
    tratamento = Column(String(20), nullable=True)
    
    consul_med = relationship("Consul_Med",back_populates="medicacao")   #    consul_med = relationship("Consul_Med", cascade="all, delete-orphan",back_populates="medicacao",single_parent=True)



class ExamCompl(Base):
    __tablename__ = 'examcompl'
    exam_id = Column(Integer(), primary_key=True, autoincrement=True)
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    nome = Column(String(30), nullable=False)
    data = Column(String(10), nullable=False)
    obser = Column(String(20), nullable=True)
    resultado = Column(String(20), nullable=True)

    consul_med = relationship("Consul_Med", back_populates="examcompl")


#------------------------------

#create a Schema
Base.metadata.create_all(engine)

#iniciar sessão
session = Session()

inspector = inspect(engine)



session.commit()

for table_name in inspector.get_table_names():
    print("\n|||Object: %s" % table_name + "|||")
    for column in inspector.get_columns(table_name):
        print("-" + column['name'])

print("\n## SQLAlchemy ORM --> Objetos criados com sucesso. ##\n")

