import pymysql
import database
from datetime import date, time, datetime


def db_read_records():
    db = pymysql.connect("localhost", "root", "secret", "finance_db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM accountdb")
    result = cursor.fetchall()
    for r in result:
        print(r)
    db.close()


class Account:
    def __init__(
            self,acc_id=None,acc_provider=None,acc_no=None,acc_name=None,
            acc_type=None,acc_create_datetime=None,acc_status=None,
            acc_credit=None,acc_balance=None):
        #acc_id - Running Number
        #acc_provider - Bank, Finace or Cash Pocket
        #acc_no - Account Number (for Bank Reference)
        #acc_name - Account Owner
        #acc_type - Account Type (Cash,Saving,Current,Credit)
        #acc_create_date - Date of Account Created
        #acc_status - Account Status (Active, Disable, Closed)
        #acc_balance - Balance of this account

        self._acc_id = acc_id
        self._acc_provider = acc_provider
        self._acc_no = acc_no
        self._acc_name = acc_name
        self._acc_type = acc_type
        self._acc_create_datetime = acc_create_datetime
        self._acc_status = acc_status
        self._acc_credit = acc_credit
        self._acc_balance = acc_balance

    @property
    def acc_id(self):
        return self._acc_id

    @acc_id.setter
    def acc_id(self,value):
        self._acc_id = value


    @property
    def acc_provider(self):
        return self._acc_provider

    @acc_provider.setter
    def acc_provider(self, value):
        self._acc_provider = value

    @property
    def acc_no(self):
        return self._acc_no

    @acc_no.setter
    def acc_no(self, value):
        self._acc_no = value

    @property
    def acc_name(self):
        return self._acc_name

    @acc_name.setter
    def acc_name(self, value):
        self._acc_name = value

    @property
    def acc_type(self):
        return self._acc_type

    @acc_type.setter
    def acc_type(self, value):
        self._acc_type = value

    @property
    def acc_create_date(self):
        return self._acc_create_date

    @acc_create_date.setter
    def acc_create_date(self, value):
        self._acc_create_date = value

    @property
    def acc_status(self):
        return self._acc_status

    @acc_status.setter
    def acc_status(self, value):
        self._acc_status = value

    @property
    def acc_credit(self):
        return self._acc_credit

    @acc_credit.setter
    def acc_credit(self, value):
        self._acc_credit = value

    @property
    def acc_balance(self):
        return self._acc_balance

    @acc_balance.setter
    def acc_balance(self, value):
        self._acc_balance = value

    @staticmethod
    def check_today(self):
        return date.today().strftime("%y-%m-%d")

    def acc_day(self):
        return datetime.strptime(self._acc_create_datetime,"%y-%m-%d").day()

    def acc_month(self):
        return datetime.strptime(self._acc_create_datetime, "%y-%m-%d").month()

    def acc_year(self):
        return datetime.strptime(self._acc_create_datetime, "%y-%m-%d").year()

    def create_account(self):
        db = pymysql.connect("localhost", "root", "secret", "finance_db")
        cursor = db.cursor()
        sql1 = "INSERT INTO accountdb (acc_provider, \
               acc_no, acc_name, acc_type, acc_create_datetime, \
               acc_status, acc_credit, acc_balance) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('System', 'Income', 'Income', '', datetime.now(), 'Active', 0, 0)

    def __str__(self):
        return self._acc_balance


class saving_account(Account):
    def __init__(self, acc_id=None, acc_provider=None, acc_no=None, acc_name=None, acc_type="Saving",
                 acc_create_datetime=None, acc_status=None, acc_credit=0, acc_balance=0):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)

    def new_account(self):
        self._acc_status = "Active"

    def close_account(self):
        self._acc_status = "Close"
        return self._acc_balance

    def disable_account(self):
        self._acc_status = "Inactive"

    def withdraw(self,value):
        if self._acc_balance >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def deposit(self,value):
        self._acc_balance += value

    def transfer_from(self,value):
        if self._acc_balance >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def transfer_to(self,value):
        self._acc_balance += value


class credit_account(Account):
    def __init__(self, acc_id=None, acc_provider=None, acc_no=None, acc_name=None, acc_type="Credit",
                 acc_create_datetime=None, acc_status=None, acc_credit=0, acc_balance=0):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)
    def new_account(self):
        self._acc_status = "Active"

    def close_account(self):
        self._acc_status = "Close"
        return self._acc_balance

    def disable_account(self):
        self._acc_status = "Inactive"

    def withdraw(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def deposit(self,value):
        self._acc_balance += value

    def transfer_from(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False

    def transfer_to(self,value):
        self._acc_balance += value

    def payment_by_credit(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False


class cash_account(Account):
    def __init__(self, acc_id=None, acc_provider="System", acc_no=None, acc_name=None, acc_type="Cash",
                 acc_create_datetime=None, acc_status="Active", acc_credit=0, acc_balance=0):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)

    def increse_money(self,value):
        self._acc_balance += value

    def decrease_money(self,value):
        if (self._acc_balance + self._acc_credit) >= value:
            self._acc_balance -= value
            return True
        else:
            return False


class income_account(Account):
    def __init__(self, acc_id=None, acc_provider="System", acc_no=None, acc_name=None, acc_type="Shop",
                 acc_create_datetime=None, acc_status="Active", acc_credit=0, acc_balance=0):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)

    def income_log(self,value):
        self._acc_balance += value


class shop_account(Account):
    def __init__(self, acc_id=None, acc_provider="System", acc_no=None, acc_name=None, acc_type="Shop",
                 acc_create_datetime=None, acc_status="Active", acc_credit=0, acc_balance=0):
        super().__init__(acc_id, acc_provider, acc_no, acc_name, acc_type, acc_create_datetime, acc_status, acc_credit,
                         acc_balance)

    def shop_log(self,value):
        self._acc_balance += value


if __name__ == '__main__':

    db_read_records()
    sql1 = """
           SELECT * FROM accountdb;
           """
    db = database.Database()
    accounts = db.query(sql1)
    for acc in accounts:
        print(acc)

    list_account = [saving_account()]
    list_account[0].acc_id = 1
    list_account[0].acc_provider = "BBL"
    list_account[0].acc_no = "12345678"
    list_account[0].acc_name = "Tawatchai Saving"
    list_account[0].acc_type = "Saving"
    list_account[0].acc_create_date = datetime.now()
    list_account[0].acc_status = "Active"
    list_account[0].acc_credit = 0
    list_account[0].acc_balance = 0

    list_account[0].deposit(500)
    print(list_account[0].acc_balance)
    status = list_account[0].withdraw(1440)
    if status:
        print(list_account[0].acc_balance)
    else:
        print("Not enough money")

