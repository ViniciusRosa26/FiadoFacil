from datetime import datetime
from model.MovimentacaoModel import MovimentacaoModel
from model.ClienteModel import ClienteModel
from repository.MovimentacaoRepository import MovimentacaoRepository
from repository.ClienteRepository import ClienteRepository
from enums.TipoDeMovimentacaoEnum import TipoDeMovimentacaoEnum


class MovimentacaoService:
    def __init__(self):
        self.repository = MovimentacaoRepository()
        self.cliente_repository = ClienteRepository()

    def _gerar_data_formatada(self):
        return datetime.now().strftime("%d/%m/%y %H:%M")

    def listar_por_cliente(self, cliente_id):
        return self.repository.buscar_por_cliente(cliente_id)

    def criar_movimentacao_divida(self, cliente: ClienteModel, valor: float):
        if valor <= 0:
            raise ValueError("O valor da dívida deve ser maior que zero.")

        data_movimentacao = self._gerar_data_formatada()
        cliente.saldo_devedor += valor
        self.cliente_repository.atualizar(cliente)

        nova_movi = MovimentacaoModel(
            cliente_id=cliente.id,
            valor=valor,
            tipo=TipoDeMovimentacaoEnum.DEBITO.value,
            data_hora=data_movimentacao,
            descricao="Dívida criada",
        )

        self.repository.salvar(nova_movi)
        return nova_movi

    def abater_total_saldo(self, cliente: ClienteModel):
        if cliente.saldo_devedor <= 0:
            raise ValueError(f"O cliente {cliente.apelido} não possui dívida ativa para abater.")

        valor_abatido = cliente.saldo_devedor
        data_movimentacao = self._gerar_data_formatada()
        cliente.saldo_devedor = 0.0
        self.cliente_repository.atualizar(cliente)

        nova_movi = MovimentacaoModel(
            cliente_id=cliente.id,
            valor=valor_abatido,
            tipo=TipoDeMovimentacaoEnum.CREDITO.value,
            data_hora=data_movimentacao,
            descricao="Abatimento total",
        )

        self.repository.salvar(nova_movi)
        return nova_movi

    def abater_parcial_saldo(self, cliente: ClienteModel, valor_pagamento: float):
        if valor_pagamento <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")

        if valor_pagamento > cliente.saldo_devedor:
            raise ValueError(
                f"O valor informado (R${valor_pagamento:.2f}) é maior que a dívida atual "
                f"(R${cliente.saldo_devedor:.2f})."
            )

        data_movimentacao = self._gerar_data_formatada()
        cliente.saldo_devedor -= valor_pagamento
        self.cliente_repository.atualizar(cliente)

        nova_movi = MovimentacaoModel(
            cliente_id=cliente.id,
            valor=valor_pagamento,
            tipo=TipoDeMovimentacaoEnum.CREDITO.value,
            data_hora=data_movimentacao,
            descricao="Abatimento parcial",
        )

        self.repository.salvar(nova_movi)
        return nova_movi
