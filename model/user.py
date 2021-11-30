from logging import NullHandler
from database import database
import hashlib
import os



class UserModel():

    def __init__(self, id, username, password,nome,ddd,telefone):
        self.id       = id
        self.username = username
        self.password = password
        self.nome = nome
        self.ddd = ddd
        self.telefone = telefone
        
    #Gravar user no DB
    def save_to_db(self):
        id = int()
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("INSERT INTO usuario(email,senha,nome,ddd,telefone,tipo) VALUES (%s,%s,%s,%s,%s,%s)", (self.username, self.password, self.nome, self.ddd, self.telefone,"cliente"))
        connect.commit()
        cur.close()

    #Ao criar verificar se o usuário já existe
    @classmethod
    def find_by_username(self, email):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT id, email, senha, nome, ddd, telefone, tipo FROM usuario WHERE email=%s",(email,))
        username = cur.fetchone()
        if (username): 
            user = self
            user.id = username[0]
            user.username = username[1]
            user.password = username[2]
            user.nome = username[3]
            user.ddd = username[4]
            user.telefone = username[5]
            user.tipo = username[6]
            return user
        username = False


    @classmethod
    def find_by_id(cls, id):
        id = str(id)
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT id FROM usuario WHERE id='" + id + "'")
        username = cur.fetchone()
        return username

    @classmethod
    def update_by_id(self,id,nome,ddd,telefone):
        connectorDatabase = database()
        id = int(id)
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("UPDATE usuario SET nome =%s, ddd= %s, telefone = %s WHERE id= %s",(nome,ddd,telefone, id))
        connect.commit()
        cur.close()
    
    @classmethod
    def update_pass(self,id,senha):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("UPDATE usuario SET senha =%s WHERE id =%s",(senha,id))
        connect.commit()
        cur.close()


class pwdHash():
    def __init__(self, password):
        self.password = password
        self.salt = os.urandom(16) # Remember this
        self.key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        self.password.encode('utf-8'), # Convert the password to bytes
        self.salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
    

    def setEncriptPass(self, password):
        # Encryption with AES-256-CBC
        encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(self.key, self.salt))
        ciphertext = encrypter.feed(password.encode('utf8'))
        ciphertext += encrypter.feed()
        return ciphertext
    
    def getDecriptPass(self, password):
        # Decryption with AES-256-CBC
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(password))
        decryptedData = decrypter.feed(password)
        decryptedData += decrypter.feed()
        return decryptedData
