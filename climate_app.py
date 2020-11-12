import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool, echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
        return """<html>
<h1>Homework Step 2 - Climate App </h1>

<img src="https://afar-production.imgix.net/uploads/images/afar_post_headers/images/s6P1cWj2kE/original_hawaii_202019.jpg", 
width=400
alt="Hawaii Pic"/>

<p>Precipitation Data:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Data:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Data:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Data:</p>
<ul>
  <li><a href="/api/v1.0/2017-01-01">/api/v1.0/2017-01-01</a></li>
</ul>
<p>Start & End Day Data:</p>
<ul>
  <li><a href="/api/v1.0/2017-01-01/2017-01-14">/api/v1.0/2017-01-01/2017-01-14</a></li>
</ul>
</html>
"""


@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the query results to a dictionary using date as the key and prcp as the value.
        y = dt.date(2017,8,23) - dt.timedelta(days=365)
        
        prcp_score = session.query(M.date, M.prcp).\
                filter(M.date >= y).\
                order_by(M.date).all()
        
        pcrp_score1 = dict(prcp_score)

        # Return the JSON representation of your dictionary.
        return jsonify(pcrp_score1)


@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON list of stations from the dataset.
        s1 = session.query(S.station, S.name).all()
        
        s2 = list(s1)
        
        return jsonify(s2)


@app.route("/api/v1.0/tobs")
def tobs():
        # Query the dates and temperature observations of the most active station for the last year of data.
        y = dt.date(2017,8,23) - dt.timedelta(days=365)
      
        # Return a JSON list of temperature observations (TOBS) for the previous year.
        tobs_data = session.query(M.date, M.tobs).\
                filter(M.date >= y).\
                order_by(M.date).all()
        
        tobs_data1 = list(tobs_data)
   
        return jsonify(tobs_data1)

#Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")

# When given the start only, calculate TMIN, TAVG, 
# and TMAX for all dates greater than and equal to the start date.

def start_day(start):
        start_day = session.query(M.date, func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
                filter(M.date >= start).\
                group_by(M.date).all()
       
        start_day1= list(start_day)
      
        return jsonify(start_day1)


@app.route("/api/v1.0/<start>/<end>")

# When given the start and the end date, calculate 
# the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

def start_end_day(start, end):
        start_end = session.query(M.date, func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
                filter(M.date >= start).\
                filter(M.date <= end).\
                group_by(M.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day1 = list(start_end)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day1)


if __name__ == '__main__':
    app.run(debug=True)


