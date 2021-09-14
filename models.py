"""Models for User"""

from flask_bcrypt import Bcrypt
from flask_cors.core import DEFAULT_OPTIONS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

MAX_USERNAME_LEN = 20
MAX_NAME_LEN = 30
MAX_EMAIL_LEN = 50
MAX_NOTE_LEN = 5000
MAX_TITLE_LEN = 100
DEFAULT_USER_IMG = 'https://i.redd.it/c9lg95srmj521.png'


class User(db.Model):
    """Users."""

    __tablename__ = "users"

    def __repr__(self):
        return f"""<id={self.id} username={self.username} password={self.password} email={self.email} first_name={self.first_name}
                last_name={self.last_name} image={self.image_url}>"""

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates between python and postgreSQL
                    primary_key=True,
                    autoincrement=True)
    
    username = db.Column(db.String(MAX_USERNAME_LEN),
                            unique=True,
                            nullable=False)
    
    password = db.Column(db.String(), 
                            nullable=False)

    email = db.Column(db.String(MAX_EMAIL_LEN),  #maybe import email or use email from documentation? or no; dependencies might break
                            nullable=False)

    first_name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)


    last_name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)
    
    image_url = db.Column(db.String(MAX_NOTE_LEN), 
                        nullable=False,
                        default=DEFAULT_USER_IMG)

    portfolios = db.relationship("Portfolio", backref="user") #don't cascade delete these b/c other users can view other porfolios

    # feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")
    #def function to salt/encrpyt password
    
    # still needs to be fixed
    @classmethod
    def register(cls, username, password, email, first_name, last_name, image_url=DEFAULT_USER_IMG):

        user = User(username=username,
                    password=bcrypt.generate_password_hash(password).decode('UTF-8'),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)

        db.session.add(user)

        return user

    #still needs to be fixed
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate User existence and correct password"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Portfolio(db.Model):
    """Porfolio."""

    __tablename__ = "portfolios"

    def __repr__(self):
        return f"""<name={self.name}>"""


    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)

    description = db.Column(db.String(MAX_NOTE_LEN),
                        nullable=False)

    profit = db.Column(db.Float,
                        default=0)

    # tells what user made this portfolio
    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id"),
                    #    primary_key=True #uncommenting this line breaks schema; ask
                       )

    stocks = db.relationship("StocksPortfolio", backref="portfolio", cascade="all, delete-orphan")           

class PortfolioUser(db.Model):
    """Mapping of Portfolio to Users that are monitoring it, not necessarily created it"""

    __tablename__ = "portfolios_users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id", ondelete="cascade"))
                       # primary_key=True) #not needed as primary key for this table

    portfolio_id = db.Column(db.Integer,  #having user_id FK in the Portfolio class above breaks the schema(if you leave primary_key=True in that particular part of the mentioned class)
                       db.ForeignKey("portfolios.id", ondelete="cascade"))
                       # primary_key=True) #not needed as primary key for this table


class StocksPortfolio(db.Model):
    """Mapping of Stocks to a Portfolio."""

    __tablename__ = "stocks_portfolios"

    def __repr__(self):
        return f"<id={self.id} portfolio_id={self.portfolio_id} ticker={self.ticker}>"

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)

    portfolio_id = db.Column(db.Integer,    #having user_id FK in the Portfolio class above breaks the schema(if you leave primary_key=True in that particular part of the mentioned class)
                       db.ForeignKey("portfolios.id"))

                       #primary_key=True) removed; not needed as primary key
                       #issue with sqlalchemy, models, viewownportfolio.html, delete_stock route
                       # don't have two primary keys
                       #https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
                       #see above on compound primary keys

    ticker = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)

    # implement later:
    # amount = db.Column(db.Integer, nullable=False,
                        # default=1)