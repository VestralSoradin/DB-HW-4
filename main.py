import sqlalchemy
import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id_publ = sq.Column('id_publ', sq.Integer, primary_key=True)
    name = sq.Column('name', sq.String(length=40))

    def __init__(self, id_publ, name):
        self.id_publ = id_publ
        self.name = name

    def __repr__(self):
        return f'({self.id_publ}) {self.name}'


class Book(Base):
    __tablename__ = 'book'
    id_book = sq.Column('id_book', sq.Integer, primary_key=True)
    title = sq.Column('title', sq.String(length=40))
    id_publ = sq.Column('id_publ', sq.Integer, sq.ForeignKey('publisher.id_publ'))

    def __repr__(self):
        return f'{self.title}'


    def __init__(self, id_book, title, id_publ):
        self.id_book = id_book
        self.title = title
        self.id_publ = id_publ


class Shop(Base):
    __tablename__ = 'shop'
    id_shop = sq.Column('id_shop', sq.Integer, primary_key=True)
    name = sq.Column('name', sq.String(length=40))

    def __init__(self, id_shop, name):
        self.id_shop = id_shop
        self.name = name

    def __repr__(self):
        return f'{self.name}'



class Stock(Base):
    __tablename__ = 'stock'
    id_stock = sq.Column('id_stock', sq.Integer, primary_key=True)
    id_book = sq.Column('id_book', sq.Integer, sq.ForeignKey('book.id_book'))
    id_shop = sq.Column('id_shop', sq.Integer, sq.ForeignKey('shop.id_shop'))
    count = sq.Column('count', sq.Integer)

    def __init__(self, id_stok, id_book, id_shop, count):
        self.id_stock = id_stok
        self.id_book = id_book
        self.id_shop = id_shop
        self.count = count


class Sale(Base):
    __tablename__ = 'sale'
    id_price = sq.Column('id_price', sq.Integer, primary_key=True)
    price = sq.Column('price', sq.Integer)
    date_sale = sq.Column('date_sale', sq.Date)
    id_stock = sq.Column('id_stock', sq.Integer, sq.ForeignKey('stock.id_stock'))
    count = sq.Column('count', sq.Integer)

    def __init__(self, id_price, price, date_sale, id_stock, count):
        self.id_price = id_price
        self.price = price
        self.date_sale = date_sale
        self.id_stock = id_stock
        self.count = count

    def __repr__(self):
        return f'{self.price} | {self.date_sale}'



engine = create_engine('postgresql://postgres:@localhost:5432/hw_db_4')
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session: Session = Session()

publ_1 = Publisher(1,'Лавкрафт')
publ_2 = Publisher(2,'Эдгар По')
publ_3 = Publisher(3, 'Гоголь')

session.add(publ_1)
session.add(publ_2)
session.add(publ_3)
session.commit()

book_1 = Book(1, 'Хребты безумия', 1)
book_2 = Book(2, 'Крысы в стенах', 1)
book_3 = Book(3, 'Ворон', 2)
book_4 = Book(4, 'Вечера на хуторе близ Диканьки', 3)

session.add(book_1)
session.add(book_2)
session.add(book_3)
session.add(book_4)
session.commit()

shop_1 = Shop(1, 'Буквоед')
shop_2 = Shop(2, 'Книжная гавань')

session.add(shop_1)
session.add(shop_2)

session.commit()

stock_1 = Stock(1, 1, 1, 1)
stock_2 = Stock(2, 2, 1, 1)
stock_3 = Stock(3, 3, 2, 1)
stock_4 = Stock(4, 4, 2, 1)

session.add(stock_1)
session.add(stock_2)
session.add(stock_3)
session.add(stock_4)

session.commit()

sale_1 = Sale(1, 500, '23.06.2019', 1, 1)
sale_2 = Sale(2, 200, '17.08.2021', 2, 1)
sale_3 = Sale(3, 300, '13.04.2018', 3, 1)
sale_4 = Sale(4, 400, '06.11.2020', 4, 1)

session.add(sale_1)
session.add(sale_2)
session.add(sale_3)
session.add(sale_4)

session.commit()
writer = input('Введите имя или ID автора ')

query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale
                      ).join(Publisher).join(Stock).join(Shop).join(Sale)
if writer.isdigit():
    query = query.filter(Publisher.id_publ == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for Book.title, Shop.name, Sale.price, Sale.date_sale in query:
    print(f"{Book.title: <40} | {Shop.name: <10} | {Sale.price: <8} | "
          f"{Sale.date_sale.strftime('%d-%m-%Y')}")


session.close()