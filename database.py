import mysql.connector
from mysql.connector import errorcode

class database():
  def __init__(self):
     self.config = {
      'user': 'b4e0f46015fe75',
      'password': '5edba6ba',
      # 'password': 'techit@2021',
      'host': 'us-cdbr-east-04.cleardb.com',
      'database': 'heroku_ea3a5eaf6af7dd4',
      # 'user': 'root',
      # 'password': 'techit@2021',
      # 'host': '127.0.0.1',
      # 'database': 'temakitech',
      'raise_on_warnings': True
    }

  def abrirConexao(self):
    mysqlconnector = mysql.connector.connect(**self.config)

    return mysqlconnector
  
  def commitWork(self):
    mysqlconnector = mysql.connector.connect(**self.config)
    mysqlconnector.commit()

  





