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

cursor = connection.cursor()

# CREAT TABLE
# creat_table = """
# create table Users (name varchar(200), email varchar(200), phone int(15), api_key varchar(200), secret_key varchar(200), password char(40))
# """

# table = cursor.execute(creat_table)

cursor.execute("SELECT * FROM Users")
details = cursor.fetchall()
print(details)


 