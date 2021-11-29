from model.pedido import PedidoModal
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Pedido():
#     # @jwt_required()
#     def post(self):
#         #Função post para registro de usuário
#         data = Produto.parser.parse_args()
#         #Função para verificar se o usuário já existe no ban    co de dados
#         if ProdutoModel.get_produto(data['nome']):
#             #caso não existir retorno a mensagem abaixo
#             return {"message": "Essa categoria já existe no sistema"},409
#         #chamando a classe para gravar o usuário no banco de dados
#         categoria = ProdutoModel(data['idCategoria'],data['nome'],data['detalhe'], data['preco'],data['img'])
#         categoria.save_to_db()
        
#         return {"message": "Produto criado com sucesso!"}, 201
    
    def get(self,id):
        #Função post para registro de usuário
        #Função para verificar se o usuário já existe no banco de dados
        enderecoAtual = AuxenderecoModal.get_endereco_pedido(id)
        if enderecoAtual:
            #caso não existir retorno a mensagem abaixo
            return enderecoAtual
        #chamando a classe para gravar o usuário no banco de dados
        return {"message": "Endereco atual inexistente"}, 404

class PedidoList(Resource):
    def get(self,id):
        registros = PedidoModal.get_pedidos(int(id))
        produtos = []
        for row in registros:
            produtos.append({'id': row[0], 'idUsuario': row[1], 'idEndereco': row[2], 'idStatus': row[3], 'idFpagamento': row[4], 'valor_total': row[5] })
        return produtos

    def getUser(self,id):
        registros = PedidoModal.get_pedidos_user(int(id))
        produtos = []
        for row in registros:
            produtos.append({'id': row[0], 'valorTotal': row[1], 'nome': row[2], 'detalhe': row[3], 'preco': row[4], 'quantidade': row[5], 'endereco': row[6], 'numero': row[7],'estado': row[8], 'estado': row[9], 'complemento': row[10], 'status': row[11],'formaPagamento': row[12],'idStatus': row[13]})
        return produtos
    
    def getStatus(self,id):
        registros = PedidoModal.get_pedidos_status(int(id))
        produtos = []
        for row in registros:
            produtos.append({'id': row[0], 'valorTotal': row[1], 'nome': row[2], 'detalhe': row[3], 'preco': row[4], 'quantidade': row[5], 'endereco': row[6], 'numero': row[7],'estado': row[8], 'estado': row[9], 'complemento': row[10], 'status': row[11], 'formaPagamento': row[12] })
        return produtos

        
    

# class ProdutoMaintenance(Resource):
#     #Atualização do produto
#     def put(self,id):
#         data = Produto.parser.parse_args()
#         produtoModel = ProdutoModel.find_by_id(id)
#         if (produtoModel):
#              #Depois de ter verificado os campos que foram atualizados chamo a função para atualizar 
#             try:
#                 ProdutoModel.update_produto(data['idCategoria'],data['nome'],data['detalhe'],data['preco'],id, data['img'])
#                 return {"message": "Produto atualizado com sucesso!"}  
#             except:
#                 {"message": "Ocorreu um erro para atualizar o produto"}
#         else:
#             return {"message": "Erro o produto não foi encontrado!"}, 404
#     def delete(self, id):
#         produtoModel = ProdutoModel.find_by_id(id)
#         if (produtoModel):
#             try:
#                 ProdutoModel.delete_by_id(id)
#                 return {'message': 'produto deletado'}
#             except:
#                 return {"message": "Ocorreu um erro para deletar o produto"}
#         else:
#             return {"message": "Produto não encontrado para ser deletado!"}       

    # def get(self, id):
    #     #Função post para registro de usuário
    #     data = Produto.parser.parse_args()
    #     #Função para verificar se o usuário já existe no banco de dados
    #     produto = ProdutoModel.get_produto(id)
    #     if produto:
    #         #caso não existir retorno a mensagem abaixo
    #         produtos = []
    #         for row in registros:
    #          produtos.({'id': row[0], 'idCategoria': row[1], 'nome': row[2], 'detalhe': row[3], 'preco': str(row[4]), 'img': row[5] })
    #          return categoria.json()
    #     #chamando a classe para gravar o usuário no banco de dados
    #     return {"message": "Categoria não encontrada"}, 404
     
        