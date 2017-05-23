import pymysql

def checkTableExists(dbcon, tablename):
    dbcursor = dbcon.cursor()
    dbcursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcursor.fetchone()[0] == 1:
        dbcursor.close()
        return True

    dbcursor.close()
    return False

def db_create_database():
    db = pymysql.connect("localhost","root","secret")
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS test1"
    cursor.execute(sql)
    db.close()

def db_connect():
    #https: // www.tutorialspoint.com / python3 / python_database_access.htm
    db = pymysql.connect("localhost","root","secret","employees" )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print ("Database version : %s " % data)
    db.close()

def db_create():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    sql = """CREATE TABLE EMPLOYEE (
       FIRST_NAME  CHAR(20) NOT NULL,
       LAST_NAME  CHAR(20),
       AGE INT,
       SEX CHAR(1),
       INCOME FLOAT )"""
    cursor.execute(sql)
    db.close()

def db_insert1():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
       LAST_NAME, AGE, SEX, INCOME)
       VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def db_insert2():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
          ('Mac', 'Mohan', 20, 'M', 2000)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def db_read():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    sql = "SELECT * FROM EMPLOYEE \
           WHERE INCOME > '%d'" % (1000)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            fname = row[0]
            lname = row[1]
            age = row[2]
            sex = row[3]
            income = row[4]
            print("fname = %s,lname = %s,age = %d,sex = %s,income = %d" % \
                  (fname, lname, age, sex, income))
    except:
        print("Error: unable to fetch data")
    db.close()

def db_update():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()

def db_deleterecord():
    db = pymysql.connect("localhost", "root", "secret", "test")
    cursor = db.cursor()
    sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

if __name__ == '__main__':
    db_connect()
    db_create()
    db_insert1()
    db_read()
    print()
    db_update()
    db_insert2()
    db_read()
    print()
    db_deleterecord()
    db_read()

    db_create_database()

    db = pymysql.connect("localhost","root","secret","employees" )
    cursor = db.cursor()
    print(checkTableExists(db,"test",))
    cursor = db.cursor()
    print(checkTableExists(db, "employees", ))
    db.close()

