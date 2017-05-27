import pymysql
import database
from datetime import date, time, datetime


class Account:
    def __init__(self,acc_no=None,acc_type=None,acc_balance=0,acc_credit=0):
        #acc_no - Account Number (for Bank Reference)
        #acc_type - Account Type (Cash,Saving,Current,Credit)
        #acc_balance - Balance of this account
        #acc_credit - Credit Limit
        self._acc_no = acc_no
        self._acc_type = acc_type
        self._acc_balance = acc_balance
        self._acc_credit = acc_credit

    @property
    def acc_no(self):
        return self._acc_no

    @acc_no.setter
    def acc_no(self, value):
        self._acc_no = value

    @property
    def acc_type(self):
        return self._acc_type

    @acc_type.setter
    def acc_type(self, value):
        self._acc_type = value

    @property
    def acc_balance(self):
        return self._acc_balance

    @acc_balance.setter
    def acc_balance(self, value):
        self._acc_balance = value

    @property
    def acc_credit(self):
        return self._acc_credit

    @acc_credit.setter
    def acc_credit(self, value):
        self._acc_credit = value

    def __str__(self):
        return self._acc_balance


class Saving_Account(Account):
    def __init__(self,acc_no=None,acc_type='Saving',acc_balance=0,acc_credit=0):
        super().__init__(acc_no,acc_type,acc_balance,acc_credit)


    def withdraw(self,value):
        if self._acc_balance >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def deposit(self,value):
        self._acc_balance += value
        return True

    def transfer_from(self,value):
        if self._acc_balance >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def transfer_to(self,value):
        self._acc_balance += value
        return True


class Credit_Account(Account):
    def __init__(self, acc_no=None, acc_type='Credit', acc_balance=0, acc_credit=0):
        super().__init__(acc_no, acc_type, acc_balance, acc_credit)

    def withdraw(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def deposit(self,value):
        self._acc_balance += value
        return True

    def transfer_from(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def transfer_to(self,value):
        self._acc_balance += value
        return True

    def payment_by_credit(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False


class Cash_Account(Account):
    def __init__(self, acc_no='Cash', acc_type='Cash', acc_balance=0, acc_credit=0):
        super().__init__(acc_no, acc_type, acc_balance, acc_credit)

    def deposit(self,value):
        self._acc_balance += value
        return True

    def withdraw(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False


class Income_Account(Account):
    def __init__(self, acc_no='Income', acc_type='Income', acc_balance=0, acc_credit=0):
        super().__init__(acc_no, acc_type, acc_balance, acc_credit)

    def income_log(self,value):
        self._acc_balance += value
        return True


class Shop_Account(Account):
    def __init__(self, acc_no='Shop', acc_type='Shop', acc_balance=0, acc_credit=0):
        super().__init__(acc_no, acc_type, acc_balance, acc_credit)

    def shop_log(self,value):
        self._acc_balance += value
        return True

