import mysql.connector
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.exc import SQLAlchemyError
from sys import argv


arg1 = argv[1]  #nif    
arg2 = argv[2]  #nome
arg3 = argv[3]  #data_nascimento
arg4 = argv[4]  #email
arg5 = argv[5]  #telefone
arg6 = argv[6]  #codigo_postal
arg7 = argv[7]  #localidade



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


Session = sessionmaker(bind=db)
s = Session()


ind = s.query(InfPes).get(arg1)

if ind != None:

    ind.nome = arg2
    ind.data_de_nascimento = arg3
    ind.email = arg4
    ind.telefone = arg5
    ind.codigo_postal = arg6
    ind.localidade = arg7
    s.commit()
    print("%s atualizado" % (arg1))
else:
    print("nif Invalido")


