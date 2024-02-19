"""
Module for Stock Exchange

This module provides a simple simulation of a stock market.
The main actions are:
1. Opening an Portfolio
2. Taking and closing a loan
3. Investing in a stock or Cryptocurrency
4. Computing taxes paid
5. Paying dividends
6. Closing a Portfolio

"""

import math
import datetime
import a3assets
import a3helpers

#--------------------------------------Part 1 ---------------------------------------------
def open_portfolio(to_invest,fee):
    """
    Returns: a Portfolio with cash equal to the amount invested minus the enrollment fee;
    If the enrollment fee is larger than the investment, the function returns None instead.

    Parameter to_invest: the amount of money to be invested in the account
    Precondition: to_invest is a non-negative float

    Parameter fee: the enrollment fee for opening a new Portfolio
    Precondition: fee is a non-negative float
    """
    assert type(to_invest)==float and to_invest>=0.0
    assert type(fee)==float and fee>=0.0
    if (fee>to_invest):
        return None
    else:
        return a3assets.Portfolio(to_invest-fee)

#-------------------------------------- Part 2 --------------------------------------
def invest_BitCoin(portfolio,amount):
    """
    Returns: a bool; True if the investment was successful, , False Otherwise.

    Attempts to purchase `amount` BitCoins.

    If the cost of the transaction (the
    value of the coins + the portfolio's commission fee) is greater than its cash
    on hand, this transaction fails.

    Otherwise, the portfolio receives `amount` BitCoins
    and has its cash on hand is decreased by the cost of the transaction.

    Parameter portfolio: the portfolio attempting the transaction
    Precondition: portfolio is a Portfolio object

    Parameter amount: the number of BitCoins to be purchased
    Precondition: amount is a positive int
    """
    assert type(amount)==int and amount>0
    assert isinstance(portfolio,a3assets.Portfolio)
    bitcoins=a3helpers.get_BTC_price()
    if (portfolio.cash -(bitcoins+portfolio.commission_fee  )>=0):
        portfolio.coins=amount
        portfolio.cash=portfolio.cash -(bitcoins*portfolio.coins+portfolio.commission_fee)
        return True
    else:
        return False
def sell_BitCoin(portfolio,amount):
    """
    Returns: a bool; True if the transaction was successful, False Otherwise.

    Attempts to sell `amount` BitCoins (if the account has less, than as many as the
    account has).

    The profit of of this transation is the value of the coins minus a commission fee.
    If selling would cause a negative cash balance, this transaction fails.

    Otherwise, the transaction is successful and the profit is returned to the portfolio and
    the portfolio's BitCoin balance is decreased.

    Taxes do not have to be paid for BitCoin in this application.

    Parameter portfolio: a portfolio object
    amount: amount of BitCoins to be purchased

    Precondition: portfolio is an existing portfolio object
    amount: amount is a positive int
    """
    assert type(amount)==int and amount>0
    assert isinstance(portfolio,a3assets.Portfolio)
    bitcoins=a3helpers.get_BTC_price()
    am=min(amount,portfolio.coins  )
    if (portfolio.cash +bitcoins*am-portfolio.commission_fee >=0.0):
        portfolio.coins=portfolio.coins-am
        portfolio.cash=portfolio.cash  +(bitcoins*am)-portfolio.commission_fee
        return True
    else:
        return False

#--------------------------------------Part 3 ---------------------------------------------

def compute_interest(portfolio,rate,years,times_compounded):
    """
    Returns: a float; amount of cash in portfolio after certain 'time'.

    Calculates cash in portfolio after being compounded according to formula.
    Sets cash balance equal to this  value.

    See formula later in write-up.

    Parameter portfolio: a portfolio object
    rate: % of interest gained
    years: number of years
    times_compounded: amount of times compounded per year.

    Precondition: portfolio is an existing portfolio object
    rate: a non-negative float
    years: a positive float
    times_compounded: a float > 1.0
    """
    assert type(rate)==float and rate>=0.0
    assert type(years)==float and years>0.0
    assert type(times_compounded)==float and times_compounded>1.0
    assert isinstance(portfolio,a3assets.Portfolio)
    if (times_compounded!=float("inf")):
        total=portfolio.cash  *math.pow(1+(rate/100)/times_compounded,times_compounded*years)
        portfolio.cash(total)
        return total
    else:
        total=portfolio.cash  *math.exp((rate/100)*years)
        portfolio.cash(total)
        return total
