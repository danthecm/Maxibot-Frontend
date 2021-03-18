import pymysql as mysql
import base64
import pickle

# Data instance identifer
db = "MaxiBot"
username = "admin"
password = "maxitest"
host = "maxitest.cepigw2nhp7p.us-east-2.rds.amazonaws.com"
port = 3306

connection = mysql.connect(
    host=host,
    port=port,
    user=username,
    password=password,
    db=db,
    cursorclass=mysql.cursors.DictCursor
)


# CREAT TABLE
def createUsers():
    cursor = connection.cursor()
    creat_table = """
    create table Users (id int(11) NOT NULL AUTO_INCREMENT, name varchar(200), email varchar(200) UNIQUE, phone bigint(15), api_key varchar(200), secret_key varchar(200), password char(225), PRIMARY KEY (id))
    """
    cursor.execute(creat_table)
    cursor.close()
    print("successfuly create the database")


def createOrders():
    try:
        cursor = connection.cursor()
        creat_table = """
        create table Orders (id int(11) NOT NULL AUTO_INCREMENT, user_id varchar(200), trade_id varchar(200), pairs varchar(50), order_id varchar(200) UNIQUE, time float(25) UNIQUE, PRIMARY KEY (id))
        """
        cursor.execute(creat_table)
        print("successfuly create the table")
        cursor.close()
    except Exception as e:
        print(e)


def createTrades():
    try:
        cur = connection.cursor()
        create_table = """ 
        create table Trades (id int(11) NOT NULL AUTO_INCREMENT, user_id varchar(200), pairs varchar(50),current_price float(25), average_margin float(25), current_margin float(25), amount float(50), sell_margin float(25), trades int(11), status varchar(200), time float(25) UNIQUE, PRIMARY KEY (id))
         """
        cur.execute(create_table)
        print("Successfully created the table")
        cur.close()
    except Exception as e:
        print(e)

def register(name, email, phone, api_key, secret_key, password):
    try:
        cur = connection.cursor()
        sql = "INSERT INTO `Users` (`name`, `email`, `phone`, `api_key`, `secret_key`, `password`) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (name, email, int(phone),
                          api_key, secret_key, password))
        connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return "There was an error"


def new_trade(user_id, pairs, current_price, average_m, current_m, amount, sell_m, trades, status, time):
    try:
        cur = connection.cursor()
        sql = "INSERT INTO `Trades` (`user_id`, `pairs`, `current_price`, `average_margin`, `current_margin`, `amount`, `sell_margin`, `trades`, `status`, `time`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (user_id, pairs, current_price, average_m, current_m, amount, sell_m, trades, status, time))
        connection.commit()
        cur.close
        return True
    except Exception as e:
        print(e)


def new_order(user_id, pairs, order_id, time):
    try:
        cur = connection.cursor()
        sql = "INSERT INTO `Orders` (`user_id`, `pairs`,  `order_id`, `time`) VALUES(%s, %s, %s, %s, %s)"
        cur.execute(sql, (user_id, pairs, order_id, time))
        connection.commit()
        cur.close
        return True
    except Exception as e:
        print(e)
        return "There was an error"

def get_order(id):
    cur = connection.cursor()
    sql = ("SELECT * FROM Orders WHERE user_id = %s")
    result = cur.execute(sql, id)
    if result > 0:
        order = cur.fetchall()
        cur.close
        return order
    else:
        return None

def get_all_trades(id):
    cur = connection.cursor()
    sql = ("SELECT * FROM Trades WHERE status = %s")
    result = cur.execute(sql, id)
    if result > 0:
        trades = cur.fetchall()
        cur.close
        return trades
    else:
        return None

def result(id):
    cur = connection.cursor()
    sql = ("SELECT result FROM celery_taskmeta WHERE id = %s")
    result = cur.execute(sql, id)
    if result > 0:
        order = cur.fetchone()
        cur.close
        return order
    else:
        return None

def login(email):
    try:
        cur = connection.cursor()
        sql = ("SELECT * FROM Users WHERE email = %s")
        result = cur.execute(sql, email)
        if result > 0:
            user = cur.fetchone()
            cur.close()
            return user
        else:
            return None
    except Exception as e:
        print(e)
        return "Connection Error"


def delete():
    try:
        cur = connection.cursor()
        droped = cur.execute("DROP TABLE Trades")
        print(droped)
        cur.close()
    except Exception as e:
        print(e)


def email_exist(email):
    pass


# try:
#     register("Dan Test2", "dantest@gmail.com", int("2349011509080") , "EADFAASDFWfasdfqwFASDFsdaf", "EASDasdfweasdfFSFDAsdfa", "maxitest")
# except mysql.err.IntegrityError:
#     print("Opps you have a duplicate email")
# me = login("asdfasdfs@gmail.com")
# print(me)
# if me == None:
#     print(" YOu've entered the wrong email")
# else:
#     print(f"WELCOME {me[1]} your email address is {me[2]} and your phone number is {me[3]} all other information are secret bro ")
# createTrades()
# createOrders()
# delete()
# me = result(20)
# answer = pickle.loads(me["result"])

# print(answer)