import pymysql
import account
from datetime import date, time, datetime


class Database:
    dsn1 = ("localhost", "root", "secret")
    dsn2 = ("localhost", "root", "secret", "finance_db")

    _conn1 = None
    _conn2 = None
    _cursor1 = None
    _cursor2 = None

    def __init__(self):
        self.db_create_database()
        self._conn2 = pymysql.connect(*self.dsn2)
        self._cursor2 = self._conn2.cursor()

    def __enter__(self):
        return Database()

    def db_create_database(self):
        self._conn1 = pymysql.connect(*self.dsn1)
        self._cursor1 = self._conn1.cursor()
        sql ="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'finance_db'"
        self._cursor1.execute(sql)
        if not self._cursor1.fetchone()[0]:
            sql = "CREATE DATABASE IF NOT EXISTS finance_db"
            self._cursor1.execute(sql)

    def db_drop_tables(self):
        sql = "DROP TABLE IF EXISTS accountdb"
        self._cursor2.execute(sql)
        sql = "DROP TABLE IF EXISTS transactiondb"
        self._cursor2.execute(sql)
        self.init_database()

    def db_create_tables(self):
        self._conn1 = pymysql.connect(*self.dsn1)
        self._cursor1 = self._conn1.cursor()
        sql = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = 'finance_db'
                    AND TABLE_NAME = 'accountdb';"""
        self._cursor1.execute(sql)
        if not self._cursor1.fetchone():
            sql = """CREATE TABLE IF NOT EXISTS accountdb (
                       acc_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                       acc_provider  CHAR(20),
                       acc_no VARCHAR(20) NOT NULL UNIQUE,
                       acc_name VARCHAR(30),
                       acc_type CHAR(10),
                       acc_create_datetime DATETIME,
                       acc_status CHAR(10),
                       acc_credit DECIMAL,
                       acc_balance DECIMAL)"""
            self._cursor2.execute(sql)

        sql = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'finance_db'
                            AND TABLE_NAME = 'transactiondb';"""
        self._cursor1.execute(sql)
        if not self._cursor1.fetchone():
            sql = """CREATE TABLE IF NOT EXISTS transactiondb (
                               trans_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                               trans_datetime DATETIME,
                               trans_action VARCHAR(20),
                               trans_amount DECIMAL,
                               from_acc VARCHAR(20),
                               to_acc VARCHAR(20),
                               from_acc_balance DECIMAL,
                               to_acc_balance DECIMAL)"""
            self._cursor2.execute(sql)

    def transaction_code(self,trans_code):
        trans_dic = {0: "Create Account",
                     1: "Delete Account",
                     2: "Withdraw From",
                     3: "Deposit To",
                     4: "Transfer From",
                     5: "Transfer To",
                     6: "Payment with Credit Account",
                     7: "Payment with Cash"
                     }
        return trans_dic(trans_code)

    def init_database(self):
        self.db_create_database()
        self.db_create_tables()
        self.db_insert_default_accounts()

    def insert_transaction_log(self,trans_datetime,trans_action,trans_amount,from_acc, to_acc, from_acc_balance, to_acc_balance):
        sql = "INSERT INTO transactiondb (trans_datetime, trans_action, \
                    trans_amount, from_acc, to_acc, from_acc_balance, to_acc_balance) \
                    VALUES ('%s', '%s', '%f', '%s', '%s', '%f', '%f')" % \
              (trans_datetime,trans_action,trans_amount, from_acc, to_acc, from_acc_balance, to_acc_balance)
        try:
            self._cursor2.execute(sql)
            self._conn2.commit()
            return True
        except:
            self._conn2.rollback()
            return False

    def db_read_all_transaction(self,acc_type):
        if acc_type == "All":
            sql = "SELECT * FROM transactiondb ORDER BY trans_id"
        elif acc_type == "Bank":
            sql = "SELECT * FROM transactiondb WHERE NOT (from_acc IN ('Cash','Income','Shop') and to_acc IN ('Cash','Income','Shop')) ORDER BY trans_id"
        elif acc_type == "Income":
            sql = "SELECT * FROM transactiondb WHERE from_acc = 'Income' ORDER BY trans_id"
        elif acc_type == "Shop":
            sql = "SELECT * FROM transactiondb WHERE from_acc = 'Shop' ORDER BY trans_id"
        elif acc_type == "Cash":
            sql = "SELECT * FROM transactiondb WHERE from_acc = 'Cash' ORDER BY trans_id"
        self._cursor2.execute(sql)
        return self._cursor2.fetchall()

    def db_read_one_account(self,acc_no):
        sql = "SELECT * FROM accountdb WHERE acc_no = '{}'".format(acc_no)
        self._cursor2.execute(sql)
        return self._cursor2.fetchone()

    def db_read_all_account(self,acc_type):
        if acc_type == "All":
            sql = "SELECT * FROM accountdb WHERE acc_provider <> '_System' ORDER BY acc_provider, acc_type, acc_name"
        elif acc_type == "Bank":
            sql = "SELECT * FROM accountdb WHERE not (acc_provider = '_System' or acc_provider = '_Personal') ORDER BY acc_provider, acc_type, acc_name"
        else:
            sql = "SELECT * FROM accountdb WHERE acc_type = '{}' ORDER BY acc_provider, acc_type, acc_name".format(acc_type)
        self._cursor2.execute(sql)
        return self._cursor2.fetchall()



    def db_insert_default_accounts(self):
        sql1 = "SELECT count(*) FROM accountdb WHERE acc_no = 'Income'"
        sql2 = "SELECT count(*) FROM accountdb WHERE acc_no = 'Cash'"
        sql3 = "SELECT count(*) FROM accountdb WHERE acc_no = 'Shop'"
        sql4 = "INSERT INTO accountdb (acc_provider, \
           acc_no, acc_name, acc_type, acc_create_datetime, \
           acc_status, acc_credit, acc_balance) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('_System', 'Income', '-', 'Income', datetime.now(), 'Active', 0, 0)
        sql5 = "INSERT INTO accountdb (acc_provider, \
               acc_no, acc_name, acc_type, acc_create_datetime, \
               acc_status, acc_credit, acc_balance) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('_Personal', 'Cash', '-', 'Cash', datetime.now(), 'Active', 0, 0)
        sql6 = "INSERT INTO accountdb (acc_provider, \
               acc_no, acc_name, acc_type, acc_create_datetime, \
               acc_status, acc_credit, acc_balance) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('_System', 'Shop', '-', 'Shop', datetime.now(), 'Active', 0, 0)
        try:
            self._cursor2.execute(sql1)
            if not self._cursor2.fetchone()[0]:
                self._cursor2.execute(sql4)
            self._cursor2.execute(sql2)
            if not self._cursor2.fetchone()[0]:
                self._cursor2.execute(sql5)
            self._cursor2.execute(sql3)
            if not self._cursor2.fetchone()[0]:
                self._cursor2.execute(sql6)
            self._conn2.commit()
        except:
            self._conn2.rollback()

    def db_insert_saving_account(self,acc_provider,acc_no,acc_name):
        sql1 = "SELECT count(*) FROM accountdb WHERE acc_no = '%s'" %acc_no
        sql2 = "INSERT INTO accountdb (acc_provider,\
                acc_no, acc_name, acc_type, acc_create_datetime, \
                acc_status, acc_credit, acc_balance) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d')" % \
                (acc_provider, acc_no, acc_name, 'Saving', datetime.now(), 'Active', 0, 0)
        try:
            self._cursor2.execute(sql1)
            if not self._cursor2.fetchone()[0]:
                self._cursor2.execute(sql2)
                self._conn2.commit()
                print("\tResult : Account Created")
            else:
                print("\tResult : Can't create this account - Account Number : {} already exist".format(acc_no))
        except:
            self._conn2.rollback()
            print("Error creating this account")

    def db_insert_current_account(self,acc_provider,acc_no,acc_name,acc_credit):
        sql1 = "SELECT count(*) FROM accountdb WHERE acc_no = '%s'" % acc_no
        sql2 = "INSERT INTO accountdb (acc_provider, \
                acc_no, acc_name, acc_type, acc_create_datetime, \
                acc_status, acc_credit, acc_balance) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d')" % \
                (acc_provider, acc_no, acc_name, 'Credit', datetime.now(), 'Active', acc_credit, 0)
        try:
            self._cursor2.execute(sql1)
            if not self._cursor2.fetchone()[0]:
                self._cursor2.execute(sql2)
                self._conn2.commit()
                print("\tResult : Account Created")
            else:
                print("\tResult : Can't create this account - Account Number : {} already exist".format(acc_no))
        except:
            self._conn2.rollback()
            print("Error creating this account")

    def delete_account(self,acc_no):
        sql = "delete from accountdb where acc_no = '{}'".format(acc_no)
        try:
            self._cursor2.execute(sql)
            self._conn2.commit()
            return True
        except:
            self._conn2.rollback()
            return False

    def update_account_balance(self,acc_no,amount):
        sql = "update accountdb set acc_balance={} where acc_no = '{}'".format(amount,acc_no)
        try:
            self._cursor2.execute(sql)
            self._conn2.commit()
            return True
        except:
            self._conn2.rollback()
            return False

    def insert_update_delete(self, query):
        try:
            self._cursor2.execute(query)
            self._conn2.commit()
            return True
        except:
            self._conn2.rollback()
            return False

    def query(self, query):
        cursor = self._conn2.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        if self._conn2:
            self._conn2.close()


def db_check_connection():
    try:
        conn = pymysql.connect("localhost", "root", "secret", "finance_db")
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        # Check if anything at all is returned
        if results:
            return True
        else:
            return False
    except:
        return False



            #if __name__ == '__main__':
    #db = DBase()
    #with DBase() as db:
    #db.dbase_create_database()

    #db = Database()

    #db.init_database()
    #with Database() as db:
    #db.db_insert_saving_account('bbl','123','lek')