def take_loan(portfolio,amount,length):
    """
    Returns: a Loan object, or None depending on conditions below.

    If the portfolio's loan rate is greater than .2 then the portfolio is too risky;
    the loan is denied and None is returned.

    Otherwise, the portfolio receives additional cash equal to the amount of money
    in the loan. A Loan object will be created with a balance equal to the amount
    of money loaned plus interest according to the portfolio's loan rate.After this the portfolio's
    loan rate of the portfolio will be increased by .01 afterwards to account for increased risk.

    Taxes do not have to be paid on loans and there is no commission fee on this transaction.

    Parameter portfolio: the portfolio requesting the loan
    Precondition: portfolio is a Portfolio object

    Parameter amount: the amount of money requested in the loan
    Precondition: amount is a non-negative float

    Parameter length: the length in years of the Loan
    Precondition: length is a positive int
    """
    assert type(amount)==float and amount>=0.0
    assert type(length)==int and length>0.0
    assert isinstance(portfolio,a3assets.Portfolio)
    if(portfolio.loan_rate  >0.2):
        return None
    else:
        portfolio.cash=portfolio.cash  +amount
        portfolio.loan_rate=portfolio.loan_rate  +0.01
        return a3assets.Loan(amount+length*portfolio.loan_rate  *amount,length)

def pay_loan(portfolio,loan):
    """
    Returns: a bool; True if the payment was successful, False Otherwise.

    Attempts to pay off the loan by the required monthly amount.

    If successful, loan amount decreases the amount paid off, and the loan length is
    decreased by one.

    If there is not enough money to pay off the monthly amount,
    the balance of the loan increases by its late_fee, and the portfolio's cash remains the same.

    Once a loan is fully paid off, then the portfolio's loan_rate is decreased by 0.01.

    Parameter portfolio: the portfolio paying off its loan
    Precondition: portfolio is a Portfolio object

    Parameter loan: the loan to be paid off
    Precondition: loan is a Loan object
    """
    assert isinstance(portfolio,a3assets.Portfolio)
    assert isinstance(loan,a3assets.Loan)
    if (portfolio.cash  <loan.balance  /loan.length  ):
        loan.balance(loan.balance  +loan.late_fee  )
        return False
    else:
        if (loan.length  ==1):
            portfolio.loan_rate(portfolio.loan_rate  -0.01)
        portfolio.cash(portfolio.cash  -loan.balance  /loan.length  )
        loan.balance(loan.balance  -loan.balance  /loan.length  )
        loan.length(loan.length  -1)
        return True



#-------------------------------------- Part 4 --------------------------------------
def calculate_taxes(profit,long_term):
    """
    Returns: a float representing profit after tax rate applied

    If profit is long-term, pays capital-gains taxes according to write-up
    If profit is not long-term, pays income intrest according to write-up

    Parameter profit: a float representing total profit
    long_term: bool representing if long term or short term investment.

    Precondition: portfolio is an existing portfolio object
    profit: a float
    long_term: a bool
    """
    assert type(long_term)==bool
    assert type(profit)==float
    temp_tax=0
    if (long_term!=True):
        if (profit<=10000):
            temp_tax=0.1*profit
            return profit-temp_tax
        elif (profit<=100000):
            temp_tax=0.1*10000+0.2*(profit-10000)
            return profit-temp_tax
        elif (profit<=1000000):
            temp_tax=0.1*10000+0.2*90000+0.3*(profit-100000)
            return profit-temp_tax
        elif (profit<=10000000):
            temp_tax=0.1*10000+0.2*90000+0.3*900000+0.4*(profit-1000000)
            return profit-temp_tax
        else:
            temp_tax=0.1*10000+0.2*90000+0.3*900000+0.4*9000000+0.7*(profit-10000000)
            return profit-temp_tax
    else:
        if (profit<=38600):
            temp_tax=0
            return profit-temp_tax
        elif (profit<=425800):
            temp_tax=0.15*(profit-38600)
            return profit-temp_tax
        else:
            temp_tax=0.15*(387200)+0.3*(profit-425800)
            return profit-temp_tax


