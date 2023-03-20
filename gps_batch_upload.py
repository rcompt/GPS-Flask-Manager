# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:33:05 2023

@author: Stang
"""

# imports

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import requests
import os
import json
import logging
import time

log_config = {
        "filename" : "gps_batch_upload.log",
        "filemode" : "a",
        "level"    : logging.INFO
    }

logging.basicConfig(**log_config)



from datetime import datetime

data_dir = os.path.join("..","..", "Data", "Takeout", "Location History")
os.listdir(data_dir)



def batch_upload(df):
    logger = logging.getLogger('api_logger')
    logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    


    data = {
        'DATA' : [
                {
                    "id" : idx,
                    "timestamp" : str(row["timestamp"]),
                    "lat_adj" : row["lat_adj"],
                    "long_adj" : row["long_adj"],
                    "year" : row["timestamp"].year,
                    "month" : row["timestamp"].month,
                    "day" : row["timestamp"].day,
                    "day_of_year" : row["timestamp"].day_of_year,
                    "hour" : row["timestamp"].hour
                }
                for idx, row in df.iterrows()
            ]
    }
    
    
    # sending post request and saving response as response object 
    response = requests.put(url = "http://192.168.0.246:5000/locationaddbulk", json = data) 
    return response
    
# with open(os.path.join(data_dir, "Records.json"), "r") as fp:
#     records = json.load(fp)
#     df = pd.DataFrame(records["locations"])
    
# df["lat_adj"] = df["latitudeE7"] / 10000000
# df["long_adj"] = df["longitudeE7"] / 10000000
# df["timestamp"] = pd.to_datetime(df["timestamp"])

# temp_df = df[df["timestamp"] >= "2022-04-01"]
