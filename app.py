from flask import Flask, flash, session, url_for, make_response, request, render_template, redirect, send_from_directory, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_mysqldb import MySQL
from security import authenticate, identity
from resources.user import UserRegister
from resources.categoria import CategoriaList, CategoriaMaintenance
from resources.categoria import Categoria
from resources.statusPedido import Status
from resources.produto import Produto, ProdutoList
from resources.produto import ProdutoMaintenance
from resources.endereco import EnderecoList
from resources.endereco import Endereco
from resources.auxEndereco import AuxEndereco
from resources.auxPedido import ProdutoListPed
from resources.auxPedido import AuxPedido
from resources.pedido import PedidoList
from resources.formaPagamento import FpagamentosList
from resources.formaPagamento import Fpagamentos
from flask_cors import CORS, cross_origin
from contextlib import closing
from model.user import UserModel
from model.endereco import enderecoModel
from model.pedido import PedidoModal
from model.auxPedido import AuxprodModal
from model.auxEndereco import AuxenderecoModal
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import os
import werkzeug
import json
import simplejson

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

FLASK_ENV="production"
# Criando conexões com o banco de dados
app.secret_key = 'techit'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Criação do endpoint  /auth
# Chamando as Apis através dos endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(CategoriaList, '/categoria/list')
api.add_resource(Categoria, '/categoria')
api.add_resource(CategoriaMaintenance, '/categoria/maintenance/<string:id>')
api.add_resource(Produto, '/produto')
api.add_resource(ProdutoList, '/produto/list')
api.add_resource(ProdutoMaintenance, '/produto/maintenance/<string:id>')
api.add_resource(Status, '/pedido/status')
# api.add_resource(Status, '/pedido')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
def raiz():
    produto = ProdutoList()
    categoria = CategoriaList()
    listaProdutos = produto.get()
    listaCategorias = categoria.get()
    try:
        carrinho = session['cart']
    except Exception as error:
        carrinho = []

    ValorTotal = 0
    ValorTotal = float(ValorTotal)
    for x in carrinho:
        ValorTotal = ValorTotal + float(x['precoTotal'])
    try:
        session['valorTotal'] = ValorTotal
    except Exception as error:
        ValorTotal

    return render_template("index.html", produtos=listaProdutos, categorias=listaCategorias, carrinho=ValorTotal)


@app.route("/logar", methods=["POST", "GET"])
def logar():
    # Extrai os dados do formulário.
    f = request.form
    if "login" not in f or "senha" not in f:
        return ":(", 422
    login = f["login"]
    senha = f["senha"]

    logado = authenticate(login, senha)

    if logado:
        res = make_response(redirect("/"))
        nome = logado.nome
        nome= nome.split(' ')
        

        res.set_cookie("nomeUser", nome[0], samesite="Strict")
        res.set_cookie("id", str(logado.id), samesite="Strict")
        res.set_cookie("login", login, samesite="Strict")
        res.set_cookie("senha", senha, samesite="Strict")
        return res
    else:
        return {'message': 'Email ou senha inválidos'}, 400

@app.route("/gerenciaProduto", methods=["POST", "GET"])
def gerenciaProduto():
    produto = ProdutoList()
    categoria = CategoriaList()
    listaProdutos = produto.get()
    listaCategorias = categoria.get()
    return render_template("produto.html",produtos = listaProdutos,categorias = listaCategorias)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    res = make_response(redirect("/"))
    res.set_cookie("nomeUser", "", samesite="Strict")
    res.set_cookie("id", "", samesite="Strict")
    res.set_cookie("login", "", samesite="Strict")
    res.set_cookie("senha", "", samesite="Strict")
    return res

# FRONT - Tela login e cadastro


@app.route("/login", methods=["POST", "GET"])
def login():

    control = request.form['login']
    if control == 'cadastro':
        control = ''
    return jsonify({'htmlresponse': render_template('login.html', controlLogin=control)})

#Tela de cadastro de produto
@app.route("/addTelaProduto", methods=["POST", "GET"])
def addTelaProduto():
    return jsonify({'htmlresponse': render_template('cadastroProduto.html')})

#Tela de cadastro de endereço
@app.route("/addTelaEndereco", methods=["POST", "GET"])
def addTelaEndereco():
    return jsonify({'htmlresponse': render_template('cadastroEndereco.html')})

