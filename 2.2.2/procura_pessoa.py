import mysql.connector
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.exc import SQLAlchemyError
from sys import argv

db = create_engine('mysql+mysqlconnector://SGBD:SGBD1920@localhost/app_covid')

Base = declarative_base(bind=db)


class InfPes(Base):
    __tablename__ = 'infpes'
    nif = Column(String(9), primary_key=True)
    nome = Column(String(45), nullable=False)
    data_de_nascimento = Column(String(10), nullable=False)
    email = Column(String(60), nullable=False)
    telefone = Column(String(9), nullable=False)
    codigo_postal = Column(String(8), nullable=False)
    localidade = Column(String(50), nullable=False)


Session = sessionmaker(bind=db)
s = Session()

ind = s.query(InfPes).get(argv[1])
if ind:
    print("Pessoa encontrada: %s %s %s %s %s %s %s" % (ind.nif, ind.nome, ind.data_de_nascimento,
            ind.email, ind.telefone, ind.codigo_postal, ind.localidade))
else:
    print("Pessoa não encontrada: %s" % (argv[1]))
