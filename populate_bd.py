import sys 

import mysql.connector
import sqlalchemy as db#
from sqlalchemy import *
from sqlalchemy import create_engine 
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import *
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

#--InfPes--

list_InfPes = [
(209432143, "Alvaro Chines", "10-10-1990", "alvarones@gmail.com", 954684596, "2840-433", "Pinhal de Frades"
),
(215654970, "Claudio Mardinez", "25-04-1995", "mardinezo@gmail.com", 934564786, "2865-678", "Quinta das Laranjeiras"
),
(322548962, "Ana Rodrigues", "06-09-2000", "anarodr@gmail.com", 963243877, "2840-732", "Casal do Marco"
),
(239456876, "Daniel Nunes", "04-03-1998", "dnunes@gmail.com", 965322766, "2965-261", "Lagamecas"
),
(245965453, "Isabel Andrade", "05-07-1999", "isadrade@gmail.com", 914567845, "2670-377","Loures"
),
(356986149, "Sara Manuela", "12-02-2001", "samanu@gmail.com", 934586943, "2520/267", "Peniche"
)]


#--Consul_Med--
list_ConsulMed = [
(209432143,"Miguel Oliveira", "Medicina Geral", "01-03-2020",None),
(209432143,"Miguel Fereira", "Medicina Geral", "12-03-2020",None),
(215654970,"Yuri Ferreira", "Medicina Interna", "15-04-2020",None),
(322548962,"Yuri Ferreira", "Pneumologia", "23-02-2020", "diabéticos"),
(239456876,"Ana Pereira", "Medecina Geral", "09-03-2020",None),
(245965453,"David Duarte", "Cardiologia", "12-05-2020","insuficiência cardíaca"),
(356986149,"Luís Guerreiro", "Pneumologia", "22-05-2020",None)]

#--Sintomas--
list_Sintomas = [
(322548962,"febre"),
(239456876,"dores musculares"),
(245965453,"falta de ar")]

#--Medicacao--
list_Medicacao = [
(322548962,"paracetamol","1000mg","3 vez ao dia"),
(239456876,"ibuprofeno","200mg","2 vez ao dia"),
(245965453,"paracetamol","1000mg","3 vez ao dia")]

#--ExamCompl--
list_ExamCompl = [
(209432143,"Exame Covid-19","01-03-2020","Negativo","14 dias de isolamento"),
(209432143,"Exame Covid-19","12-03-2020","Positivo","quarentena em casa"),
(322548962,"Exame Covid-19","23-02-2020","Positivo","quarentena em casa"),
(239456876,"Exame Covid-19","09-03-2020","Negativo","14 dias de isolamento"),
(245965453,"Exame Covid-19","12-05-2020","Positivo","quarentena em casa")]



#iniciar sessão
session = Session()


for x in list_InfPes:
    ind = session.query(InfPes).get(x[0])
    session.commit()
    if ind == None:
        infpes1 = InfPes(nif=x[0], nome=x[1], data_de_nascimento=x[2],
             email=x[3], telefone=x[4], codigo_postal=x[5],
             localidade=x[6])
        session.add(infpes1)
        session.commit()
    else:
        print("-nif já existe")


consul_med1 = Consul_Med(nif = list_ConsulMed[0][0], medico_nome = list_ConsulMed[0][1], especialidade = list_ConsulMed[0][2], data=list_ConsulMed[0][3],  obser=list_ConsulMed[0][4])
consul_med2 = Consul_Med(nif = list_ConsulMed[1][0], medico_nome = list_ConsulMed[1][1], especialidade = list_ConsulMed[1][2], data=list_ConsulMed[1][3],  obser=list_ConsulMed[1][4])
consul_med3 = Consul_Med(nif = list_ConsulMed[2][0], medico_nome = list_ConsulMed[2][1], especialidade = list_ConsulMed[2][2], data=list_ConsulMed[2][3],  obser=list_ConsulMed[2][4])
consul_med4 = Consul_Med(nif = list_ConsulMed[3][0], medico_nome = list_ConsulMed[3][1], especialidade = list_ConsulMed[3][2], data=list_ConsulMed[3][3],  obser=list_ConsulMed[3][4])
consul_med5 = Consul_Med(nif = list_ConsulMed[4][0], medico_nome = list_ConsulMed[4][1], especialidade = list_ConsulMed[4][2], data=list_ConsulMed[4][3],  obser=list_ConsulMed[4][4])
consul_med6 = Consul_Med(nif = list_ConsulMed[5][0], medico_nome = list_ConsulMed[5][1], especialidade = list_ConsulMed[5][2], data=list_ConsulMed[5][3],  obser=list_ConsulMed[5][4])
consul_med7 = Consul_Med(nif = list_ConsulMed[6][0], medico_nome = list_ConsulMed[6][1], especialidade = list_ConsulMed[6][2], data=list_ConsulMed[6][3],  obser=list_ConsulMed[6][4])

