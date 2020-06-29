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
arg2 = argv[2]  #especialidade
arg3 = argv[3]  #data
arg4 = argv[4]  #nome_medico
arg5 = argv[5]  #obser
arg6 = argv[6]  #medicação
arg7 = argv[7]  #exames


db = create_engine('mysql+mysqlconnector://SGBD:SGBD1920@localhost/App_Covid')


#declarative base
Base = declarative_base(bind=db)

#obter fabrica de sessões
Session = sessionmaker(bind=db)

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



s = Session()


ind = s.query(InfPes).get(arg1)

consult = s.query(Consul_Med.id).filter(and_(Consul_Med.especialidade==arg2, Consul_Med.nif==arg1, Consul_Med.data==arg3, Consul_Med.medico_nome==arg4))
s.commit()

consult1 = None
for x in consult:
    consult1 = str(x[0])
#print("Id da Consulta: " + str(consult1))


if ind != None and consult1 == None:

    
    arg6=arg6.replace("{","")
    arg6=arg6.replace("}","")
    arg6={i.split(': ')[0]: i.split(': ')[1] for i in arg6.split(', ')}
   
    arg7=arg7.replace("{","")
    arg7=arg7.replace("}","")
    arg7={i.split(': ')[0]: i.split(': ')[1] for i in arg7.split(', ')} 


    consul_med1 = Consul_Med(nif = arg1,medico_nome = arg4, especialidade = arg2, obser=arg5 ,data=arg3)
    s.add(consul_med1)
    s.commit()

    medicacao1 = Medicacao(id=consul_med1.id,nome= arg6["nome"],dose= arg6["dose"],tratamento=arg6["tratamento"])
    examcompl1 = ExamCompl(id=consul_med1.id,nome=arg7["nome"],data=arg7["data"],resultado=arg7["resultado"])
    s.add(medicacao1)
    s.add(examcompl1)
    s.commit()

    
    print("nova consulta médica registada para %s" % (argv[1]))

else:

    print("nif Invalido ou consulta já existente")

#python3 ./2.2.1/regista_consulta_medica.py <nif> pneumonologia 2020-05-20 "Madalena Lopes" "Doente exibe sintomas COVID-19" "{nome: Benuron, dose: 1gr, tratamento: 8h em 8h}" "{nome: COVID-19, data: 2020-05-20, resultado: Positivo}"