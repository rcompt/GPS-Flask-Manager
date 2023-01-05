# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 18:32:07 2023

@author: Stang
"""

from datetime import datetime
from flask_restful import Resource, reqparse

from models.locations import LocationModel


class Location(Resource):

    parser = reqparse.RequestParser() 

    parser.add_argument('timestamp',
                        type=str,
                        )          
    parser.add_argument('lat_adj',
                       type=float
                       )
   
    parser.add_argument('long_adj',
                        type=float
                        )
    parser.add_argument('year',
                        type=int
                        )
    parser.add_argument('month',
                        type=int
                        )
    parser.add_argument('day',
                        type=int
                        )
    parser.add_argument('day_of_year',
                        type=int
                        )
    parser.add_argument('hour',
                        type=int
                        )

    def get(self,id_):
        location = LocationModel.find_location_by_id(id_) 
        if location:   
           return location.json() 
        return {'message': 'Location not found'}, 404  
    
    def post(self,id_):
        if LocationModel.find_location_by_id(id_): 

               return {"message": f"A Location with id {id_} already exists"}, 400

        data = Location.parser.parse_args()
        location = LocationModel(id_, **data)
        try:
            location.insert()
        except Exception as inst:
            return {"message" : f"An error occured inserting the location {inst}"}, 500 
        
        return location.json(), 201
     
    def delete(self,id_):                                              
        location = LocationModel.find_location_by_id(id_)
        if location:
            location.delete()
        return {"message" : f"location {id_} deleted"}
     
    def put(self,id_):
        data = Location.parser.parse_args()
        location = LocationModel.find_location_by_id(id_)
        if location:
            location.year = data['year']
            location.ratings = data['ratings']
        else:
            location = LocationModel(id_, **data)
            location.insert()
        return location.json()
     

class LocationList(Resource):

    def get(self):
        return {'locations' : [location.json() for location in LocationModel.query.all()]}
    
    def post(self,id_):
        
        if LocationModel.find_location_by_id(id_): 

               return {"message": f"A Location with id {id_} already exists"}, 400

        data = Location.parser.parse_args()
        location = LocationModel(id_, **data)
        try:
            location.save_to_db()
        except:
            return {"message" : "An error occured inserting the movie"}, 500 
        
        return location.json(), 201
    