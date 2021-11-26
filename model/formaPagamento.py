from logging import NullHandler
from database import database
import hashlib
import os



class PagamentoModel():

    def __init__(self, id):
        self.id = id
        
        
    #Gravar user no DB
    # def save_to_db(self):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("INSERT INTO endereco(id, idUsuario, endereco, numero,bairro,estado, complemento) VALUES (%s,%s,%s,%s,%s,%s,%s)", (self.id,self.idUsuario,self.endereco, self.numero,self.bairro,self.estado, self.complemento))
    #     connect.commit()
    #     cur.close()
    
    @classmethod
    def get_all_forma_pagamento(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM forma_pagamento")
        registros = cur.fetchall()
        return registros
    
    def get_forma_pagamento_id(id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM forma_pagamento WHERE id=%s",(int(id),))
        registros = cur.fetchall()
        return registros

