class MovimentacaoModel:
    def __init__(self, id=None, cliente_id=None, valor=0.0, data_hora=None, tipo=None, descricao=None):
        self.id = id
        self.cliente_id = cliente_id
        self.valor = valor
        self.data_hora = data_hora
        self.tipo = tipo
        self.descricao = descricao

    @property
    def dataHora(self):
        return self.data_hora

    @dataHora.setter
    def dataHora(self, value):
        self.data_hora = value

    @property
    def tipoDeMovimentacao(self):
        return self.tipo

    @tipoDeMovimentacao.setter
    def tipoDeMovimentacao(self, value):
        self.tipo = value