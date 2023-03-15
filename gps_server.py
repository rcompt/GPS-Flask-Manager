# -*- coding: utf-8 -*-
"""
Created on Sat Dec  31 17:20:00 2022

@author: James
"""

import os
import json

from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS, cross_origin
from flask_restful import Api
import logging

from models.locations import Location

from db import db

app = Flask(__name__)


api = Api(app)

#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "postgres:///{}".format(os.path.join(project_dir, "locations.db"))

# uri = os.getenv("DATABASE_URL") 
# if uri: # or other relevant config var
#     if uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)

# else:
#     uri = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:<password>@localhost/locations"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_tables():
     db.create_all()

#api.add_resource(Location,'/location/<string:id_>')
#api.add_resource(LocationList, '/locations')

@app.route('/')
def home():
    return '<a href="/addlocation"><button> Click here </button></a>'


@app.route("/addlocation")
def addlocation():
    return render_template("home.html")


@app.route("/locationadd", methods=['POST'])
def personadd():
    
    entry = Location(
        request.form["id"],
        request.form["timestamp"],
        request.form["lat_adj"],
        request.form["long_adj"],
        request.form["year"],
        request.form["month"],
        request.form["day"],
        request.form["day_of_year"],
        request.form["hour"]
    )
    db.session.add(entry)
    db.session.commit()

    return render_template("home.html")




if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)