def buy_stock(portfolio,stock,amount_shares,short,time):
    """
    Returns: a Stock object

    This function does the following things
    1. Gets cost of transaction which is current price of stock purchased + the portfolio's commission fee
    2. If the cost is less than cash on hand and the transaction occurs between 8 am and 4 pm on a weekday
    a stock object is created.
    3. If not possible None is returned.

    Parameter portfolio: a portfolio object
    stock: a str representing the stock trading symbol of the company
    amount_shares: a int representing how many shares to buy
    short: a bool representing if stock is "shorted" (see later description)
    time: a datetime object representing the time of transaction

    Precondition: portfolio is an existing portfolio object
    stock: a str representing the symbol of a company. (We will not give a nonsense str)
    amount_shares: is a positive int.
    short: a bool
    time: a time object
    """
    assert type(stock)==str
    assert type(amount_shares)==int and amount_shares>0
    assert type(short)==bool
    assert isinstance(portfolio,a3assets.Portfolio)

    sprice=a3helpers.get_stock_price(stock)
    portfolio.commission_fee
    if(sprice*amount_shares+portfolio.commission_fee  <=portfolio.cash  ):
        if(a3helpers.is_weekday(time) and time.hour>=10 and time.hour<16):
            portfolio.cash=portfolio.cash  -sprice*amount_shares-portfolio.commission_fee
            st=Stock(stock,sprice,amount_shares,short,time)
            return st
    return None
def pay_dividends(portfolio,stock,company,payments):
    """
    Returns: a bool;  True if the transaction was successful, False Otherwise.
    Pays dividends to the investors.
    After paying short-term taxes the money is deposited in the user's profolio

    Parameter portfolio: a portfolio object
    company: a str representing the trading symbol of the company that is paying dividends
    payments: The amount per share that each owner gets
    stock: the stock to be owned

    Precondition: portfolio is an existing portfolio object
    company: str
    payments: a non-negative float
    stock: a stock object
    """
    assert isinstance(portfolio,a3assets.Portfolio)
    assert isinstance(stock,a3assets.Stock)
    assert type(company)==str
    assert type(payments)==float and payments>=0.0
    if(stock.company  ==company):
        profit=payments*stock.shares
        posttax=calculate_taxes(profit,False)
        portfolio.cash=portfolio.cash  +posttax
        return True
    return False

def sell_stock(portfolio,amount_shares,time,stock):
    """
    Returns: a bool; True if transaction was successful, False Otherwise.

    Attempts to sell `amount_shares` of stock (if the account has less, than as many as the
    account has).

    The profit is defined to as follows.
    If the stock was shorted: The profit is equal to twice the buy price - the sell price
    If the stock was not shorted: The profit is equal to twice the sell price - the buy price

    Tax must paid under the followering rules:
    1. If there is negative profit. No taxes are paid
    2. If the original stock was bought more than a year before [time], then capital gains tax must be paid
    3. If the original stock was less than a year before [time], then regular income tax must be paid.

    If the Transaction is successful, then the post-tax profit is returned to the portfolio's cash account,
    and the stock's shares are decreased.

    NOTE: A Transaction fails when
        1. The transaction occurs outside the hours of 8 am and 4 pm on a weekday (if not it fails).
        2. There is not enough money to pay the commission fee

    Parameter portfolio: a portfolio object
    amount_shares: a int representing how many shares of stock to sell
    payments: The amount per share that each owner gets
    time: a datetime object representing the time of transaction
    stock: a stock object reporeseting the stock to be sold

    Precondition: portfolio is an existing portfolio object
    stock: a str representing the symbol of a company. (We will not give a nonsense str)
    amount_shares: is a positive int.
    time: a time object
    stock: stock: a stock object
    """
    assert isinstance(portfolio,a3assets.Portfolio)
    assert isinstance(stock,a3assets.Stock)
    assert isinstance(time,datetime.datetime)
    assert type(amount_shares)==int and amount_shares>0
    if(a3helpers.is_weekday(time) and time.hour>=10 and time.hour<16 and portfolio.cash  >=portfolio.commission_fee  ):
        sharestosell=min(stock.shares,amount_shares)
        if (stock.short  ):
            profit=sharestosell*2*(stock.buy_price  -a3helpers.get_stock_price(stock.company  ))
        else:
            profit=sharestosell*2*(a3helpers.get_stock_price(stock.company  )-stock.buy_price  )
        stock.shares=stock.shares -sharestosell
        if (profit<=0):
            profitaftertax=0
        else:
            if(a3helpers.one_year_ago(time)>stock.buy_date  ):
                profitaftertax=calculate_taxes(profit,True)
            else:
                profitaftertax=calculate_taxes(profit,False)
        portfolio.cash=portfolio.cash  -portfolio.commission_fee  +profitaftertax
        return True
    return False

