import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

RAILWAY_HOST = os.environ['RAILWAY_HOST']
RAILWAY_DB = os.environ['RAILWAY_DB']
RAILWAY_USER = os.environ['RAILWAY_USER']
RAILWAY_PASSWORD = os.environ['RAILWAY_PASSWORD']
RAILWAY_PORT =int(os.environ['RAILWAY_PORT'])

def connection():
    conn = any
    
    try:
        conn = mysql.connector.connect(
            host=RAILWAY_HOST,
            database=RAILWAY_DB,
            user=RAILWAY_USER,
            password=RAILWAY_PASSWORD,
            port=RAILWAY_PORT
        )
    except mysql.connector.Error as e:
      print('An exception occurred', e)
      
    return conn