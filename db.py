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


# CREAT TABLE
# creat_table = """
# create table Users (name varchar(200), email varchar(200), phone int(15), api_key varchar(200), secret_key varchar(200), password char(40))
# """

# table = cursor.execute(creat_table)

def register(name, email, phone, api_key, secret_key, password):
    cur = connection.cursor()
    cur.execute("INSERT INTO Users (name, email, phone, api_key, secret_key, password) VALUES ($s, $s, $s, $s, $s, $s)", (name, email, phone, api_key, secret_key, password))
    cur.commit()

def login(email, password):
    
print(details)


 