import requests
import datetime
import random

key = "TEST"

def is_weekday(time):
    """
    Returns: True if it time lands on a weekday, False if it is a weekend
    time: a datetime object 

    In python, 0 represents Monday... 5 represents Saturday and 6 represents Sunday.
    """
    return time.weekday() < 5

def one_year_ago(time):
    """
    Returns: A new datetime object one year back from time. 
    time: a datetime object 
    """
    return time.replace(time.year-1)

def get_stock_price(stock):
    """
    Returns: current price of stock as a float

    IF Key == Test returns constant value used for testing 

    stock: a string representing a company's stock tranding symbol 
    """
    if key == "TEST":
        if stock == "CORNELL":
            return 18.65
        if stock == "HARVARD":
            return 0.0
        else:
            return 1.0
    try:
        stock = stock.upper()
        req = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + stock + "&apikey=" + key
        response = requests.get(req).text
        price = response[(response).find("price")+len("price")+4:]
        price = price[:price.find("\"")]
        return float(price)
    except:
        return random.random() * 100

def get_BTC_price():
    """
    Returns: current price of BitCoin as a float

    IF Key == Test returns constant value used for testing 
    """
    if key == "TEST":
        return 18.65
    try:
        req = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=" + key
        response = requests.get(req).text
        price = response[(response).find("5. Exchange Rate")+20:]
        price = price[:price.find(",")-1]
        return float(price)
    except:
        return random.random() * 100