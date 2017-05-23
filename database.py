import pymysql
from datetime import date, time, datetime


class DBase:

    dsn = ("localhost","root","secret","personal_finance")

    def __init__(self):
        self.conn = pymysql.connect(*self.dsn)
        self.cur = self.conn.cursor()

    def dbase_create_database(self):
        sql = "CREATE DATABASE IF NOT EXISTS finance_db"
        self.cur.execute(sql)

    def __enter__(self):
        return DBase()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


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
        sql = "CREATE DATABASE IF NOT EXISTS finance_db"
        self._cursor1.execute(sql)

    def db_create_tables(self):
        sql = """CREATE TABLE IF NOT EXISTS accountdb (
                   acc_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   acc_provider  CHAR(20),
                   acc_no VARCHAR(20),
                   acc_name VARCHAR(30),
                   acc_type CHAR(10),
                   acc_create_datetime DATETIME,
                   acc_status CHAR(10),
                   acc_credit DECIMAL,
                   acc_balance DECIMAL)"""
        self._cursor2.execute(sql)

    def db_insert_default_accounts(self):
        sql1 = "SELECT count(*) FROM accountdb WHERE acc_name = 'Income'"
        sql2 = "SELECT count(*) FROM accountdb WHERE acc_name = 'Cash'"
        sql3 = "SELECT count(*) FROM accountdb WHERE acc_name = 'Shop'"
        sql4 = "INSERT INTO accountdb (acc_provider, \
           acc_no, acc_name, acc_type, acc_create_datetime, \
           acc_status, acc_credit, acc_balance) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('System', 'Income', 'Income', '', datetime.now(), 'Active', 0, 0)
        sql5 = "INSERT INTO accountdb (acc_provider, \
               acc_no, acc_name, acc_type, acc_create_datetime, \
               acc_status, acc_credit, acc_balance) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('System', 'Cash', 'Cash', '', datetime.now(), 'Active', 0, 0)
        sql6 = "INSERT INTO accountdb (acc_provider, \
               acc_no, acc_name, acc_type, acc_create_datetime, \
               acc_status, acc_credit, acc_balance) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
               ('System', 'Shop', 'Shop', '', datetime.now(), 'Active', 0, 0)
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

    def init_database(self):
        self.db_create_tables()
        self.db_insert_default_accounts()

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

#if __name__ == '__main__':
    #db = DBase()
    #with DBase() as db:
    #db.dbase_create_database()

    #db = Database()

    #db.init_database()
    #with Database() as db:
