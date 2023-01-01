# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 17:25:52 2022

@author: Stang
"""

import os
from sqlalchemy import Column, String, Integer, create_engine, Float
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    database_name ='local_db_name'
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
class LocationModel(db.Model):
    
    __tablename__ = 'locations'
    id_ = Column(Integer, primary_key=True)
    lat_adj = Column(Float)
    long_adj = Column(Float)
    timestamp = Column(db.DateTime)
    
    def __init__(self, id_, timestamp, lat, long):
        self.id_ = id_
        self.timestamp = timestamp
        self.lat_adj = lat
        self.long_adj = long
        
    def json(self):
        return {
            'id': self.id_,
            'timestamp': self.timestamp,
            'lat_adj': self.lat_adj,
            'long_adj': self.long_adj
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()