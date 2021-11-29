from logging import NullHandler
from database import database
import hashlib
import os



class configModal():

    def __init__(self, horaInicial, horaFinal, taxaEntrega, tempoEntrega):
        self.horaInicial = horaInicial
        self.horaFinal        = horaFinal
        self.taxaEntrega     = taxaEntrega
        self.tempoEntrega       = tempoEntrega
        
        

    #Ao criar verificar se o categoria já existe
    @classmethod
    def get_config(self):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("SELECT * FROM configuracoes")
        registro = cur.fetchone()
        if (registro): 
            config = self
            config.horaInicio = registro[1]
            config.horaFim = registro[2]
            config.taxaEntrega = registro[3]
            config.tempoEntrega = registro[4]
            cur.close()
            return config
        config = False
        cur.close()
        return config


    @classmethod
    def update_config(self,horaInicio, horaFim, taxaEntrega, tempoEntrega):
        connectorDatabase = database()
        connect = connectorDatabase.abrirConexao()
        cur = connect.cursor()
        cur.execute("UPDATE configuracoes SET id = 1,horario_inicio =%s, horario_fim =%s, valor_frete= %s, tempo_entrega= %s",(horaInicio,horaFim,taxaEntrega, tempoEntrega))
        connect.commit()
        cur.close()
        return "Sucesso"
        
