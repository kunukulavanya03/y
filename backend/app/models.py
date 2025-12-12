from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    data = relationship('Data', backref='user')

    def __repr__(self):
        return f'User(id={self.id!r}, name={self.name!r}, email={self.email!r})'

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'Data(id={self.id!r}, data={self.data!r}, user_id={self.user_id!r})'