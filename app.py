import os
from random import randint
from flask import Flask, render_template, redirect, request, jsonify, session, flash, g 
from flask_debugtoolbar import DebugToolbarExtension
from wtforms.widgets.core import CheckboxInput
# import requests
from models import StocksPortfolio, db, connect_db, User, Portfolio, PortfolioUser #, StocksPortfolio
from flask_cors import CORS
from forms import UserAddForm, LoginForm, CreatePortfolioForm, AddStockForm
from sqlalchemy.exc import IntegrityError
import requests

CURR_USER_KEY = "curr_user"
ALPHA_VAN_API_KEY = 'ZM8LBVFEHBG9JWEP'

app = Flask(__name__)
CORS(app) #https://flask-cors.readthedocs.io/en/latest/
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:myPassword@localhost:5433/stocker')) 
#@ people looking at this code; you may need to change on your own computer for code to work

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints in ipython the queries being run
app.config["SECRET_KEY"] = "maxcode1" #put this in a secret file later
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

        print('*********************************')
        print(f"{session[CURR_USER_KEY]} and {g.user}")

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
        return render_template("base.html")

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

        if user: # if user succesfull created
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

            #finish the route below that lets you view the details of a portfolio
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
        
        #valididate ticker symbol
        if not check_valid_ticker(form.ticker.data):    
            flash("This ticker cannot be added (doesn't exist)", 'danger')
            return redirect(f"/portfolio/{user_id}/{portfolio_id}")

        try:
            stock_portf_link = StocksPortfolio(portfolio_id=portfolio_id, ticker=(form.ticker.data).upper())
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
        
    # ref the above portfolio/create route once youre done here

@app.route('/testapi', methods=["GET","POST"])
def test_api():

    #get ticker name from axios call from js
    data = request.get_json() #only works with axios.post?
    ticker_data = alphavantage_api_call(data['ticker']) #returns data ordered oldest to newest

    date_keys = []
    price_vals = []
    print(ticker_data)

    for k, v in ticker_data['Time Series (Daily)'].items():
        print(k, v)
        date_keys.append(k)
        price_vals.append(v['4. close'])

    date_keys.reverse()
    price_vals.reverse()

    return {
        'date_keys': date_keys,
        'price_vals': price_vals
    }
    

# https://github.com/mcodemax/Lucky_Number_Flask_2/blob/master/lucky-nums/app.py refer for api calls
def alphavantage_api_call(ticker):
    
    url = f"""https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_VAN_API_KEY}"""
    r = requests.get(url)
    
    data = r.json()

    return data
    # d.get("Time Series (Daily)") gets the daily open/close vol data

# def parse_alpha_call_data(data):


def check_valid_ticker(ticker):
    """check if symbol is valid ticker, returns True if valid"""

    response = alphavantage_api_call(ticker)

    if 'Error Message' in response.keys():
        return False
    
    return True
    
