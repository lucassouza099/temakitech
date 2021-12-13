import mysql.connector
from mysql.connector import errorcode

class database():
  def __init__(self):
     self.config = {

      'user': 'w6orm2w7c0f9io2p',
      'password': 'ndl4r94n3vhz73p6',
      'host': 'yjo6uubt3u5c16az.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
      'database': 'afx2fov6gpzbgr2g',

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

  





