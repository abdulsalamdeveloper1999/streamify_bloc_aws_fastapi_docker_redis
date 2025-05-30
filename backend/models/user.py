from db.base import Base

from sqlalchemy import Column, Integer, Text


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(Text,nullable=False)
    email=Column(Text,nullable=False,unique=True)
    cognito_sub=Column(Text,unique=True,nullable=False,index=True)
