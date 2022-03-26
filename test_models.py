"""App route tests."""

# run these tests like:
#    FLASK_ENV=production python -m unittest test_models.py

import os
from unittest import TestCase
from models import StocksPortfolio, db, connect_db, User, Portfolio, PortfolioUser, DEFAULT_USER_IMG

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

class TestModels(TestCase):
    "Test Models"

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.register(
                first_name='First',
                last_name='Last',
                username='Username1',
                password='passy1',
                email='email@email.com',
                image_url = User.image_url.default.arg,
            )

        db.session.commit()

        port1 = Portfolio(
                    name = 'Portfolio1',
                    description = 'A portfolio.',
                    user_id = u1.id
                )
        
        db.session.add(port1)
        db.session.commit()

        self.u1 = u1        

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does registering user model work? Does password work?"""

        u = User.register(
                first_name='Bob',
                last_name='Bradley',
                username='Username7',
                password='passy7',
                email='email7@email.com',
            )

        db.session.commit()

        # User should have no portfolios, and have info above
        self.assertEqual(u.first_name, 'Bob')
        self.assertEqual(u.last_name, 'Bradley')
        self.assertEqual(u.username, 'Username7')
        self.assertEqual(u.email, 'email7@email.com')
        self.assertEqual(u.image_url, DEFAULT_USER_IMG)

        # test authentication
        self.assertTrue(User.authenticate('Username7', 'passy7'))


    def test_portfolio_creation(self):
        """Test if portfolio creation works"""

        test_portfolio = Portfolio(
                    name = 'Portfolio_Test',
                    description = 'Another portfolio.',
                    user_id = self.u1.id
                )

        db.session.add(test_portfolio)
        db.session.commit()

        self.assertEqual(test_portfolio.name, 'Portfolio_Test')
        self.assertEqual(test_portfolio.description, 'Another portfolio.')


    def test_add_stocks(self):
        "Test if stocks can be added to portfolio"

        test_portfolio = Portfolio.query.get(self.u1.id)

        ticker = StocksPortfolio(
            portfolio_id = test_portfolio.id,
            ticker = 'NVDA',
            amount = 55
            )

        db.session.add(ticker)
        db.session.commit()

        self.assertEqual(ticker.ticker, 'NVDA')
        self.assertEqual(ticker.amount, 55)
    