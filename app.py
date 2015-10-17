"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 

  """

  app.logger.debug("Got a JSON request");
  miles = request.args.get('miles', 0, type=float)
  brevet = request.args.get('brevet', 0, type=str)
  app.logger.debug(brevet)
  date = request.args.get('date', 0, type=str)
  app.logger.debug(date)
  time = request.args.get('time', 0, type=str)
  app.logger.debug(time)
  start_date = arrow.get(date + " "+ time, "ddd MM/DD/YYYY HH:mm")
  app.logger.debug(start_date)
  km = miles * 1.60934
  app.logger.debug(km)
  if km <200:
    opentime = start_date.replace(hours=+ km/34)
    closetime = start_date.replace(hours=+ km/15)
    #return jsonify(opentime, closetime)
  elif (200 <= km <= 220):
    opentime =  start_date.replace(hours=+ 200/34)
    closetime = start_date.replace(hours=+ 13.5)
    #return jsonify(opentime, closetime)
  elif 220 < km:
    opentime = "error"
    closetime ="error"
  elif km < 300 and brevet == "300":
    opentime = start_date.replace(hours =+ (200/34) + ((km - 200)/32))
    closetime = start_date.replace(hours=+ km/15)
      #return jsonify(opentime, closetime)
  elif  brevet == "300" and 300< km <= 330:
    opentime = start_date.replace(hours=+ (200/34) + (100/32))
    closetime = start_date.replace(hours=+ 20)
  elif brevet == "300" and 330 < km:
    opentime = "error"
    closetime ="error"
  elif brevet == "400" and km < 400:
    opentime = start_date.replace(hours =+(200/34) + ((km -200)/32))
    closetime = start_date.replace(hours=+ km/15)
  elif brevet =="400" and 400 < km <= 440:
    opentime = start_date.replace(hours=+(200/34)+ (200/32))
    closetime = start_date.replace(hours=+27)
  elif brevet == "400" and 440 < km:
    opentime = "error"
    closetime ="error"
  elif brevet == "600" and km < 600:
    opentime = start_date.replace(hours=+ (200/34) + (200/32) + ((km-400)/30))
    closetime = start_date.replace(hours=+ km/15)
  elif brevet == "600" and 600 < km < 660:
    opentime = start_date.replace(hours=+ (200/34) + (200/32) + (200/30))
    closetime = start_date.replace(hours=+40)
      
  elif brevet == "600" and 660 < km:
    opentime = "error"
    closetime ="error"
  elif brevet == "1000" and km < 1000:
    opentime = start_date.replace(hours=+ (200/34) + (200/32) + (200/30) + (km-600)/28)
    closetime = start_date.replace(hours=+ (600/15) + (km-600)/11.428)
  elif brevet == "1000" and 1000 < km <1100:
    opentime = start_date.replace(hours=+ (200/34) + (200/32) + (200/30) + (400/28))
    closetime = start_date.replace(hours=+ (600/15)+(400/11.428))
  elif brevet == "1000" and 1100 < km:
    opentime = "error"
    closetime ="error"

  #open_time = opentime
  open_time = format_arrow_date(opentime)
  close_time = format_arrow_date(closetime)
  app.logger.debug(open_time)
  app.logger.debug(close_time)
  sbmhd ={"sb": open_time, "mhd": close_time}



  #return jsonify(result=miles * 2)
  #print (brevet)
  sbmhd = json.dumps(sbmhd)
  return jsonify(result = sbmhd)
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY HH:mm")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
