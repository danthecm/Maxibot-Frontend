import pymysql as mysql


# Data instance identifer 
db = "MaxiBot" 
username = "admin"
password = "maxitest"
host = "maxitest.cepigw2nhp7p.us-east-2.rds.amazonaws.com"
port = 3306

connection = mysql.connect(
    host = host,
    port = port,
    user = username,
    password = password,
    db = db
)

# cursor = connection.cursor()

# CREAT TABLE
# creat_table = """
# create table Users (id int(11) NOT NULL AUTO_INCREMENT, name varchar(200) NOT NULL, email varchar(200) NOT NULL UNIQUE, phone int(15) NOT NULL, api_key varchar(200) NOT NULL UNIQUE, secret_key varchar(200) NOT NULL UNIQUE, password char(40) NOT NULL, PRIMARY KEY (id))
# """

# table = cursor.execute(creat_table)

def register(name, email, phone, api_key, secret_key, password):
    cur = connection.cursor()
    sql = "INSERT INTO `Users` (`name`, `email`, `phone`, `api_key`, `secret_key`, `password`) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (name, email, phone, api_key, secret_key, password))
    connection.commit()

def login(email, password="adfd"):
    cur = connection.cursor()
    sql = ("SELECT * FROM Users")
    cur.execute(sql)
    users = cur.fetchall()
    return users
def delete():
    cur = connection.cursor()
    droped = cur.execute("DROP TABLE Users")
    print(droped)
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
