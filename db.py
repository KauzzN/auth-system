import pymysql

conn = pymysql.connect(
    host="localhost",
    user="auth_system_user",
    password="12345678",
    database="auth_system",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()