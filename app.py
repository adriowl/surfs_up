#To run this from terminal:
#python3 -m venv venv
#. venv/bin/activate
#export FLASK_APP=app.py
#flask run

#Imports
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Create database engine
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)
# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#Create a session link
session = Session(engine)
#Define Flask app
app = Flask(__name__)
#Define the welcome route
@app.route('/')
def welcome():
    return(
        '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Add precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Our anchor date minus 1 year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Query for precipitation by date >= prev year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    #Query for all the stations
    results = session.query(Station.station).all()
    #Unravel results into a 1D array, convert into list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    #anchor date minus a year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Query for temps from our chosen station for the prev year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    #Convert results into a list
    temps=list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#Have to navigate to link like this: 
#/api/v1.0/temp/2017-06-01/2017-06-30
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)