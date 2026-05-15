import os
import pymysql

def get_connection():
    """
    Reads connection info from environment variables:
      MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
    """
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        autocommit=True,
    )