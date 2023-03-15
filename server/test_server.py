# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 22:18:43 2023

@author: Stang
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "My flask app"
  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)