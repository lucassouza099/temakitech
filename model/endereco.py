from logging import NullHandler
from database import database
import hashlib
import os



class enderecoModel():

    def __init__(self, id, idUsuario, endereco, numero,bairro,estado, complemento):
        self.id = id
        self.idUsuario = idUsuario
        self.endereco = endereco
        self.numero = numero
        self.endereco = endereco
        self.bairro = bairro
        self.estado = estado
        self.complemento = complemento
        
        
    #Gravar user no DB
    def save_to_db(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO endereco(id, idUsuario, endereco, numero,bairro,estado, complemento) VALUES (%s,%s,%s,%s,%s,%s,%s)", (self.id,self.idUsuario,self.endereco, self.numero,self.bairro,self.estado, self.complemento))
        connect.commit()
        cur.close()
    
    @classmethod
    def get_enderecos_user(self,idUser):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM endereco WHERE idUsuario =%s",(int(idUser),))
        registros = cur.fetchall()
        return registros

    @classmethod
    def get_endereco(self, id, idUser):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM endereco WHERE id=%s and idUsuario =%s",(id,idUser,))
        registro = cur.fetchone()
        if (registro): 
            endereco = self
            endereco.id = registro[0]
            endereco.idUsuario = registro[2]
            endereco.endereco = registro[3]
            endereco.numero = registro[4]
            endereco.bairro = registro[5]
            endereco.estado = registro[5]
            endereco.complemento = registro[5]

            return endereco
        endereco = False

    @classmethod
    def update_endereco_main(self,id, idUser):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        #Limpa todos os usuários principais
        cur.execute("UPDATE endereco SET main = %s where idUsuario = %s",(None,int(idUser),))
        connect.commit()
        #Seta ultimo usuário cadastrado como principal
        cur.execute("UPDATE endereco SET main = 'X' where id= %s and idUsuario= %s",(int(id), int(idUser),))
        connect.commit()
        cur.close()

    @classmethod
    def get_endereco_atual(self, idUser):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM endereco WHERE idUsuario=%s and main = 'X'",(idUser,))
        registro = cur.fetchone()
        if (registro): 
            endereco = self
            endereco.id = registro[0]
            endereco.idUsuario = registro[1]
            endereco.endereco = registro[2]
            endereco.numero = registro[3]
            endereco.bairro = registro[4]
            endereco.estado = registro[5]
            endereco.complemento = registro[6]
    
            return endereco
        endereco = False

    @classmethod
    def delete_by_id(self, id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("DELETE FROM endereco WHERE id =%s",(int(id),))
        connect.commit()
        cur.close()