# -*- coding: utf-8 -*-
"""
Created on Sat Dec  31 17:20:00 2022

@author: James
"""

import os
import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import logging

from models import setup_db, Location, db_drop_and_create_all

log = logging.getLogger("gps_server_log.txt")    
                  
app = Flask(__name__)
CORS(app, supports_credentials = True)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html",prediction="2.56")

@app.route("/predict",methods=["POST"])
@cross_origin()
def predict():
    if request.data:

        text = request.json.get('TEXT')

        predictionData = {'prediction': list(prediction)}
        
        response = jsonify(predictionData)
        return response
   

if __name__ == "__main__":
    app.run(debug=True)
    log.info("App is running")