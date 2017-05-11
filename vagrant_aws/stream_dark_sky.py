# -*- coding: utf-8 -*-

# I am using python scripts to get data from Dark Sky API that I found on the following githup page: https://github.com/bitpixdigital/forecastiopy3

import requests
import os
import yaml
from forecastiopy import *
import boto
import time
import sys

def get_coordinates(cityName):
    dic = {}
    dic[cityName] = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + cityName.replace(' ', '+')).json()['results'][0]['geometry']['location']

    return dic


credentials = yaml.load(open(os.path.expanduser('~/.ssh/api_cred.yml')))
my_key = credentials['dark_sky']['secret_key']

locations = ['San Francisco', 'Walnut Creek', 'Santa Barbara', 'San Diego']
coord = []
report = {}
while True:
    for elm in locations:
        coord.append(get_coordinates(elm))
    for part in coord:
        for key in part:
            weather = ForecastIO.ForecastIO(my_key, latitude=part[key]['lat'], longitude=part[key]['lng'])
            if weather.has_currently() is True:
               currently = FIOCurrently.FIOCurrently(weather)
               report[key] = FIOCurrently.FIOCurrently.get(currently)
            else:
                print('No current data')
    conn = boto.connect_s3()
    bucket = conn.get_bucket('weatherstream2')
    k = boto.s3.key.Key(bucket)
    k.key = time.strftime("%Y%m%d%H%M")
    k.set_contents_from_string(str(report))

    time.sleep(600)

