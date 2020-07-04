from neo4j import GraphDatabase
from sys import argv

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "SGBD1920"), encrypted=False)

session = driver.session()

arg1 = argv[1]  # nif

res = session.run('Match(a:Pessoa{nif:%s})-[n]-(b) return a.nif, b.nome, b.nif, n' % arg1)
# print(res.peek())

# 0 - nif
# 1 - Nomes
# 2 - nif

for a in res:
    if a[2] is not None:
        print('%s %s %s' % (a[0], a[3].type, a[2]))
    else:
        print('%s %s %s' % (a[0], a[3].type, a[1]))
