import os
import re
from random import randint
from typing import Dict
from flask import Flask, render_template, redirect, request, jsonify, session, flash, g 
from flask_debugtoolbar import DebugToolbarExtension
from wtforms.widgets.core import CheckboxInput
# from secretcodes import ALPHA_VAN_API_KEY, SECRET_KEY #uncomment if working on Stocker locally
from models import StocksPortfolio, db, connect_db, User, Portfolio, PortfolioUser
from flask_cors import CORS
from forms import UserAddForm, LoginForm, CreatePortfolioForm, AddStockForm
from sqlalchemy.exc import IntegrityError
import requests

CURR_USER_KEY = "curr_user"
close_price_dict = {}
ALPHA_VAN_API_KEY = os.environ.get('ALPHA_VAN_API_KEY', 'nothere') #comment out deving Stocker locally

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:myPassword@localhost:5433/stocker')) 

# rest of connection code using the connection string `uri`
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
	app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #prints in ipython the queries being run
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'xxx') #change 'xxx' to SECRET_KEY   no quotes when working on Stocker locally
# https://stackoverflow.com/questions/30873189/where-should-i-place-the-secret-key-in-flask

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# db.create_all() #comment out for Heroku deployment, creates initial database

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session: # have to access database in every request; it's avoidable
        #store User in session and retrieve from session everytime instead of going to the database
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/")
def homepage():
    """Show homepage."""

    if None != g.user and g.user.id == User.query.get_or_404(session[CURR_USER_KEY]).id:
        return render_template('users/loggedin.html', user=g.user)
    else:
        return render_template("home.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user: # if user succesfully created
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')
        return redirect("/login")

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('Logged Out!', 'success')
    return redirect("/login")

@app.route('/portfolio/create', methods=["GET", "POST"])
def make_portfolio():
    """Create Portfolio"""
    
    form = CreatePortfolioForm()

    if form.validate_on_submit():
        try:
            portfolio = Portfolio(
                name=form.name.data,
                description=form.description.data,
                user_id=g.user.id)
            db.session.add(portfolio)
            db.session.commit()

            portf_user_entry = PortfolioUser(user_id=g.user.id,portfolio_id=portfolio.id)
            db.session.add(portf_user_entry)
            db.session.commit()

            return redirect(f"/portfolio/{g.user.id}/{portfolio.id}")

        except IntegrityError:
            flash("This portfolio cannot be created", 'danger')
            return redirect('/portfolio/create')
    else:
        return render_template('/portfolio/createportfolio.html', form=form)

@app.route('/portfolio/<int:user_id>/<int:portfolio_id>', methods=["GET", "POST"])
def view_own_portfolio(user_id, portfolio_id):
    """This route allows a user to view their own portfolio, and add stocks"""

    form = AddStockForm()

    # authenticate user here
    if (form.validate_on_submit() and 
        g.user.id == Portfolio.query.get_or_404(portfolio_id).user_id):
        
        portfolio_stocks = []
        # show warning only 5 stocks allowed, due to free API limits
        portfolio = StocksPortfolio.query.filter_by(portfolio_id = portfolio_id).all() 
        portfolio_size = len(portfolio)
        if(portfolio_size >= 5):
            flash("This ticker cannot be added to this portfolio; limit is 5 tickers due to API limits.", 'danger')
            return redirect(f"/portfolio/{user_id}/{portfolio_id}")

        # code below needed to see if there are duplcate tickers
        if portfolio_size > 0:
            for stock in portfolio:
                portfolio_stocks.append(stock.ticker)
        
        #prevents duplicate tickers from being added
        # broken rn; looks at all tickers available in the backend db of al portoflios
        if (form.ticker.data).upper() in portfolio_stocks:
            flash(f"Added {form.amount.data} shares of {(form.ticker.data).upper()}", 'success')

            for stock in portfolio:
                if stock.ticker == (form.ticker.data).upper():
                    stock.amount+=form.amount.data
                    db.session.commit()
            return redirect(f"/portfolio/{user_id}/{portfolio_id}")
            
        if not check_valid_ticker(form.ticker.data):    
            flash("This ticker cannot be added (doesn't exist)", 'danger')
            return redirect(f"/portfolio/{user_id}/{portfolio_id}")
            
        try:
            stock_portf_link = StocksPortfolio(portfolio_id=portfolio_id, ticker=(form.ticker.data).upper(), amount=form.amount.data)
            db.session.add(stock_portf_link)
            db.session.commit()
            return redirect(f"/portfolio/{g.user.id}/{portfolio_id}")

        except IntegrityError:
            flash("This ticker cannot be added", 'danger')
            return redirect(f"/portfolio/{user_id}/{portfolio_id}")

    else:
        # pass in form as well as the user's list of stocks in that particular portfolio
        if g.user.id == Portfolio.query.get_or_404(portfolio_id).user_id:
            portfolio = Portfolio.query.get_or_404(portfolio_id)

        return render_template('/portfolio/viewownportfolio.html', form=form, portfolio=portfolio)
        
@app.route('/portfolio/<int:portfolio_id>/<int:ticker_id>/delete', methods=["POST"])
def delete_stock(portfolio_id, ticker_id):
    """route to delete a stock on portfolio"""
    
    stock = StocksPortfolio.query.get_or_404(ticker_id)

    if g.user.id == Portfolio.query.get_or_404(portfolio_id).user_id: 
        db.session.delete(stock)
        db.session.commit()
    else:
        flash(f"You aren't allowed to delete; permission denied!", 'danger')

    return redirect(f"/portfolio/{g.user.id}/{portfolio_id}")

@app.route('/portfolio/<int:portfolio_id>/delete', methods=["POST"])
def delete_portfolio(portfolio_id):
    """route to delete a user's portfolio"""

    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if g.user.id == portfolio.user_id: 
        db.session.delete(portfolio)
        db.session.commit()
    else:
        flash(f"You aren't allowed to delete; permission denied!", 'danger')

    return redirect("/")

@app.route('/testapi', methods=["GET","POST"])
def test_api():

    #get ticker name from axios call from js
    data = request.get_json() #only works with axios.post; see parseAPIcall in script.js
    
    ticker_data = alphavantage_api_call(data['ticker']) #returns data ordered oldest to newest

    date_keys = []
    price_vals = []
    
    for k, v in ticker_data['Time Series (Daily)'].items(): 
        date_keys.append(k)
        price_vals.append(v['4. close'])

    close_price_dict[data['ticker']] = price_vals[0] 
    # stores the most recent close price in a dict
    # to calc the total portfolio val later

    date_keys.reverse()
    price_vals.reverse()

    return {
        'date_keys': date_keys,
        'price_vals': price_vals
    }

def alphavantage_api_call(ticker):
    
    url = f"""https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VAN_API_KEY}"""
    r = requests.get(url)
    
    data = r.json()

    return data
    
def check_valid_ticker(ticker):
    """check if symbol is valid ticker, returns True if valid"""

    response = alphavantage_api_call(ticker)

    if 'Error Message' in response.keys():
        return False
    
    return True    