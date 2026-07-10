class ClienteModel:
    def __init__(self, id=None, nome=None, apelido=None, data_criacao=None, saldo_devedor=0.0):
        self.id = id
        self.nome = nome
        self.apelido = apelido
        self.data_criacao = data_criacao
        self.saldo_devedor = saldo_devedor

    @property
    def dataDeCriacao(self):
        return self.data_criacao

    @dataDeCriacao.setter
    def dataDeCriacao(self, value):
        self.data_criacao = value
