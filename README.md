# Stocker

###### Developer: Maxwell Johnson

[Link to Stocker](https://herokuapphere/) 

Description: A website where users can create a portfolio up to 5 stocks and calculate the near realtime value of their portfolio holdings. Users can view daily chart price history of stock holding in their portfolio. Disclaimer: Due to free API limits from AlphaVantage App performs best is waiting 30-60s before viewing portfolios and altering them.

### Features:
- **Create multiple portfolios and see total value**: Users can create multiple portfolios and see the total holding value of each one.
- **View Realtime Snapshot**: When users add holding to portfolio they see the value of that ticker and total current portfolio holdings at that exact point in time.
    
### Basic user flow:
1. User must create a Stocker account to use Stocker. 
2. After registering, users can create portfolios.
3. Following portfolio creation users can add holdings to portfolios and see real snapshot data of their holdings at time of ticker addition to portfolio.
4. Due to free API limits from AlphaVantage App performs best is waiting 30-60s before viewing portfolios and altering them.
5. Users are limited to 5 different ticker holdings per portfolio.

### APIs used: 
1. Alpha Vantage:
    - Root URL: https://www.alphavantage.co/
    - [Docs](https://www.alphavantage.co/documentation/)
2. ChartJs:
    - Root URL: https://www.chartjs.org/
    - [Docs](https://www.chartjs.org/docs/latest/)
    
### Tech stack:
- Front-end: HTML, CSS, JS, jQuery, Axios, Bootstrap, Font Awesome
- Backend: Python, Flask, WTForms, requests, Bcrypt
- Database: SQLAlchemy
- Deployment: Heroku

To access required tools, run the following in terminal:

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

Then run the server by typing `flask run`

**The code in this repo is written specifically for deployment purposes. In order to interact with the code locally on your machine, you must do the following:**
1. Create a file `secret_codes.py` and define the `ALPHA_VAN_API_KEY` and `SECRET_KEY` variables according to your own dev environment.
    - Add to `.gitignore` file
2. Uncomment out secretcodes import in app.py
3. change xxx to SECRET_KEY in line 30 of app.py ... where it says app.config['SECRET_KEY']
4. change ALPHA_VAN_API_KEY const declaration line in app.py

### Possible features to add:
- **Store Internal Data of prev requested tickers**: To work around free API limits from Alpha Vantage possibly store previously requested ticker data in server.
- **Allow Users to View others Portfolios and Compare Portfolios**
- **Contribute to Stocker**: Stocker is open-source; users can contribute to increase Stocker's capabilities.



