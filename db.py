import pymysql as mysql


def hello():
    print("I am hello world")
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
    db = db,
    cursorclass=mysql.cursors.DictCursor
)



# CREAT TABLE
def create():
    cursor = connection.cursor()
    creat_table = """
    create table Users (id int(11) NOT NULL AUTO_INCREMENT, name varchar(200), email varchar(200) UNIQUE, phone bigint(15), api_key varchar(200), secret_key varchar(200), password char(225), PRIMARY KEY (id))
    """
    table = cursor.execute(creat_table)
    print("successfuly create the database")

def register(name, email, phone, api_key, secret_key, password):
    cur = connection.cursor()
    sql = "INSERT INTO `Users` (`name`, `email`, `phone`, `api_key`, `secret_key`, `password`) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (name, email, int(phone), api_key, secret_key, password))
    connection.commit()

def login(email, password="adfd"):
    cur = connection.cursor()
    sql = ("SELECT * FROM Users WHERE email = %s")
    result = cur.execute(sql, email)
    if result > 0:
        user = cur.fetchone()
        return user
    else:
        return None
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
# # create()