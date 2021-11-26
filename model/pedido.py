from logging import NullHandler
from database import database
import hashlib
import os



class PedidoModal():

    def __init__(self, id, idUser, idEndereco,idStatus,idFormaPagamento,valor_total,dataPedido,horaPedido):
        self.id = id
        self.idUser = idUser
        self.idEndereco = idEndereco
        self.idStatus = idStatus
        self.idFormaPagamento = idFormaPagamento
        self.valor_total = valor_total
        self.dataPedido = dataPedido
        self.horaPedido = horaPedido
        
        
    #Gravar user no DB
    def save_to_db(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO pedido(id, id_usuario, id_aux_endereco, id_status,id_forma_pagamento,valor_total ) VALUES (%s,%s,%s,%s,%s,%s)", (self.id,self.idUser,self.idEndereco,self.idStatus,self.idFormaPagamento,self.valor_total ))
        connect.commit()
        cur.close()

    def countPedidos():
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT count(*) FROM pedido")
        count = cur.fetchone()
        return count
    
    @classmethod
    def get_pedidos_user(self,id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM pedido WHERE id_usuario=%s",( int(id),))
        registros = cur.fetchall()
        return registros

        

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
