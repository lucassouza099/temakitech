from logging import NullHandler
from database import database
import hashlib
import os



class AuxenderecoModal():

    def __init__(self, id_pedido, endereco, numero,bairro,estado,complemento):
        self.id_pedido = id_pedido
        self.endereco = endereco
        self.numero = numero
        self.bairro = bairro
        self.estado = estado
        self.complemento = complemento
        
        
    #Gravar user no DB
    def save_to_db(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO aux_endereco(id_pedido, endereco, numero, bairro,estado,complemento ) VALUES (%s,%s,%s,%s,%s,%s)", (self.id_pedido, self.endereco, self.numero, self.bairro,self.estado,self.complemento ))
        connect.commit()
        cur.execute("SELECT * FROM aux_endereco WHERE id_pedido= %s",(self.id_pedido,))
        registro = cur.fetchone()
        if registro:
            idEndereco = registro[0]
            return idEndereco

    @classmethod
    def get_endereco_pedido(self,id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM aux_endereco WHERE id_pedido=%s",(int(id),))
        registros = cur.fetchall()
        
        return registros
        
        
        

    # def getAuxProduto(self,idPedido):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("SELECT * FROM aux_produto WHERE id_pedido= %s",(idPedido))
    #     count = cur.fetchone()
    #     return count

        

    # #Ao criar verificar se o categoria já existe
    # @classmethod
    # def get_produto(self, nome):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("SELECT id FROM produto WHERE nome=%s",(nome,))
    #     registro = cur.fetchone()
    #     if (registro): 
    #         categoria = self
    #         categoria.nome = registro[0]
    #         return categoria
    #     categoria = False

    # @classmethod
    # def get_produto_all(self):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("SELECT * FROM produto")
    #     registros = cur.fetchall()
    #     return registros
        
    # @classmethod
    # def delete_by_id(self, id):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("DELETE FROM produto WHERE id =%s",(int(id),))
    #     connect.commit()
    #     cur.close()



    # @classmethod
    # def update_produto(self,idCategoria, nome, detalhe, preco, id):
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("UPDATE produto SET id_categoria =%s, nome =%s, detalhe= %s, preco = %s where id= %s",(int(idCategoria),nome,detalhe,preco, id))
    #     connect.commit()
    #     cur.close()
        

    # @classmethod
    # def find_by_id(self, id):
    #     id = int(id)
    #     connectorDatabase = database()
    #     connect = connectorDatabase.abrirConexao()
    #     cur = connect.cursor()
    #     cur.execute("SELECT id FROM produto WHERE id='%s'",(id,))
    #     produto = cur.fetchone()
    #     return produto
