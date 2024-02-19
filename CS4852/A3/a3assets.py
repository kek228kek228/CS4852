"""
Helper Functions + Classes for A3. (equivalent of introcs from old A3)

"""

import math
import datetime

class Portfolio(object):
    """
    The class Portfolio is the type of object that represents a person's account. It has 5 attributes.
        cash - An float representing how much cash is in the account; non-negative
        commission_fee - A float that represents for each transaction how much does it cost for that transaction to occur; non-negative
        loan_rate - A float that represents when taking out a loan how much interest will be owed; non-negative
        stock - Any stock objects that the person will reside here.
        coins - a int representing how many BitCoins are owned; non-negative

    The constructor can be called like this
    Portfolio(100.0)
    Which opens a new Portfolio with $100.0 in it.
    """
    @property
    def cash(self):
        """
        The amount of cash that the account contains.

        **Invariant**: Value must be a non-negative float.
        """
        return self._cash

    @cash.setter
    def cash(self,value):
        assert type(value) == float, 'f{value} is not a float'
        assert value >= 0, 'f{value} must not be negative'
        self._cash = value

    @property
    def commission_fee(self):
        """
        The amount of money it costs to make a transaction; this is subtracted every time
        a transaction occurs.

        **Invariant**: Value must be a non-negative float.
        """
        return self._commission_fee

    @commission_fee.setter
    def commission_fee(self,value):
        assert type(value) == float, f'{value} is not a float'
        assert value >= 0, f'{value} must not be negative'
        self._commission_fee = value

    @property
    def loan_rate(self):
        """
        The interest rate on any loans taken out for the account.

        **Invariant**: Value must be a non-negative float.
        """
        return self._loan_rate

    @loan_rate.setter
    def loan_rate(self,value):
        assert type(value) == float, f'{value} is not a float'
        assert value >= 0, f'{value} must not be negative'
        self._loan_rate = value

    @property
    def stocks(self):
        """
        The list of stocks that this Portfolio owns.

        **Invariant**: Value must be a List or None.
        """
        return self._stocks

    @stocks.setter
    def stocks(self,value):
        assert value is None or isinstance(value, list), f'{value} must be List or None'
        self._stocks = value

    @property
    def loans(self):
        """
        The list of loans that this Portfolio owes.

        **Invariant**: Value must be a List or None.
        """
        return self._loans

    @stocks.setter
    def loans(self,value):
        assert value is None or isinstance(value, list), f'{value} must be List or None'
        self._loans = value

    @property
    def coins(self):
        """
        The amount of BitCoin owned by this Portfolio.

        **Invariant**: Value must be a non-negative int.
        """
        return self._coins

    @coins.setter
    def coins(self,value):
        assert type(value) == int, f'{value} is not an int'
        assert value >= 0, f'{value} must not be negative'
        self._coins = value

    def __init__(self,c):
        """
        :param c: initial cash value
        :type c:  ``float`` >=0
        """
        self.cash = c
        self.commission_fee = 1.0
        self.loan_rate = .1
        self.stocks = []
        self.loans = []
        self.coins = 0


class Loan(object):
    """
    The class Loan is the type of object that represents a person's loan. It has 3 attributes.
        balance - A float representing how much cash is owed still; non-negative
        length - A int representing how many months the loan still has to be paid out; non-negative
        late_fee - A float that represents how much the user will incur when payment can not be made; non-negative

    A user has to pay balance/length every month a payment is due or a late_fee will be incurred.

    The constructor can be called like this
    Loan(200.0,10)
    Which creates a $200.0 Loan that has to be paid in every month for 10 months
    """
    @property
    def balance(self):
        """
        The amount of balance that must be repaid for the Loan.

        **Invariant**: Value must be a non-negative float.
        """
        return self._balance

    @balance.setter
    def balance(self,value):
        assert type(value) == float, f'{value} is not a float'
        assert value >= 0, f'{value} must not be negative'
        self._balance = value

    @property
    def length(self):
        """
        The amount of months remaining in the Loan.

        **Invariant**: Value must be a non-negative int.
        """
        return self._length

    @length.setter
    def length(self,value):
        assert type(value) == int, f'{value} is not an int'
        assert value >= 0, f'{value} must not be negative'
        self._length = value

    @property
    def late_fee(self):
        """
        The monthly penalty for failing to make the required payment, which is
        calculated through `balance` / `length`.

        **Invariant**: Value must be a non-negative float.
        """
        return self._late_fee

    @late_fee.setter
    def late_fee(self,value):
        assert type(value) == float, f'{value} is not a float'
        assert value >= 0, f'{value} must not be negative'
        self._late_fee = value

    def __init__(self,m,l):
        """
        :param m: initial balance owed value
        :type m:  ``float`` >=0

        :param l: initial length value
        :type l:  ``int`` >=0
        """
        self.balance = m
        self.length = l
        self.late_fee = 100.0


class Stock(object):
    """
    The class Stock is the type of object that represents one stock transaction. It has 5 attributes.
        company - A string representing the stock symbol of the trading company
        shares - A int representing how many shares of the company the person owns
        buy_price - A float that represents how much the shares are worth at last update
        buy_date - A DateTime object representing date of purchase of stock
        short - A boolean representing if the stock was shorted or not. True means it was shorted


    """
    @property
    def company(self):
        """
        The ticker symbol of the company this Stock belongs to.

        **Invariant**: Value must be a non-empty str.
        """
        return self._company

    @company.setter
    def company(self,value):
        assert type(value) == str, f'{value} is not a str'
        assert len(value) != 0, 'Company name must not be empty'
        self._company = value

    @property
    def shares(self):
        """
        The amount of shares of the company this Stock represents are owned.

        **Invariant**: Value must be a non-negative int.
        """
        return self._shares

    @shares.setter
    def shares(self,value):
        assert type(value) == int, f'{value} is not an int'
        assert value >= 0, f'{value} must not be negative'
        self._shares = value

    @property
    def buy_price(self):
        """
        The current value of a share of this Stock.

        **Invariant**: Value must be a non-negative float.
        """
        return self._buy_price

    @buy_price.setter
    def buy_price(self,value):
        assert type(value) == float, f'{value} is not a float'
        assert value >= 0, f'{value} must not be negative'
        self._buy_price = value

    @property
    def buy_date(self):
        """
        The purchase time of this stock.

        **Invariant**: Value must be a datetime object.
        """
        return self._buy_date

    @buy_date.setter
    def buy_date(self,value):
        assert isinstance(value,datetime.datetime) , f'{value} is not a datetime object'
        self._buy_date = value

    @property
    def short(self):
        """
        Whether or not the Stock is shorted. True if shorted.

        **Invariant**: Value must be a bool.
        """
        return self._short

    @short.setter
    def short(self,value):
        assert type(value) == bool, f'{value} is not a bool'
        self._short = value

    def __init__(self,c,b,sa,so,t):
        """
        :param c: initial company ticker value
        :type c:  str, len(c) > 0

        :param b: initial buy_price value
        :type b:  ``float`` >=0

        :param sa: initial shares
        :type sa:  ``int`` >=0

        :param so: initial short value
        :type so:  ``bool``

        :param t: initial datetime value
        :type t:  ``datetime``
        """
        self.company = c
        self.buy_price = b
        self.shares = sa
        self.short = so
        self.buy_date = t
