"""
Create postgreSQL empty database and tables
Ensure that postgresql is installed on your machine (I am using 16.6)
This script assumes you have created a database called fyp_db and is accessible
"""

import os
import psycopg2

# Create .env file containing your own DB_USERNAME and DB_PASSWORD
db_user = os.environ["DB_USERNAME"]
db_pass = os.environ["DB_PASSWORD"]

conn = psycopg2.connect(
    host="localhost",
    database="fyp_db",
    user=db_user,  
    password=db_pass,
)


cur = conn.cursor()
# Creates table for storing essential user info.
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute(
    "CREATE TABLE users ("
    "id SERIAL PRIMARY KEY,"
    "username VARCHAR(50) UNIQUE NOT NULL,"
    "max_level INT CHECK (max_level > 0),"
    "cur_level INT CHECK (cur_level > 0 AND cur_level <= max_level),"
    "skill TEXT);"
)

conn.commit()

cur.close()
conn.close()
