from sqlalchemy import create_engine, Column, Integer, String, event, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engines for x.db and y.db
engine_x = create_engine('sqlite:///x.db')
engine_y = create_engine('sqlite:///y.db')


Base_x = declarative_base()
Base_y = declarative_base()

# Define table models
class XTable(Base_x):
    __tablename__ = 'x_table'
    id = Column(Integer, primary_key=True)
    data = Column(String)

class YTable(Base_y):
    __tablename__ = 'y_table'
    id = Column(Integer, primary_key=True)
    data = Column(String)

# Create tables
Base_x.metadata.create_all(engine_x)
Base_y.metadata.create_all(engine_y)

# Create a trigger when data is deleted from the table in x.db
@event.listens_for(XTable, 'after_delete')
def delete_related_data(mapper, connection, target):
    session_y = sessionmaker(bind=engine_y)()
    delYobj=session_y.query(YTable).first()
    session_y.delete(delYobj)
    session_y.commit()

# Add x.db sample data
Session_x = sessionmaker(bind=engine_x)
session_x = Session_x()
session_x.add(XTable(data='x example data2'))
session_x.commit()

# y.db Add sample data
Session_y = sessionmaker(bind=engine_y)
session_y = Session_y()
session_y.add(YTable(data='y example data2'))
session_y.commit()

import time
time.sleep(10)
#When data is deleted from the table in x.db,
#the related table in y.db is deleted with tgigger
#or optional action is taken (update,add).
session_x = sessionmaker(bind=engine_x)()
delXobj=session_x.query(XTable).first()
session_x.delete(delXobj)
session_x.commit()
