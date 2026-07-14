from datetime import datetime
from model.ClienteModel import ClienteModel
from repository.ClienteRepository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def _gerar_data_formatada(self):
        return datetime.now().strftime("%d/%m/%y %H:%M")

    def criar(self, nome, apelido):
        nome = nome.strip()
        apelido = apelido.strip()

        if not nome:
            raise ValueError("O nome do cliente é obrigatório.")

        data_atual = self._gerar_data_formatada()

        novo_cliente = ClienteModel(
            nome=nome,
            apelido=apelido,
            data_criacao=data_atual,
            saldo_devedor=0.0,
        )

        self.repository.salvar(novo_cliente)
        return novo_cliente

    def listar(self):
        return self.repository.buscar_todos()

    def atualizar(self, cliente_id, nome=None, apelido=None):
        cliente = self.repository.buscar_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente com id {cliente_id} não encontrado.")

        if nome:
            cliente.nome = nome.strip()
        if apelido:
            cliente.apelido = apelido.strip()

        self.repository.atualizar(cliente)
        return cliente

    def deletar(self, cliente_id):
        return self.repository.deletar(cliente_id)