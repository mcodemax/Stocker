"""Models for User"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


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



class User(db.Model):
    """Users."""

    __tablename__ = "users"

    def __repr__(self):
        return f"""<id={self.id} username={self.username} password={self.password} email={self.email} first_name={self.first_name}
                last_name={self.last_name} image={self.image}>"""

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates between python and postgreSQL
                    primary_key=True,
                    autoincrement=True)
    
    username = db.Column(db.String(MAX_USERNAME_LEN),
                            unique=True,
                            primary_key=True,
                            nullable=False)
    
    password = db.Column(db.String(), 
                            nullable=False)

    email = db.Column(db.String(MAX_EMAIL_LEN),  #maybe import email or use email from documentation? or no; dependencies might break
                            nullable=False)

    first_name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)


    last_name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)
    
    image = db.Column(db.String(MAX_NOTE_LEN), 
                        nullable=False,
                        default='https://i.redd.it/c9lg95srmj521.png')

    # feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")
    #def function to salt/encrpyt password
    
    # still needs to be fixed
    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        user = User(username=username,
                    password=bcrypt.generate_password_hash(password).decode("utf8"),
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

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

    #def serialize_cupcake(self):
        # """serialize cupcakes"""
        
        # return {
        #     "id": self.id,
        #     "flavor": self.flavor,
        #     "size": self.size,
        #     "rating": self.rating,
        #     "image" : self.image
        # }

class PortfolioUser(db.Model):
    """Mapping of Portfolio to Users that are monitoring it, not necessarily created it"""

    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id"),
                       primary_key=True)

    portfolio_id = db.Column(db.Integer,
                       db.ForeignKey("portfolios.id"),
                       primary_key=True)                    


class Portfolio(db.Model):
    """Porfolio."""

    __tablename__ = "portfolios"

    def __repr__(self):
        return f"""<feedback id={self.id} title={self.title} content={self.content} username={self.username}>"""


    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)

    description = db.Column(db.String(MAX_NOTE_LEN),
                        nullable=False)

    # tells what user made this portfolio
    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id"),
                       primary_key=True)

    
class StocksPortfolio(db.Model):
    """Mapping of Stocks to a Portfolio."""

    __tablename__ = "stocks_portfolios"

    def __repr__(self):
        return f"<id={self.id} portfolio_id={self.portfolio_id} ticker={self.ticker}>"

    id = db.Column(db.Integer, # int not the same as SQL Integer, the ORM translates etween python and postgreSQL
                    primary_key=True,
                    autoincrement=True)

    portfolio_id = db.Column(db.Integer,
                       db.ForeignKey("portfolios.id"),
                       primary_key=True)

    ticker = db.Column(db.String(MAX_NAME_LEN),
                        nullable=False)