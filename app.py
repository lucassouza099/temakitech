from flask import Flask, config, flash, session, url_for, make_response, request, render_template, redirect, send_from_directory, jsonify
from flask.wrappers import Request
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
from model.produto import ProdutoModel
from model.configuracao import configModal
from resources.endereco import EnderecoList
from resources.endereco import Endereco
from resources.auxEndereco import AuxEndereco
from resources.auxPedido import ProdutoListPed
from resources.auxPedido import AuxPedido
from model.categoria import CategoriaModel
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
from pytz import timezone
import os
import werkzeug
import json
import simplejson
import datetime

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
# APP_ROOT = 'https://temakitechit.herokuapp.com/'

UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\img')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Regras
def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end




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

    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES-------------------    

    return render_template("index.html", produtos=listaProdutos, categorias=listaCategorias, carrinho=ValorTotal, config = configuracao)


@app.route("/deletarProduto", methods=["POST", "GET"])
def deletarProduto():
    id = request.form['id']
    produtoMaintenance = ProdutoMaintenance()

    produto = Produto()
    getProduto = produto.get(int(id))

    if produtoMaintenance.delete(id):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER,secure_filename(getProduto.img)))
            return {"message":"Sucesso para deletar"}
        except Exception as error:
            if produtoMaintenance.delete(id):
                return {"message":"Sucesso para deletar"}
        
        


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

    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES------------------- 

    return render_template("produto.html",produtos = listaProdutos,categorias = listaCategorias, config=configuracao)

@app.route("/configuracoesGerais", methods=["POST", "GET"])
def configuracoesGerais():
    try:
        carrinho = session['cart']
    except Exception as error:
        carrinho = []
    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES-------------------   
    return render_template("configuracoesGerais.html", carrinho = carrinho, config = configuracao)    

@app.route("/gerenciaCategoria", methods=["POST", "GET"])
def gerenciaCategoria():
    categoria = CategoriaList()
    listaCategorias = categoria.get()
    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES------------------- 
    return render_template("categoria.html",categorias = listaCategorias, config = configuracao )

@app.route("/contato", methods=["POST", "GET"])
def contato():

     #-------------------Cookie Carrinho
     try:
         carrinho = session['cart']
     except Exception as error:
         carrinho = []
      #------------------CONFIGURAÇÕES-------------------
     configuracao = configModal.get_config()
     south_africa = timezone('Brazil/East')
     horaInicio = int(configuracao.horaInicio[0:2])
     minutoInicio = int(configuracao.horaInicio[3:5])
     horaFim = int(configuracao.horaFim[0:2])
     minutoFim = int(configuracao.horaFim[3:5])
     start = datetime.time(horaInicio, minutoInicio, 0)
     end = datetime.time(horaFim, minutoFim, 0)
     current = datetime.datetime.now(south_africa).time()
     if(time_in_range(start, end, current)):
         session['atividade'] = 1
     else:
         session['atividade'] = 0
     #----------------FIM-CONFIGURAÇÕES------------------- 
     return render_template("contato.html", config = configuracao )

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
    categoria = CategoriaList()
    listaCategorias = categoria.get()
    return jsonify({'htmlresponse': render_template('cadastroProduto.html', categorias = listaCategorias)})

#Tela de cadastro de categorias
@app.route("/addTelaCategoria", methods=["POST", "GET"])
def addTelaCategoria():
    return jsonify({'htmlresponse': render_template('cadastroCategoria.html')})

#Tela de cadastro de produto
@app.route("/telaUpdateProduto", methods=["POST", "GET"])
def telaUpdateProduto():
    produto = Produto()
    getProduto = produto.get(int(request.form['id']))
    categoria = CategoriaList()
    listaCategorias = categoria.get()
    return jsonify({'htmlresponse': render_template('atualizaProduto.html', categorias = listaCategorias, produto = getProduto)})

#Tela de atualização de categoria
@app.route("/telaUpdateCategoria", methods=["POST", "GET"])
def telaUpdateCategoria():
    categoria = CategoriaModel.find_by_id(request.form['id'])
    return jsonify({'htmlresponse': render_template('atualizaCategoria.html', categoria= categoria)})



