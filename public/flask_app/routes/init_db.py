"""
Create postgreSQL empty database and tables
Ensure that postgresql is installed on your machine (I am using 16.6)
This script assumes you have created a database called fyp_db and is accessible
Once run, server.py will be able to connect to the database
"""

import os
import psycopg2

def create_database():
    # Create .env file containing your own DB_USERNAME and DB_PASSWORD
    db_user = os.environ["fyp_db_user"]
    db_pass = os.environ["fyp_db_pass"]

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
    )

    conn.commit()

    cur.close()
    conn.close()
