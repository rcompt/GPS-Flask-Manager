# -*- coding: utf-8 -*-
"""
Created on Sat Dec  31 17:20:00 2022

@author: James
"""

import os
import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api
import logging

from resources.locations import Location, LocationList


from db import db

app = Flask(__name__)
api = Api(app)

uri = os.getenv("DATABASE_URL") 
if uri: # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

else:
    uri = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Location,'/location/<string:id_>')
api.add_resource(LocationList, '/locations')

db.init_app(app)


if __name__ == '__main__':
   app.run(debug=True)