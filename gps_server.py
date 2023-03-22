# -*- coding: utf-8 -*-
"""
Created on Sat Dec  31 17:20:00 2022

@author: James
"""

import os
import json
import io
import base64
import sqlalchemy as sa
import pandas as pd

import seaborn as sns
import geopandas as geo
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask import Response
import logging
import pickle

from models.locations import Location

from db import db

app = Flask(__name__)


api = Api(app)

with open("config.pickle", "rb") as fp:
    config_obj = pickle.load(fp)
    PASSWORD = config_obj["PASSWORD"]
    IP_ADDRESS = config_obj["IP_ADDRESS"]

#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "postgres:///{}".format(os.path.join(project_dir, "locations.db"))

# uri = os.getenv("DATABASE_URL") 
# if uri: # or other relevant config var
#     if uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)

# else:
#     uri = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = F"postgresql://postgres:{PASSWORD}@localhost/locations"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def location_generator(form):
        return Location(
            form["id"],
            form["timestamp"],
            form["lat_adj"],
            form["long_adj"],
            form["year"],
            form["month"],
            form["day"],
            form["day_of_year"],
            form["hour"]
        )
        

@app.before_first_request
def create_tables():
     db.create_all()

#api.add_resource(Location,'/location/<string:id_>')
#api.add_resource(LocationList, '/locations')

@app.route('/')
def home():
    return '<a href="/addlocation"><button> Click here </button></a>'


gdf = None

@app.route("/addlocation")
def addlocation():
    global gdf
    locations = Location.query.all()
    
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql_query(
        sql = db.select([Location.id_,
                         Location.timestamp,
                         Location.lat_adj,
                         Location.long_adj,
                         Location.year,
                         Location.month,
                         Location.day,
                         Location.day_of_year,
                         Location.hour
                         ]),
        con = engine
    )
    #df["timestamp"] = pd.to_datetime(df["timestamp"])
    #df = df[df["timestamp"] >= "2022-04-01"]
    df["lat_adj"] = df["lat_adj"].astype(float)
    df = df[df["lat_adj"] < 37.82]
    crs = {'init':'EPSG:4326'}
    gdf = geo.GeoDataFrame(
        df, 
        crs = crs,
        geometry=geo.points_from_xy(df.long_adj, df.lat_adj))
    
    #g = sns.jointplot(x=df.long_adj,y=df.lat_adj, height=16, kind="kde")

    #plt.show()
    plot_png()
    return render_template("home.html", locations=locations)

@app.route('/plot.png')
def plot_png():
    global gdf
    sf_map = geo.read_file(os.path.join("..","..","Data", "city-of-san-francisco-california-streets.shp"))
    fig, ax = plt.subplots(figsize = (10,10))
    sf_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey',alpha=0.5)
    gdf.plot(ax=ax)
    ax.set_title('SF Travel')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/locationadd", methods=['POST'])
def personadd():
    db.session.add(location_generator(request.form))
    db.session.commit()

    return redirect("/addlocation")

@app.route("/locationaddbulk", methods=["PUT"])
def locationaddbulk():       
    if request.data:
        db.session.add_all(
            [
                location_generator(location) 
                for location in request.json.get('DATA')
            ]
        )
        db.session.commit()
    locations_count = len(request.json.get('DATA'))
    return jsonify(
        {"RESPONSE" : f"Successfully added: {locations_count} locations"}
    )
    
@app.route("/retrieve", methods=["GET"])
def get():
    row_id = request.args.get('row_id')
    return jsonify(
        {
            "RESPONSE" : f"{row_id}, here is your data",
            "DATA" : [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
            ]
        }
    )

@app.route("/update", methods=["POST"])
def update():
    new_id = request.form.get("new_id")
    old_id = request.form.get("old_id")
    location = Location.query.filter_by(id_=old_id).first()
    location.id_ = new_id
    db.session.commit()
    return redirect("/addlocation")

@app.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")
    location = Location.query.filter_by(id_=id_).first()
    db.session.delete(location)
    db.session.commit()
    return redirect("/addlocation")


if __name__ == '__main__':
    #db.create_all()
    app.run(host=IP_ADDRESS, debug=True)