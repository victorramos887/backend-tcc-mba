from sqlalchemy import DateTime, ForeignKey
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession
)
from sqlalchemy.ext.asyncio import async_sessionmaker
from dotenv import load_dotenv
from os import path
import os

db = SQLAlchemy()

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../../.env'))


url_do_banco = os.environ.get('SQLALCHEMY_DATABASE_URI_ASNC')

engine = create_async_engine(url_do_banco, pool_recycle=0)
# Base= declarative_base()

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession,
)


class Usuarios(db.Model):

    __table_args__ = {'schema' : 'main'}
    __tablename__ = 'usuarios'

    fid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    USO2013 = db.Column(db.String)
    TU = db.Column(db.String)
    DC = db.Column(db.Float)
    M = db.Column(db.String)
    UL = db.Column(db.Float)

    def __init__(self, id, USO2013, TU, DC, M, UL):
        
        self.id = id
        self.USO2013 = USO2013
        self.TU = TU
        self.DC = DC
        self.M = M
        self.UL = UL

    def to_json(self):
        return json.dumps({c.name: str(getattr(self, c.name)) for c in self.__table__.columns})

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            if isinstance(column.type, DateTime):
                d[column.name] = getattr(self, column.name).strftime("%Y-%m-%dT%H:%M:%S")
            else:
                d[column.name] = getattr(self, column.name)
        return d

class Consumos(db.Model):

    __table_args__ = {'schema' : 'main'}
    __tablename__ = 'consumos'

    id = db.Column(db.Integer, primary_key=True)
    FK = db.Column(db.Integer)
    Data = db.Column(db.Date)
    consumo = db.Column(db.Float)
    
    def __init__(self, FK, Data, consumo):
        self.FK = FK
        self.Data = datetime.strptime(Data, '%Y-%m-%d').date()
        self.consumo = consumo

    def to_json(self):
        return json.dumps({c.name: str(getattr(self, c.name)) for c in self.__table__.columns})

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            if isinstance(column.type, DateTime):
                d[column.name] = getattr(self, column.name).strftime("%Y-%m-%dT%H:%M:%S")
            else:
                d[column.name] = getattr(self, column.name)
        return d