@app.route("/addTelaEnderecoPerfil", methods=["POST", "GET"])
def addTelaEnderecoPerfil():
    return jsonify({'htmlresponse': render_template('cadastroEnderecoPerfil.html')})

# Rotina de criação de usuário

@app.route("/cadastroProduto", methods=["POST"])
def cadastroProduto():
    f = request.files['file']
    f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
    return 'file uploaded successfully'
# check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save('favicon.png')  

@app.route("/cadastroUser", methods=["POST"])
def cadastroUser():
    # Função post para registro de usuário

    # Função para verificar se o usuário já existe no banco de dados
    if UserModel.find_by_username(request.form['email']):
      # caso não existir retorno a mensagem abaixo
        return {"message": "Este email já existe no sistema"}, 409
        # chamando a classe para gravar o usuário no banco de dados
    
    if request.form['senha'] != request.form['repsenha']:
        return {"message": "As senhas são diferentes!"}, 409

    user = UserModel(False, request.form['email'], request.form['senha'], request.form['nome'], int(request.form['ddd']),
                     int(request.form['telefone']))
    
    user.save_to_db()
    res = make_response(redirect("/"))
    user = UserModel.find_by_username(request.form['email'])
    res.set_cookie("nomeUser", request.form['nome'], samesite="Strict")
    res.set_cookie("id", str(user.id), samesite="Strict")
    res.set_cookie("login", request.form['email'], samesite="Strict")
    res.set_cookie("senha", request.form['senha'], samesite="Strict")
    return res      

@app.route("/updateUser", methods=["POST"])
def updateUser():
    user = UserModel(request.cookies.get("id", ""),None, None, request.form['nome'],int(request.form['ddd']),int(request.form['telefone']))
    user.update_by_id(request.cookies.get("id", ""),request.form['nome'],int(request.form['ddd']),int(request.form['telefone']))
    return{"message":"Sucesso para alterar"}

@app.route("/updateUserPass", methods=["POST"])
def updateUserPass():
    user = UserModel.find_by_username(request.cookies.get("login", ""))
    if request.form['senhaAtual'] != user.password:
       return {"message":"Senha atual está inválida"},404
    
    if request.form['senha'] != request.form['repsenha']:
        return {"message":"Senhas novas divergem!"},404
    
    if request.form['senha'] == request.form['senhaAtual']:
        return {"message":"Senhas nova não pode ser igual a senha atual!"},404

    user = UserModel(request.cookies.get("id", ""),None,request.form['senha'], None, None,  None)
    user.update_pass(request.cookies.get("id", ""),request.form['senha'])
    return{"message":"Sucesso para alterar a senha"}

@app.route("/cadastroEndereco", methods=["POST"])
def cadastroEndereco():
    # Função post para registro de endereco
    endereco = enderecoModel(False, int(request.cookies.get("id", "")), request.form['endereco'], int(request.form['numero']), request.form['bairro'],
                     request.form['estado'], request.form['complemento'])
    
    endereco.save_to_db()
    return redirect('/endereco')

@app.route("/cadastroEnderecoPerfil", methods=["POST"])
def cadastroEnderecoPerfil():
    # Função post para registro de endereco
    endereco = enderecoModel(False, int(request.cookies.get("id", "")), request.form['endereco'], int(request.form['numero']), request.form['bairro'],
                     request.form['estado'], request.form['complemento'])
    
    endereco.save_to_db()
    return {"message":"Sucesso ao cadastrar o usuário"}

@app.route("/deletarEndereco", methods=["POST"])
def deletarEndereco():
    # Função post para registro de endereco
    try:
        Endereco.delete(int(request.form['id']))
        return {"message":"Sucesso ao deletar"}
    except Exception as error:
        return {"message":"Erro para deletar"},404

    


@app.route("/backEndereco",  methods=["POST"])
def backEndereco():
    return redirect('/endereco')

@app.route("/confirmPedido",  methods=["POST"])
def confirmPedido():
    if session['cart'] == []:
        return {'message': 'Não existe produtos no carrinho'}, 400

    if request.cookies.get("login", ""):
        return redirect('/endereco')
    return jsonify({'htmlresponse': render_template('login.html',controlLogin="logar")})

@app.route("/confirmEndereco",  methods=["POST"])
def confirmEndereco():    
    enderecoModel.update_endereco_main(int(request.form['id']),int(request.cookies.get("id", "")))
    return redirect('/formaPagamento')