#Tela de cadastro de endereço
@app.route("/addTelaEndereco", methods=["POST", "GET"])
def addTelaEndereco():
    return jsonify({'htmlresponse': render_template('cadastroEndereco.html')})

@app.route("/addTelaEnderecoPerfil", methods=["POST", "GET"])
def addTelaEnderecoPerfil():
    return jsonify({'htmlresponse': render_template('cadastroEnderecoPerfil.html')})

@app.route("/alterarProduto", methods=["POST", "GET"])
def alterarProduto():
    f = request.files['file']
    if f.filename != '':
        if 'file' not in request.files:
            return {"message":"No file part"},400

        typeFile = f.filename.split('.')[-1]
        if typeFile in ALLOWED_EXTENSIONS:
          ok = 'ok'
        else:
            return{"message":"Arquivo inválido"},400
        
        #remove o antigo e salva o novo
        try:
            os.remove(os.path.join(UPLOAD_FOLDER,secure_filename(request.form['img'])))
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        except Exception as error:
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
    else:
        f.filename = request.form['img']
 
    ProdutoModel.update_produto(request.form['categoria'],request.form['produto'],request.form['detalhe'],request.form['preco'],int(request.form['id']), f.filename)

    return {"Message":"Produto alterado com sucesso!"},200
# Rotina de criação de usuário

@app.route("/cadastroProduto", methods=["GET", "POST"])
def cadastroProduto():

    if request.form['categoria'] == '':
            return {"message":"Selecione ao menos uma categoria"},400
    
    f = request.files['file']
    if 'file' not in request.files:
        return {"message":"No file part"},400
        
    if f.filename == '':
        return {"message":"No selected file"},400
    
    typeFile = f.filename.split('.')[-1]
    if typeFile in ALLOWED_EXTENSIONS:
        pass
    else:
        return{"message":"Arquivo inválido"},400
    
    if ProdutoModel.find_by_img(f.filename):
      return{"message":"Imagem já está vinculada a um produto!"},400

        
        #Função para verificar se o usuário já existe no ban    co de dados
    if ProdutoModel.find_by_name(request.form['produto']):
            #caso não existir retorno a mensagem abaixo
        return {"message":"Essa categoria já existe no sistema!"}, 400
        #chamando a classe para gravar o usuário no banco de dados
    categoria = ProdutoModel(request.form['categoria'],request.form['produto'],request.form['detalhe'], request.form['preco'],f.filename)
    categoria.save_to_db()

    if f and allowed_file(f.filename):
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        

    return {"message":"Sucesso ao cadastrar o produto!"},201

    
@app.route("/cadastroCategoria", methods=["GET", "POST"])
def cadastroCategoria():
    
    if CategoriaModel.get_categoria(request.form['categoria']):
        return {"message":"Categoria já existente"},400

    newCategoria = request.form['categoria'].upper()

    categoria = CategoriaModel(newCategoria)
    categoria.save_to_db()
    return {"message":"Categoria criada com sucesso!"},200

@app.route("/alterarCategoria", methods=["GET", "POST"])
def alterarCategoria():
    
    currentCategory = CategoriaModel.get_categoria(request.form['categoria'])

    if currentCategory:
        if int(currentCategory.id) == int(request.form['id']):
            return {"message":"Categoria existente!"},400
    
    newCategoria = request.form['categoria'].upper()

    CategoriaModel.update_categoria(int(request.form['id']),newCategoria)
    return {"message":"Categoria alterada com sucesso!"},200


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


@app.route("/deletarCategoria", methods=["POST"])
def deletarCategoria():
    # Função post para registro de endereco
    try:
        if ProdutoModel.find_by_cat(int(request.form['id'])):
            return {"message":"Produtos possuem esta categoria, remova o produto da categoria!"},400
        CategoriaMaintenance.delete(int(request.form['id']))
        
        return {"message":"Sucesso ao deletar"},200
    except Exception as error:
        return {"message":"Erro para deletar"},400

    


@app.route("/backEndereco",  methods=["POST"])
def backEndereco():
    return redirect('/endereco')

