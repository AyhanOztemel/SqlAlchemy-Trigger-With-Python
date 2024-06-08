from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    children = relationship("Child", backref="parent", cascade="all, delete-orphan")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    age = Column(Integer)

# Veritabanı bağlantısını kurma
engine = create_engine('sqlite:///z.db')
Base.metadata.create_all(engine)

# Oturum oluşturma ve kullanma
Session = sessionmaker(bind=engine)
session = Session()

# Örnek veri ekleme
parent = Parent(name="john", surname="Doe")
child1 = Child(age=10)
child2 = Child(age=8)
parent.children.append(child1)
parent.children.append(child2)
session.add(parent)
session.commit()

# Örnek veri ekleme
parent = Parent(name="Derek", surname="Doe")
child1 = Child(age=15)
child2 = Child(age=21)
parent.children.append(child1)
parent.children.append(child2)
session.add(parent)
session.commit()

# Parent nesnesini silme
parent_to_delete = session.query(Parent).filter_by(surname="Doe").first()
session.delete(parent_to_delete)
session.commit()