@app.route("/formaPagamento",  methods=["POST","GET"])
def formaPagamento():
    listaPagamentos = FpagamentosList.get()
    return render_template("formaPagamento.html", formaPagamento = listaPagamentos)

@app.route("/perfil",  methods=["POST","GET"])
def perfil():
    if request.cookies.get("login", ""):

        try:
            carrinho = session['cart']
        except Exception as error:
            carrinho = []
            

        user = UserModel.find_by_username(request.cookies.get("login", ""))
        # enderecos = EnderecoList()
        # # listaEndereco = endereco.get_enderecos_user(request.cookies.get("login", ""))
        # listaEndereco = enderecos.get(int(request.cookies.get("id", "")))
        return render_template("perfil.html",carrinho=carrinho, usuario = user)    

@app.route("/endereco",  methods=["POST","GET"])
def endereco():
    if request.cookies.get("id", ""):
        enderecos = EnderecoList()
        # listaEndereco = endereco.get_enderecos_user(request.cookies.get("login", ""))
        listaEndereco = enderecos.get(int(request.cookies.get("id", "")))
        return render_template("endereco.html", enderecos = listaEndereco)

@app.route("/enderecoPerfil",  methods=["POST","GET"])
def enderecoPerfil():
    if request.cookies.get("id", ""):
        try:
            carrinho = session['cart']
        except Exception as error:
            carrinho = []
        enderecos = EnderecoList()
        # listaEndereco = endereco.get_enderecos_user(request.cookies.get("login", ""))
        listaEndereco = enderecos.get(int(request.cookies.get("id", "")))
        return render_template("enderecoPerfil.html",carrinho=carrinho, enderecos = listaEndereco)


@app.route("/confirmProduto", methods=["POST", "GET"])
def confirmProduto():
    if request.method == 'POST':
        produto = Produto()
        onlyProduto = produto.get(request.form['userid'])
        employeelist = []
    return jsonify({'htmlresponse': render_template('confirmProduto.html', produto=onlyProduto)})


@app.route("/cart", methods=["POST", "GET"])
def cart():
    # name = request.cookies.get('name')
    try:
        produtos = session['cart']
        qtdTotal = len(session['cart'])
        ValorTotal = 0
        ValorTotal = float(ValorTotal)
        for x in produtos:
            ValorTotal = ValorTotal + float(x['precoTotal'])
        session['valorTotal'] = ValorTotal
        return render_template("cart.html", carrinho=produtos, qtdCarrinho=qtdTotal, total=ValorTotal)

    except Exception as error:
        return render_template("cart.html", carrinho='', qtdCarrinho=0, total=0)
    # teste = simplejson.loads(str(name))
    # return render_template("cart.html")


@app.route("/addCart", methods=["POST", "GET"])
def addCart():
    id = request.args.get('id')
    if 'cart' not in session:
        session['cart'] = []  #
    cart_list = session['cart']

    count = 0
    for x in cart_list:
        count = count + 1
        if x['id'] == request.form['id']:
            return {'message': 'Este produto já foi adicionado ao carrinho'}, 400

    cart_list.append({"id": request.form['id'], "nome": request.form['nome'],
                     "qtd": request.form['qtd'], "preco": request.form['preco'], "precoTotal": request.form['precoTotal'], "obs": request.form['obs']})
    session['cart'] = cart_list  #
    return session


