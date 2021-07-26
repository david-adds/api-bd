from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

engine = create_engine('sqlite:///tasks.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)

    def __repr__(self):
        return '<Person {}>'.format(self.name)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()
        
class Tasks(Base):
    __tablename__ ='tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('People')
    
    def __repr__(self):
            return '<Task {}>'.format(self.name)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Users(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20))

    def __repr__(self):
        return '<Users {}>'.format(self.login)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()
    
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    
