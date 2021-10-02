"""App route tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_app_views.py

import os
from unittest import TestCase
from models import StocksPortfolio, db, connect_db, User, Portfolio, PortfolioUser


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:myPassword@localhost:5433/stocker_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class AppRoutes(TestCase):
    """Test userviews."""


    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.register(
                first_name='First',
                last_name='Last',
                username='Username1',
                password='passy1',
                email='email@email.com',
                image_url = User.image_url.default.arg,
            )
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_logged_in_page(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
               
            resp = c.get("/")

            self.assertIn("Hello First", str(resp.data))

    def test_portfolio_creation(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post(f"/portfolio/create", data={
                'name': 'Stonksy',
                'description': 'Memes'
            }, follow_redirects=True)
            self.assertIn("Stonksy", str(resp.data))
            
    def test_stock_addition(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
        
            c.post(f"/portfolio/create", data={
                    'name': 'Stonksy',
                    'description': 'Memes'
                }, follow_redirects=True)

            portfolio = Portfolio.query.filter(Portfolio.name == 'Stonksy').first()

            #ensures we get to portfolio detail page
            resp = c.get(f"/portfolio/{self.testuser.id}/{portfolio.id}")
            self.assertIn("Memes", str(resp.data))

            #ensures stock added
            resp = c.post(f"/portfolio/{self.testuser.id}/{portfolio.id}", data={
                'ticker': 'NVDA',
                'amount': 50
            }, follow_redirects=True)
            self.assertIn("NVDA", str(resp.data))

        