def game() :
    start = float(input("How much money would you like to start with? "))
    portfolio = open_portfolio(start,1.0)
    game = True
    while game:
        print("\nYou have a cash balance of $" + str(round(portfolio.cash,2)))
        intro = "Would you like to...... (Type the number of the action you would like to do)" + \
                "\n Press 1 if you want Buy Bitcoins" + \
                "\n Press 2 if you want Sell Bitcoins" + \
                "\n Press 3 if you want Take out a Loan" + \
                "\n Press 4 if you want Buy Stock" + \
                "\n Press 5 if you want Sell Bitcoins" +\
                "\n Press 6 if you want Quit" +\
                "\n Enter: "
        move = input(intro)
        move = int(move)
        if move == 1:
            print("The current prince of BitCoins is $" + str(a3helpers.get_BTC_price()  ))
            amount = int(input("How many BitCoins would you like to buy? "))
            success = invest_BitCoin(portfolio,amount)
            if success:
                print("You now have a BitCoin balance of " + str(portfolio.coins))
                print("They are worth $" + str(portfolio.coins * a3helpers.get_BTC_price()  ))
            else:
                print("I am sorry you do not have enough money for this transaction ")
        elif move == 2:
            print("The current prince of BitCoins is $" + str(a3helpers.get_BTC_price()  ))
            amount = int(input("How many BitCoins would you like to sell? "))
            success = sell_BitCoin(portfolio,int(amount))
            if success:
                print("You now have a BitCoin balance of " + str(portfolio.coins))
                print("They are worth $" + str(portfolio.coins * a3helpers.get_BTC_price()  ))
            else:
                print("I am sorry you do not have enough money for this transaction")
        elif move == 3:
            amount = float(input("How much money would you like to take out for your loan? "))
            length = int(input("How long do you want to have it out for? "))
            loan = take_loan(portfolio,amount,length)
            if loan != None:
                print("You now have a loan with a balance of " + str(loan.balance))
                print("Your cash balance is now " + str(portfolio.cash))
                portfolio.loans.append(loan)
            else:
                print("I am sorry this transaction failed")
        elif move == 4:
            ticker = input("What stock would you like to buy? ")
            print(ticker + " is currently worth " + str(a3helpers.get_stock_price(ticker)))
            shares = int(input("How many shares would you like to buy? "))
            short = input("Would you like to short this stock Y/N? ")
            if short == "Y":
                short = True
            else:
                short = False
            date = datetime.datetime.now()
            stock = buy_stock(portfolio,ticker,shares,short,date)
            if stock != None:
                print("Transation successful!")
                portfolio.stocks.append(stock)
            else:
                print("I am sorry this transaction failed")
        elif move == 5:
            ticker = input("What stock would you like to sell?")
            print(ticker + " is currently worth " + str(a3helpers.get_stock_price(ticker)))
            amount = -1
            selling = None
            for stock in portfolio.stocks:
                if stock.company == ticker and stock.shares > amount:
                    selling = stock
            if amount == -1:
                continue
            shares = int(input("How many shares would you like to buy?"))
            date = datetime.datetime.now()
            success = sell_stock(portfolio,shares,time,selling)
            if success:
                print("Transation successful!")
                print("You now have a balance of " + str(portfolio.cash))
            else:
                print("I am sorry this transaction failed")
        elif move == 6:
            print("\nYou have a cash balance of " + str(portfolio.cash))
            print("\nThanks! ")
            game = False
        else:
            print("Key Stroke not recognized")

game()
