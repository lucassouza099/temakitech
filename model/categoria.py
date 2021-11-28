from logging import NullHandler
from database import database
import hashlib
import os



class CategoriaModel():

    def __init__(self, categoria):
        self.categoria       = categoria
        
        
    #Gravar user no DB
    def save_to_db(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO categoria(nome) VALUES (%s)", (self.categoria,))
        connect.commit()
        cur.close()

    #Ao criar verificar se o categoria já existe
    @classmethod
    def get_categoria(self, nome):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT nome FROM categoria WHERE nome=%s",(nome,))
        registro = cur.fetchone()
        if (registro): 
            categoria = self
            categoria.nome = registro[0]
            return categoria
        categoria = False

    @classmethod
    def get_categoria_all(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM categoria")
        registros = cur.fetchall()
        return registros
        

    @classmethod
    def find_by_id(self, id):
        id = str(id)
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM categoria WHERE id=%s",(int(id),))
        categoria = cur.fetchone()
        if categoria:
          cat = self
          cat.id = categoria[0]
          cat.nome = categoria[1]
        return cat

    @classmethod
    def delete_by_id(self, id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("DELETE FROM categoria WHERE id =%s",(int(id),))
        connect.commit()
        cur.close()



    @classmethod
    def update_categoria(self,id, nome):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("UPDATE categoria SET nome =%s where id =%s",(nome,id))
        connect.commit()
        cur.close()
         