@app.route("/calcProduto", methods=["POST", "GET"])
def calcProduto():
    cart_list = session['cart']
    count = 0
    if request.form['sinal'] == '-':
        for x in cart_list:
            if x['id'] == request.form['id']:
                qtd = x['qtd']
                qtd = int(qtd)
                if qtd == 1:
                    preco = session['cart'][count]['preco']
                    del session['cart'][count]
                    session.modified = True
                    preco = float(preco)
                    qtd = 0
                    session['valorTotal'] = session['valorTotal'] - preco
                    if session['valorTotal'] <= 0:
                        session['valorTotal'] = 0

                    return {"quantidade": qtd, "total": session['valorTotal']}, 200
                    exit
                else:
                    qtd = x['qtd']
                    qtd = int(qtd)
                    precoTotal = x['precoTotal']
                    preco = x['preco']
                    preco = float(preco)
                    precoTotal = float(precoTotal)
                    session['cart'][count]['qtd'] = qtd - 1
                    session.modified = True
                    qtd = qtd - 1
                    session['cart'][count]['precoTotal'] = precoTotal - preco
                    session.modified = True
                    precoTotal = precoTotal - preco
                    session['valorTotal'] = session['valorTotal'] - preco
                    if session['valorTotal'] <= 0:
                        session['valorTotal'] = 0

            count = count+1
    else:
        for x in cart_list:

            if x['id'] == request.form['id']:
                qtd = x['qtd']
                qtd = int(qtd)
                precoTotal = x['precoTotal']
                preco = x['preco']
                preco = float(preco)
                precoTotal = float(precoTotal)
                session['cart'][count]['qtd'] = qtd + 1
                qtd = qtd + 1
                session['cart'][count]['precoTotal'] = precoTotal + preco
                session['valorTotal'] = session['valorTotal'] + preco
                if session['valorTotal'] <= 0:
                    session['valorTotal'] = 0

                precoTotal = precoTotal + preco
                session.modified = True

            count = count+1
    return {"quantidade": qtd, "id": request.form['id'], "precoTotal": precoTotal, "total": session['valorTotal']}, 200


@app.route("/finalizarPedido", methods=["POST", "GET"])
def finalizarPedido():
    #Verificação dos IDS
    totalPedidos = PedidoModal.countPedidos()
    idPedido = int(1000 + totalPedidos[0])
    #Adicionando os Produtos na tabela auxiliar
    produtos = session['cart']
    for produto in produtos:
        auxProduto = AuxprodModal(idPedido, int(produto['id']),produto['nome'],produto['obs'],produto['precoTotal'],produto['qtd'])
        auxProduto.save_to_db()
    #Adicionando endereço na tabela auxiliar de endereços
    endereco = Endereco()
    enderecoAtual = endereco.get( int(request.cookies.get("id", "")))
    enderecoAux = AuxenderecoModal(idPedido,enderecoAtual.endereco,enderecoAtual.numero,enderecoAtual.bairro,enderecoAtual.estado,enderecoAtual.complemento)
    idEndereco = enderecoAux.save_to_db()
    #Setando o ID do STATUS como em aberto forma de pagamento e valor total
    idStatus = int(1)
    idFormaPagamento = int(request.form['idPagamento'])
    valorTotal = session['valorTotal']
    #Finalizando o pedido
    pedido= PedidoModal(idPedido,int(request.cookies.get("id", "")),idEndereco,idStatus,idFormaPagamento,valorTotal,None,None)
    pedido.save_to_db()
    idPedido = str(idPedido)
    session['valorTotal'] = 0
    session['cart'] = []
    return {"message":"Pedido número "+idPedido+" Criado com sucesso"}

@app.route("/pedidos", methods=["POST", "GET"])
def pedidos():
    regPedido = PedidoList()
    endereco = []
    status = []
    fpagamentos = []
    aux_produto= []

    try:
        carrinho = session['cart']
    except Exception as error:
        carrinho = []
    
    pedidos = regPedido.get(request.cookies.get("id", ""))
    for pedido in pedidos:
        #Endereço Atual
        enderecoAux = AuxEndereco()
        enderecoAtual = enderecoAux.get( int(pedido['id']))
        endereco.append(enderecoAtual)
        getStatus = Status()
        #STATUS
        descStatus = getStatus.get( int(pedido['idStatus'])) 
        status.append(descStatus)
        #Forma de pagamento
        # clFormaPagamento = Fpagamentos()
        # fpagamentos.append(clFormaPagamento.get(pedido['idFpagamento']))
        #Produtos aux
        clAuxProd = ProdutoListPed()
        retAuxPrdo = clAuxProd.get(pedido['id'])
        for prod in retAuxPrdo:
            aux_produto.append(prod)
    listaPagamentos = FpagamentosList.get()

    newlist = sorted(pedidos, key=lambda d: d['id'], reverse=True) 

    return render_template("pedidos.html", carrinho = carrinho, AllPedidos = newlist, enderecos = endereco, Allstatus = status, formaPagamentos = listaPagamentos, aux_produto=aux_produto )

def allowed_file(filename):    
    return '.' in filename and filename.split('.', 1)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run( host="0.0.0.0", port=5000, debug=True)
    # http_erver = WSGIServer(('177.198.93.24', 5000), app)
    # http_server.serve_forever()