for x in list_ConsulMed:
    consult = session.query(Consul_Med.id).filter(and_(Consul_Med.especialidade==x[2], Consul_Med.nif==x[0], Consul_Med.data==x[3], Consul_Med.medico_nome==x[1]))
    session.commit()

    consult1 = None
    for x in consult:
        consult1 = str(x[0])


    if consult1 == None:
        session.add_all([consul_med1,consul_med2,consul_med3,consul_med4,consul_med5,consul_med6,consul_med7])
        session.commit()


        sintomas1 = Sintomas(id=consul_med4.id, sintoma=list_Sintomas[0][1])
        sintomas2 = Sintomas(id=consul_med5.id, sintoma=list_Sintomas[1][1])
        sintomas3 = Sintomas(id=consul_med6.id, sintoma=list_Sintomas[2][1])
        session.add_all([sintomas1,sintomas2,sintomas3])
        session.commit()

        medicacao1 = Medicacao(id=consul_med4.id,nome= list_Medicacao[0][1],dose=list_Medicacao[0][2],tratamento=list_Medicacao[0][3])
        medicacao2 = Medicacao(id=consul_med5.id,nome= list_Medicacao[1][1],dose=list_Medicacao[1][2],tratamento=list_Medicacao[1][3])
        medicacao3 = Medicacao(id=consul_med6.id,nome= list_Medicacao[2][1],dose=list_Medicacao[2][2],tratamento=list_Medicacao[2][3])
        session.add_all([medicacao1,medicacao2,medicacao3])
        session.commit()

     
     
        examcompl1 = ExamCompl(id=consul_med1.id,nome=list_ExamCompl[0][1],data=list_ExamCompl[0][2],resultado=list_ExamCompl[0][2],obser=list_ExamCompl[0][3])
        examcompl2 = ExamCompl(id=consul_med2.id,nome=list_ExamCompl[1][1],data=list_ExamCompl[1][2],resultado=list_ExamCompl[1][2],obser=list_ExamCompl[1][3])
        examcompl3 = ExamCompl(id=consul_med4.id,nome=list_ExamCompl[2][1],data=list_ExamCompl[2][2],resultado=list_ExamCompl[2][2],obser=list_ExamCompl[2][3])
        examcompl4 = ExamCompl(id=consul_med5.id,nome=list_ExamCompl[3][1],data=list_ExamCompl[3][2],resultado=list_ExamCompl[3][2],obser=list_ExamCompl[3][3])
        examcompl5 = ExamCompl(id=consul_med6.id,nome=list_ExamCompl[4][1],data=list_ExamCompl[4][2],resultado=list_ExamCompl[4][2],obser=list_ExamCompl[4][3])
        session.add_all([examcompl1,examcompl2,examcompl3,examcompl4,examcompl5])
        session.commit()

else:
    print("\n||Consulta já existe||")

#||--Show Values--||

consult = session.query(InfPes.nif,InfPes.nome)
session.commit()

print("\n||Pessoas existentes||")
for x in consult:
    print("- nif: %s  nome: %s" % (x[0],str(x[1])))

consult = session.query(Consul_Med.id)
session.commit()

print("\n||Consultas existentes||")
for x in consult:
    print("- id: %s " % (str(x[0])))


consult = session.query(Sintomas.id)
session.commit()

print("\n||Sintomas existentes||")
for x in consult:
    print("- id: %s " % (str(x[0])))


consult = session.query(Sintomas.id)
session.commit()

print("\n||Sintomas existentes||")
for x in consult:

    print("- id: %s " % (str(x[0])))


consult = session.query(Medicacao.id)
session.commit()

print("\n||Medicacao existentes||")
for x in consult:
    print("- id: %s " % (str(x[0])))


consult = session.query(ExamCompl.id)
session.commit()

print("\n||ExamCompl existentes||")
for x in consult:
    print("- id: %s " % (str(x[0])))




# ------- Neo4j -------

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "SGBD1920"), encrypted=False)

s = driver.session()

consult = session.query(InfPes.nif,InfPes.nome)
session.commit()

for x in consult:
    s.run("MERGE (:Pessoa{nif: %s, nome: '%s'})" % (x[0], str(x[1])))

s.run("Merge (:Local{nome: 'Instituto Medico de Braganca'})")


s.run("""
Match(alvaro:Pessoa{nome: 'Alvaro Chines'}), (sara:Pessoa{nome: 'Sara Manuela'}),
(daniel:Pessoa{nome: 'Daniel Nunes'}), (claudio:Pessoa{nome: 'Claudio Mardinez'}),
(ana:Pessoa{nome: 'Ana Rodrigues'}), (isabel:Pessoa{nome: 'Isabel Andrade'}),
(iMed:Local_Freq{nome: 'Instituto Medico de Braganca'}),
(cSaude:Local_Freq{nome: 'Centro de Saude de Seixal'}),
(iCoimbra:Local_Freq{nome: 'Instituto Politecnico de Coimbra'})
Create(alvaro)-[:amigo_de]->(sara),
(daniel)-[:amigo_de]->(claudio),
(ana)-[:amigo_de]->(sara),
(isabel)-[:amigo_de]->(sara),
(daniel)-[:frequenta]->(iMed),
(ana)-[:frequenta]->(iMed),
(claudio)-[:trabalha_em]->(cSaude),
(isabel)-[:frequenta]->(iCoimbra),
(sara)-[:frequenta]->(iCoimbra),
(alvaro)-[:trabalha_em]->(iCoimbra)
""")


