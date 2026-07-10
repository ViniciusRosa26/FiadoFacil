class MovimentacaoModel:
    def __init__(self,id,cliente_id,valor,dataHora,tipoDeMovimentacao):
        self.id = id
        self.cliente_id = cliente_id
        self.valor = valor
        self.dataHora = dataHora
        self.tipoDeMovimentacao = tipoDeMovimentacao