from os import error
from typing import Dict
from random import randint
from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "maxcode1" #put this in a secret file later
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")