from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Base = declarative_base()


class Good_tb(Base):

    __tablename__ = 'good'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    prise = Column(Integer)
    manufacturer = Column(String(50))
    size = Column(String(50))
    count = Column(Integer)

    def __init__(self, name, prise, manufacturer, size, count=0):
        self.name = name
        self.prise = prise
        self.manufacturer = manufacturer
        self.size = size
        self.count = count

    def __repr__(self):
        return "<Good('%s','%s', '%s')>" % (self.name, self.prise, self.manufacturer, self.size, self.count)


# class Warehouse_tb(Base):
#
#     __tablename__ = 'warehouse'
#     id = Column(Integer, primary_key=True)
#     id_good = Column(Integer, ForeignKey('good.id'))
#     count = Column(Integer)
#
#
#     def __init__(self, id_good, count):
#         self.id_good = id_good
#         self.count = count
#
#
#     def __repr__(self):
#         return "<Good('%s','%s', '%s')>" % (self.id_good, self.count)


def connect(user, pwd, host='localhost', echo=True):
    return create_engine(f"""mysql+pymysql://{user}:{pwd}@{host}/test""", echo=echo, pool_pre_ping=True)


def migration(engine):
    Base.metadata.create_all(engine)


def create_session(engine):
    return sessionmaker(bind=engine)()


# engine = connect('root', 'root')
# session = create_session(engine)
# migration(engine)
#
# ggGood = Good_tb("GG_2", 300, "USA", 'XXL')
# session.add(ggGood)
# session.commit()

