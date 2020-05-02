from db import engine, Base
from db.model import *

Base.metadata.create_all(engine)