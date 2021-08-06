# Capstone Project 1 Proposal
Name: Stocker

Developer: Maxwell Johnson
## Goals:
For this project I’ll be making a stock app that lets people select stocks and put it in different portfolios. Portfolios will track “performance”(current time price – close price or current real time price the stock is sold or portfolio is viewed) based on shares added to portfolio for each symbol. Be able to enter 2 dates and output performance for that time frame.
Target Demographics:
The user demographics will be casual/retail stock investors.
Data Needed: 
Stock ticker info and data needed from https://www.alphavantage.co/documentation/ API. Perhaps need a graphing or stock ticker dependency add-on.
# Schema Design:

![Schema Image](https://github.com/mcodemax/Stocker/blob/master/schema.png)

```
"Users"
--
id INT PK
email UNIQUE
username UNIQUE
image_url TEXT
location TEXT
password TEXT

"Portfolios"
--
id PK
name
description optional
creator_id FK >- Users.id

"Portfolio_User"
--
user_id FK >- Users.id
portfolio_id FK >- Portfolios.id

"Stocks_Portfolio"
--
ticker PK TEXT
portfolio_id FK >-< Portfolios.id
```


## Potential API Issues:
API requests for data while market is closed for real time data may return errors. API may be down sometimes.
Need to secure user’s user-profile data. No other sensitive info will be stored.
## Functionality:
Possibly make a stock scanner with certain criteria to look for in stocks.
Front page has users sign up/log-in.
When a logged in user creates a portfolio, they can make multiple portfolios.
In portfolio users can add/remove stocks/the amount of holding for each stock ticker.
A user can browse through other portfolios, but not edit them.
When in a portfolio a user will see a UI listing of 9 graphics of different stock tickers in their portfolio.
Generate a UI of stocks that show charts, and clicking on a chart displays more info on ticker.
Possibly use chart.js
## Why this app is more than CRUD:
It will have an interactive UI that shows more data by clicking on a chart.
## Stretch Goals:
Make stock charts look like actual bar charts used by financial tech/investors.

