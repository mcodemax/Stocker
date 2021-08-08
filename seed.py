

from models import User, Portfolio, PortfolioUser, StocksPortfolio
from app import db

db.drop_all()
db.create_all()