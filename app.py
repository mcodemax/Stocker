from os import error
from random import randint
from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
# import requests
from models import db, connect_db, User, Portfolio, PortfolioUser, StocksPortfolio
from flask_cors import CORS
# from forms import 


app = Flask(__name__)
CORS(app) #https://flask-cors.readthedocs.io/en/latest/
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5433/feedback' 
#@ people looking at this code; you may need to change on your own computer for code to work

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints in ipython the queries being run
app.config["SECRET_KEY"] = "maxcode1" #put this in a secret file later
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")