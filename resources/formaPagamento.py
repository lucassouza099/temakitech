from model.formaPagamento import PagamentoModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# class Endereco():
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
    
#     def get(self,id):
#         #Função post para registro de usuário
#         #Função para verificar se o usuário já existe no banco de dados
#         categoria = ProdutoModel.get_produto(id)
#         if categoria:
#             #caso não existir retorno a mensagem abaixo
#             return categoria
#         #chamando a classe para gravar o usuário no banco de dados
#         return {"message": "Categoria não encontrada"}, 404

class Fpagamentos(Resource):
    def get(self, id):
        registros = PagamentoModel.get_forma_pagamento_id(id)
        formaPagamento = []
        for row in registros:
            return{'id': row[0], 'forma_pagamento': row[1], 'img': row[2]}
       

class FpagamentosList(Resource):
    def get():
        registros = PagamentoModel.get_all_forma_pagamento()
        formaPagamento = []
        for row in registros:
            formaPagamento.append({'id': row[0], 'forma_pagamento': row[1], 'img': row[2]})
        return formaPagamento

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
     
        