@app.route("/confirmPedido",  methods=["POST"])
def confirmPedido():
    if session['cart'] == []:
        return {'message': 'Não existe produtos no carrinho'}, 400
    
    if session['atividade'] == 0:
        return {"message":"A temakeria está fechada"},400

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
        #------------------CONFIGURAÇÕES-------------------
        configuracao = configModal.get_config()
        south_africa = timezone('Brazil/East')
        horaInicio = int(configuracao.horaInicio[0:2])
        minutoInicio = int(configuracao.horaInicio[3:5])
        horaFim = int(configuracao.horaFim[0:2])
        minutoFim = int(configuracao.horaFim[3:5])
        start = datetime.time(horaInicio, minutoInicio, 0)
        end = datetime.time(horaFim, minutoFim, 0)
        current = datetime.datetime.now(south_africa).time()
        if(time_in_range(start, end, current)):
            session['atividade'] = 1
        else:
            session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES-------------------   
        # enderecos = EnderecoList()
        # # listaEndereco = endereco.get_enderecos_user(request.cookies.get("login", ""))
        # listaEndereco = enderecos.get(int(request.cookies.get("id", "")))
        return render_template("perfil.html",carrinho=carrinho, usuario = user, config = configuracao)    

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

        #------------------CONFIGURAÇÕES-------------------
        configuracao = configModal.get_config()
        south_africa = timezone('Brazil/East')
        horaInicio = int(configuracao.horaInicio[0:2])
        minutoInicio = int(configuracao.horaInicio[3:5])
        horaFim = int(configuracao.horaFim[0:2])
        minutoFim = int(configuracao.horaFim[3:5])
        start = datetime.time(horaInicio, minutoInicio, 0)
        end = datetime.time(horaFim, minutoFim, 0)
        current = datetime.datetime.now(south_africa).time()
        if(time_in_range(start, end, current)):
            session['atividade'] = 1
        else:
            session['atividade'] = 0
        #----------------FIM-CONFIGURAÇÕES-------------------   

        return render_template("enderecoPerfil.html",carrinho=carrinho, enderecos = listaEndereco, config = configuracao)


@app.route("/confirmProduto", methods=["POST", "GET"])
def confirmProduto():
    if request.method == 'POST':
        produto = Produto()
        onlyProduto = produto.get(request.form['userid'])
        employeelist = []
    return jsonify({'htmlresponse': render_template('confirmProduto.html', produto=onlyProduto)})


@app.route("/cart", methods=["POST", "GET"])
def cart():
    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES-------------------   

    # name = request.cookies.get('name')
    try:
        produtos = session['cart']
        qtdTotal = len(session['cart'])
        ValorTotal = 0
        ValorTotal = float(ValorTotal)
        for x in produtos:
            ValorTotal = ValorTotal + float(x['precoTotal'])
        
        ValorTotal += float(configuracao.taxaEntrega)
        session['valorTotal'] = float(ValorTotal) 
        return render_template("cart.html", carrinho=produtos, qtdCarrinho=qtdTotal, total= float(ValorTotal), config = configuracao)

    except Exception as error:
        return render_template("cart.html", carrinho='', qtdCarrinho=0, total=0,config = configuracao)
    # teste = simplejson.loads(str(name))
    # return render_template("cart.html")


@app.route("/addCart", methods=["POST", "GET"])
def addCart():
    id = request.args.get('id')
    if 'cart' not in session:
        session['cart'] = []  #
    cart_list = session['cart']

    if session['atividade'] == 0:
        return {"message":"A temakeria está fechada"},400

    count = 0
    for x in cart_list:
        count = count + 1
        if x['id'] == request.form['id']:
            return {'message': 'Este produto já foi adicionado ao carrinho'}, 400

    cart_list.append({"id": request.form['id'], "nome": request.form['nome'],
                     "qtd": request.form['qtd'], "preco": request.form['preco'], "precoTotal": request.form['precoTotal']  , "obs": request.form['obs']})
    session['cart'] = cart_list  #
    redirect('/')


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
    #Configurações iniciais
    configuracao = configModal.get_config()
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
    pedido= PedidoModal(idPedido,int(request.cookies.get("id", "")),idEndereco,idStatus,idFormaPagamento,valorTotal,None,None,configuracao.taxaEntrega)
    pedido.save_to_db()
    idPedido = str(idPedido)
    session['valorTotal'] = 0
    session['cart'] = []
    return {"message":"Pedido número "+idPedido+" Criado com sucesso"}

