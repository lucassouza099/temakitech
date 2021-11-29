from logging import NullHandler
from database import database
import hashlib
import os



class PedidoModal():

    def __init__(self, id, idUser, idEndereco,idStatus,idFormaPagamento,valor_total,dataPedido,horaPedido,taxaEntrega):
        self.id = id
        self.idUser = idUser
        self.idEndereco = idEndereco
        self.idStatus = idStatus
        self.idFormaPagamento = idFormaPagamento
        self.valor_total = valor_total
        self.dataPedido = dataPedido
        self.horaPedido = horaPedido
        self.taxaEntrega = taxaEntrega
        
        
    #Gravar user no DB
    def save_to_db(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO pedido(id, id_usuario, id_aux_endereco, id_status,id_forma_pagamento,valor_total,taxa_entrega ) VALUES (%s,%s,%s,%s,%s,%s,%s)", (self.id,self.idUser,self.idEndereco,self.idStatus,self.idFormaPagamento,self.valor_total,self.taxaEntrega ))
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
    def get_pedidos(self,id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM pedido WHERE id_usuario=%s",( int(id),))
        registros = cur.fetchall()
        return registros

    @classmethod
    def get_pedidos_user(self,id):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT pedido.id,pedido.valor_total,aux_produto.nome,aux_produto.detalhe,aux_produto.preco,aux_produto.quantidade,aux_endereco.endereco,aux_endereco.numero,aux_endereco.bairro,aux_endereco.estado,aux_endereco.complemento, status_pedido.status, forma_pagamento.forma_pagamento, status_pedido.id, pedido.taxa_entrega FROM pedido, aux_produto, aux_endereco, status_pedido, forma_pagamento WHERE pedido.id_usuario = %s AND	pedido.id = aux_produto.id_pedido AND  pedido.id_aux_endereco = aux_endereco.id AND pedido.id_status = status_pedido.id AND pedido.id_forma_pagamento = forma_pagamento.id " ,( int(id),))
        registros = cur.fetchall()
        return registros
    
    @classmethod
    def get_pedidos_status(self,status):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT pedido.id,pedido.valor_total,aux_produto.nome,aux_produto.detalhe,aux_produto.preco,aux_produto.quantidade,aux_endereco.endereco,aux_endereco.numero,aux_endereco.bairro,aux_endereco.estado,aux_endereco.complemento, status_pedido.status, forma_pagamento.forma_pagamento, status_pedido.id, pedido.taxa_entrega  FROM pedido, aux_produto, aux_endereco, status_pedido, forma_pagamento WHERE pedido.id_status = %s AND	pedido.id = aux_produto.id_pedido AND  pedido.id_aux_endereco = aux_endereco.id AND pedido.id_status = status_pedido.id AND pedido.id_forma_pagamento = forma_pagamento.id " ,( int(status),))
        registros = cur.fetchall()
        return registros
    
    @classmethod
    def update_produto(self,id, idStatus):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("UPDATE pedido SET id_status =%s where id= %s",(int(idStatus), int(id)))
        connect.commit()
        cur.close()
