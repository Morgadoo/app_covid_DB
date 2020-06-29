from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "SGBD1920"), encrypted=False)

session = driver.session()


#-------------------------------------------------

# :Local:habitacao - nome - codigo_postal
# :Local:trabalho_escola - nome
# :Local:publico - nome

# :Pessoa - nif - nome


# Relações
    #coabitantes    :Pessoa -> :Pessoa
    #vizinho        :Pessoa -> :Pessoa
    #colega         :Pessoa -> :Pessoa
    
    #frequentou     :Pessoa -> :Local
    #trabalha       :Pessoa -> :Local


#-------------------------------------------------------
import mysql.connector
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.exc import SQLAlchemyError
from sys import argv

arg1 = argv[1]  #nif 
arg2 = argv[2]  #local
arg3 = argv[3]  #data



db = create_engine('mysql+mysqlconnector://SGBD:SGBD1920@localhost/App_Covid')

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
arg3 = arg3.replace("-","_")

consult = s.query(InfPes.nif,InfPes.nome)
s.commit()

ind1 = s.query(InfPes).get(arg1)

if ind1 != None:

    for x in consult:
        session.run("MERGE (:Pessoa{nif: %s, nome: '%s'})" % (x[0], str(x[1])))


    session.run("Merge (:Local{nome: '%s'})" %(arg2))
    session.run("MATCH (a:Pessoa),(b:Local) WHERE a.nif = %s and b.nome = '%s' MERGE (a)-[r:esteve_em{data:'%s'}]->(b)" %(arg1,arg2,arg3))

    print("Registado presença de %s no local %s em %s" %(arg1,arg2,arg3))
    

else:
    print("nif não existe")