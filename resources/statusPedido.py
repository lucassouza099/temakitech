from model.statusPedido import StatusModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Status(Resource):


    def get(self,id):
        #Função post para registro de usuário
        #Função para verificar se o usuário já existe no banco de dados
        status = StatusModel.get_status(id)
        return {'idEndereco': status[0], 'endereco': status[1] }

    # @jwt_required()
    def post(self):
        #Função post para registro de usuário
        data = Status.parser.parse_args()
        #Função para verificar se o usuário já existe no banco de dados
        if StatusModel.get_status(data['nome']):
            #caso não existir retorno a mensagem abaixo
            return {"message": "Essa categoria já existe no sistema"},409
        #chamando a classe para gravar o usuário no banco de dados
        statusPedido = StatusModel(data['status'])
        statusPedido.save_to_db()
        
        return {"message": "Categoria criado com sucesso!"}, 201
    
    