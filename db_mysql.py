from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Base = declarative_base()


class Product_tb(Base):

    __tablename__ = 'product'
    sku = Column(Integer, primary_key=True)
    name = Column(String(50))
    prise = Column(Integer)
    brand = Column(String(50))
    quantity = Column(Integer)

    def __init__(self, sku, name, prise, brand,  quantity=0):
        self.sku = sku
        self.name = name
        self.prise = prise
        self.brand = brand
        self.quantity = quantity

    def __repr__(self):
        return "<Good('%s','%s', '%s')>" % (self.sku, self.name, self.prise, self.brand, self.quantity)


class Tshirt_product_tb(Base):

    __tablename__ = 'tshirt_product'
    sku = Column(Integer, ForeignKey('product.id'))
    size = Column(String(50))
    color = Column(String(50))

    def __init__(self, sku, size, color):
        self.sku = sku
        self.size = size
        self.color = color

    def __repr__(self):
        return "<Good('%s','%s', '%s')>" % (self.sku, self.size, self.color)


class Food_product_tb(Base):

    __tablename__ = 'food_product'
    sku = Column(Integer, ForeignKey('product.id'))
    shelf_life = Column(DATETIME)

    def __init__(self, sku, shelf_life):
        self.sku = sku
        self.shelf_life = shelf_life

    def __repr__(self):
        return "<Good('%s','%s', '%s')>" % (self.shelf_life)


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

