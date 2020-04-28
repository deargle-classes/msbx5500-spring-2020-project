from app import db
from app import Alert
db.drop_all()
db.create_all()

al=Alert(id=1, srcaddr='122.122.122.122', dstaddr='222.222.222.222', pkts = 8,octets=588, srcport=5555, dstport=80, prot =6,reso=0)
bl=Alert(id=2,srcaddr='333.122.122.122', dstaddr='333.222.222.222', pkts = 8,octets=588, srcport=555, dstport=80, prot =6, reso=1)
cl=Alert(id=3, srcaddr='444.444.444.444', dstaddr='444.444.444.444', pkts = 8,octets=588, srcport=5555, dstport=80, prot =6,reso=0)
db.session.add(al)
db.session.add(bl)
db.session.add(cl)
db.session.commit()
