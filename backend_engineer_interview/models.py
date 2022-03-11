from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)  # type: ignore


class Employee(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    secret = Column(String)
