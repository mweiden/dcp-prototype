# coding: utf-8
import os
import sys

from sqlalchemy import ARRAY, BigInteger, Column, create_engine, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class DBSessionMaker:
    def __init__(self):
        engine = create_engine("postgresql://localhost:5432/postgres")
        Base.metadata.bind = engine
        self.session_maker = sessionmaker()
        self.session_maker.bind = engine

    def session(self, **kwargs):
        return self.session_maker(**kwargs)


class MixinDCP(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))


class Users(Base, MixinDCP):
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)


class Groups(Base, MixinDCP):
    id = Column(String, primary_key=True)


class Resources(Base, MixinDCP):
    id = Column(String, primary_key=True)


class Roles(Base, MixinDCP):
    id = Column(String, primary_key=True)