@app.route("/pedidos", methods=["POST", "GET"])
def pedidos():
    regPedido = PedidoList()
    try:
        carrinho = session['cart']
    except Exception as error:
        carrinho = []
    
    pedidos = regPedido.getUser(request.cookies.get("id", ""))
    newlist = sorted(pedidos, key=lambda d: d['id'], reverse=True) 

    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES------------------- 

    return render_template("pedidos.html", carrinho = carrinho, AllPedidos = newlist, data = 0, config = configuracao )
    # return render_template("pedidos.html", carrinho = carrinho, AllPedidos = newlist, enderecos = endereco, Allstatus = status, formaPagamentos = listaPagamentos, aux_produto=aux_produto )

@app.route("/alterarConfiguracoes", methods=["POST", "GET"])
def alterarConfiguracoes():
    if configModal.update_config(request.form['horaInicio'],request.form['horaFim'],request.form['taxaEntrega'],request.form['tempoEntrega']):
        #------------------CONFIGURAÇÕES-------------------
        configuracao = configModal.get_config()
        south_africa = timezone('Brazil/East')
        horaInicio = int(request.form['horaInicio'][0:2])
        minutoInicio = int(request.form['horaInicio'][3:5])
        horaFim = int(request.form['horaFim'][0:2])
        minutoFim = int(request.form['horaFim'][3:5])
        start = datetime.time(horaInicio, minutoInicio, 0)
        end = datetime.time(horaFim, minutoFim, 0)
        current = datetime.datetime.now(south_africa).time()
        if(time_in_range(start, end, current)):
            session['atividade'] = 1
        else:
            session['atividade'] = 0
        #----------------FIM-CONFIGURAÇÕES------------------- 

        return {"message":"Sucesso ao alterar as configurações"},200

@app.route("/gerenciaPedidos", methods=["POST", "GET"])
def gerenciaPedidos():
    regPedido = PedidoList()
    status = Status()
    try:
        carrinho = session['cart']
    except Exception as error:
        carrinho = []
    
    try:
        if request.form['id']:
            pedidos = regPedido.getStatus(request.cookies.get("id", "request.form['id']"))
    except Exception as error:
        pedidos = regPedido.getStatus(1)
    
    
    newlist = sorted(pedidos, key=lambda d: d['id'], reverse=True) 
    
    #------------------CONFIGURAÇÕES-------------------
    configuracao = configModal.get_config()
    south_africa = timezone('Brazil/East')
    horaInicio = int(configuracao.horaInicio[0:2])
    minutoInicio = int(configuracao.horaInicio[3:5])
    horaFim = int(configuracao.horaFim[0:2])
    minutoFim = int(configuracao.horaFim[3:5])
    start = datetime.time(horaInicio, minutoInicio, 0)
    end = datetime.time(horaFim, minutoFim, 0)
    current = datetime.datetime.now(south_africa).time()
    if(time_in_range(start, end, current)):
        session['atividade'] = 1
    else:
        session['atividade'] = 0
    #----------------FIM-CONFIGURAÇÕES------------------- 

    return render_template("gerenciaPedidos.html", carrinho = carrinho, AllPedidos = newlist, data = 0, config = configuracao )
    # return render_template("pedidos.html", carrinho = carrinho, AllPedidos = newlist, enderecos = endereco, Allstatus = status, formaPagamentos = listaPagamentos, aux_produto=aux_produto )

@app.route("/alterarStatusPedido", methods=["POST", "GET"])
def alterarStatusPedido():

    PedidoModal.update_produto(request.form['id'],request.form['idStatus'])
    return {"message":"Pedido alterado com sucesso!"},200
    

@app.route("/addPedidosContainer", methods=["POST", "GET"])
def addPedidosContainer():
    regPedido = PedidoList()
    try:
        if request.form['id']:
            pedidos = regPedido.getStatus(request.form['id'])
    except Exception as error:
        pedidos = regPedido.getStatus(1)
    
    newlist = sorted(pedidos, key=lambda d: d['id'], reverse=True) 
    return jsonify({'htmlresponse': render_template('tabelaPedidos.html', AllPedidos = newlist)})

def allowed_file(filename):    
    return '.' in filename and filename.split('.', 1)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run( host="0.0.0.0", port=5000, debug=True)
    # http_erver = WSGIServer(('177.198.93.24', 5000), app)
    # http_server.serve_forever()
