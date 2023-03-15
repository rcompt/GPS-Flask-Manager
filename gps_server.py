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

from resources.locations import Location, LocationList

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

#app.config['SQLALCHEMY_DATABASE_URI'] = database_file
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()

#api.add_resource(Location,'/location/<string:id_>')
#api.add_resource(LocationList, '/locations')

@app.route('/', methods=["GET", "POST"])
def home():
    locations = None
    if request.form:
        try:
            location = Location(id_=request.form.get("title"))
            db.session.add(location)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    locations = Location.query.all()
    return render_template("home.html", locations=locations)
    #return render_template("home.html")

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        location = Location.query.filter_by(id_=oldtitle).first()
        location.id_ = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update location id_")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("title")
    location = Location.query.filter_by(id_=id_).first()
    db.session.delete(location)
    db.session.commit()
    return redirect("/")


@app.errorhandler(Exception)
def handle_exception(err):
    path = request.path # this var was shown to be 'favicon.ico' or 'manifest.json'
    print(path)




if __name__ == '__main__':
   app.run(debug=True)