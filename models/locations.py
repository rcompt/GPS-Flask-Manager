# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 17:25:52 2022

@author: Stang
"""

from db import db

    
class LocationModel(db.Model):
    
    __tablename__ = 'locations_1'
    id_ = db.Column(db.Integer, primary_key=True)
    lat_adj = db.Column(db.Float)
    long_adj = db.Column(db.Float)
    timestamp = db.Column(db.String)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    day_of_year = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    
    def __init__(
            self, 
            id_, 
            timestamp, 
            lat_adj, 
            long_adj,
            year,
            month,
            day,
            day_of_year,
            hour
            ):
        self.id_ = id_
        self.timestamp = timestamp
        self.lat_adj = lat_adj
        self.long_adj = long_adj
        self.year = year
        self.month = month
        self.day = day
        self.day_of_year = day_of_year
        self.hour = hour

        
    def json(self):
        return {
            'id': self.id_,
            'timestamp': self.timestamp,
            'lat_adj': self.lat_adj,
            'long_adj': self.long_adj,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'day_of_year': self.day_of_year,
            'hour': self.hour
        }
    
    @classmethod
    def find_location_by_id(self,id_):
        return self.query.filter_by(id_=id_).first() 
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()