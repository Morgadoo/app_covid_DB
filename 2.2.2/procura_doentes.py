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

    i_h = relationship("I_H", back_populates="infpes")


class I_H(Base):
    __tablename__ = 'i_h'
    nif = Column(String(9), ForeignKey('infpes.nif'), primary_key=True)
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    data = Column(String(10))

    infpes = relationship("InfPes", back_populates="i_h")
    consul_med = relationship("Consul_Med", back_populates="i_h")


class Consul_Med(Base):
    __tablename__ = 'consul_med'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    medico_nome = Column(String(45), nullable=True)
    especialidade = Column(String(20), nullable=True)
    obser = Column(String(30), nullable=True)

    i_h = relationship("I_H", back_populates="consul_med")
    sintomas = relationship("Sintomas", back_populates="consul_med")
    con_med = relationship("Con_Med", back_populates="consul_med")
    con_exam = relationship("Con_Exam", back_populates="consul_med")


class Sintomas(Base):
    __tablename__ = 'sintomas'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    sintoma = Column(String(30), nullable=True)

    consul_med = relationship("Consul_Med", back_populates="sintomas")


# ------------------------------------------------------------------

class Con_Med(Base):
    __tablename__ = 'con_med'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    med_id = Column(Integer(), ForeignKey('medicacao.med_id'), primary_key=True)

    consul_med = relationship("Consul_Med", back_populates="con_med")
    medicacao = relationship("Medicacao", back_populates="con_med")


# ----------
class Medicacao(Base):
    __tablename__ = 'medicacao'
    med_id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(30), nullable=False)
    dose = Column(String(20), nullable=True)
    tratamento = Column(String(20), nullable=True)

    con_med = relationship("Con_Med", back_populates="medicacao")


# -----------

class Con_Exam(Base):
    __tablename__ = 'con_exam'
    id = Column(Integer(), ForeignKey('consul_med.id'), primary_key=True)
    exam_id = Column(Integer(), ForeignKey('examcompl.exam_id'), primary_key=True)

    consul_med = relationship("Consul_Med", back_populates="con_exam")
    examcompl = relationship("ExamCompl", back_populates="con_exam")


class ExamCompl(Base):
    __tablename__ = 'examcompl'
    exam_id = Column(Integer(), primary_key=True, autoincrement=True)
    nome = Column(String(30), nullable=False)
    data = Column(String(10), nullable=False)
    obser = Column(String(20), nullable=True)
    resultado = Column(String(20), nullable=True)

    con_exam = relationship("Con_Exam", back_populates="examcompl")


Session = sessionmaker(bind=db)
s = Session()

ind = s.query(InfPes, ExamCompl).filter(and_(ExamCompl.resultado == 'Positivo',
                                  ExamCompl.nome == 'COVID-19',
                                  ExamCompl.exam_id == Con_Exam.exam_id,
                                  Consul_Med.id == Con_Exam.id,
                                  Consul_Med.id == I_H.id,
                                  InfPes.nif == I_H.nif))

for i, e in ind:
    print('nif: %s data do exame: %s' % (i.nif, e.data))
