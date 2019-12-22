from sqlalchemy import Column, Integer, String, Boolean

from exp.db import Base


class Bank(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)

    def __repr__(self):
        return "Bank %s, active=%s" % (self.name, self.active)
