"""
    This is a one time code.
    It's main purpose is to create the database that we are going to use for this project
 """

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    passwd=os.environ.get('DB_PASSWD')
)

# Prepare a cursor object
cursorObject = db.cursor()

# create the database
cursorObject.execute("CREATE DATABASE danco")

print("Database created successfully")
