import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
conn= sqlite3.connect('admin.db',check_same_thread=False)
cursor=conn.cursor()    

#Create Table 
# query='''CREATE TABLE adminLogin (username VARCHAR(20),
# password VARCHAR(200))'''
# cursor.execute(query)
# conn.commit()


#Inserting a new user in the admin_database
# query = "ALTER table adminLogin add password"
# cursor.execute(query) 
# conn.commit()
new_admin='shri'
password='123'
cursor.execute("INSERT INTO adminLogin(username, password) VALUES(?, ?)",(new_admin,password))
conn.commit()

# cursor.execute("DROP TABLE adminLogin")
# conn.commit()
cursor.execute("select * from adminLogin")
print(cursor.fetchall())
conn.close()