import mysql.connector
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.exc import SQLAlchemyError
from sys import argv

arg1 = argv[1]  #nif  

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

    #consul_med = relationship("Consul_Med", back_populates="infpes")

class Consul_Med(Base):

    __tablename__ = 'consul_med'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    nif = Column(Integer(), ForeignKey('infpes.nif'), primary_key=True)
    medico_nome = Column(String(45), nullable=True)
    especialidade = Column(String(20), nullable=True)
    obser = Column(String(30), nullable=True)
    data = Column(String(10),nullable=True)

    #infpes = relationship("InfPes", back_populates="consul_med")
    #sintomas = relationship("Sintomas", back_populates="consul_med")
    #medicacao = relationship("Medicacao", back_populates="consul_med")
    #examcompl = relationship("ExamCompl", back_populates="consul_med")


class Sintomas(Base):
    __tablename__ = 'sintomas'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    sintoma = Column(String(30), nullable=False)

    #consul_med = relationship("Consul_Med", back_populates="sintomas" )


class Medicacao(Base):
    __tablename__ = 'medicacao'
    med_id = Column(Integer(), primary_key=True, autoincrement=True)
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    nome = Column(String(30), nullable=False)
    dose = Column(String(20), nullable=True)
    tratamento = Column(String(20), nullable=True)
    
    #consul_med = relationship("Consul_Med",back_populates="medicacao")   #   sqlalchemy.exc.IntegrityError: (mysql.connector.errors.IntegrityError) 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails 



class ExamCompl(Base):
    __tablename__ = 'examcompl'
    exam_id = Column(Integer(), primary_key=True, autoincrement=True)
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    nome = Column(String(30), nullable=False)
    data = Column(String(10), nullable=False)
    obser = Column(String(20), nullable=True)
    resultado = Column(String(20), nullable=True)

    #consul_med = relationship("Consul_Med", back_populates="examcompl")


#------------------------------

Session = sessionmaker(bind=db)
s = Session()

ind = s.query(InfPes).get(arg1)

if ind != None:

    #ID da Consulta
    consult = s.query(Consul_Med.id).filter(and_(Consul_Med.nif==arg1))
    s.commit()
    consult1= None
    for x in consult:
        consult1 = x[0]
        #print(str(consult1))

        result1 = s.query(Consul_Med).filter(Consul_Med.id==consult1)#
        result2 = s.query(Sintomas).filter(Sintomas.id==consult1)#
        result3 = s.query(Medicacao).filter(Medicacao.id==consult1)#
        result4 = s.query(ExamCompl).filter(ExamCompl.id==consult1)#

        result2.delete(synchronize_session='fetch')
        result3.delete(synchronize_session='fetch')
        result4.delete(synchronize_session='fetch')
        s.commit()

        result1.delete(synchronize_session='fetch')
        s.commit()


    s.delete(ind)

    s.commit()
    print("%s eliminado" % (arg1))
    

else:
    print("nif Invalido")