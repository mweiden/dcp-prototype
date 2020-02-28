# coding: utf-8
import os
import sys

from sqlalchemy import ARRAY, BigInteger, Column, create_engine, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBSessionMaker:
    def __init__(self):
        engine = create_engine("postgresql://localhost:5432/postgres")
        Base.metadata.bind = engine
        self.session_maker = sessionmaker()
        self.session_maker.bind = engine

    def session(self, **kwargs):
        return self.session_maker(**kwargs)


class DCPBase(Base):
    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))


class Users(DCPBase):
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)


class Group(DCPBase):
    id = Column(String, primary_key=True)


class Resource(DCPBase):
    id = Column(String, primary_key=True)


class Role(DCPBase):
    id = Column(String, primary_key=True)
