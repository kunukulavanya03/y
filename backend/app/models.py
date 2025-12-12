from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    email: str = Column(String, unique=True, index=True)
    password: str = Column(String)

    data = relationship('Data', backref='user')

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.
        """
        return f'User(id={self.id!r}, name={self.name!r}, email={self.email!r})'

class Data(Base):
    """
    Represents a data entry in the database.
    """
    __tablename__ = 'data'

    id: int = Column(Integer, primary_key=True, index=True)
    data: str = Column(String)
    user_id: int = Column(Integer, ForeignKey('users.id'))

    def __repr__(self) -> str:
        """
        Returns a string representation of the Data object.
        """
        return f'Data(id={self.id!r}, data={self.data!r}, user_id={self.user_id!r})'