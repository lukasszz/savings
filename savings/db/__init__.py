"""
Create db
---------
from db import engine, Base
from db.model import *
Base.metadata.create_all(engine)

Add rows
--------
from db import engine, Base, Session
import exp.db as db
from exp.db.model import Bank
bank = Bank(name='Inteligo', active=True)
session = Session()
session.add(bank)
session.commit()

Select
------

session.query(Bank).all()
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session

from sqlalchemy.interfaces import PoolListener


class ForeignKeysListener(PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')


Base = declarative_base()

engine = None
# engine = create_engine('sqlite:////home/lukasz/Xc/GnuCash20/savings/savings_db.sqlite', echo=True,  listeners=[ForeignKeysListener()])

Session: session = None


def setup(url):
    global engine
    global Session
    engine = create_engine(url, echo=False, listeners=[ForeignKeysListener()])
    Session = sessionmaker(bind=engine)
