"""
Create db
---------
from exp.db import engine, Base
from exp.db.model import Bank
Base.metadata.create_all(engine)

Add rows
--------
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
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite', echo=True)

Session = sessionmaker(bind=engine)