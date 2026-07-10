from datetime import datetime
from model.ClienteModel import ClienteModel
from repository.ClienteRepository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def _gerar_data_formatada(self):
        return datetime.now().strftime("%d/%m/%y %H:%M")

    def criar(self):
        print("\n--- CADASTRAR NOVO CLIENTE ---")
        nome = input("Digite o nome do cliente: ").strip()
        apelido = input("Digite o apelido do cliente: ").strip()

        data_atual = self._gerar_data_formatada()

        novo_cliente = ClienteModel(
            nome=nome,
            apelido=apelido,
            data_criacao=data_atual,
            saldo_devedor=0.0,
        )

        self.repository.salvar(novo_cliente)
        print(f"Cliente '{apelido}' cadastrado com sucesso em {data_atual}!")
        return novo_cliente

    def listar(self):
        print("\n--- LISTA DE CLIENTES ---")
        clientes = self.repository.buscar_todos()
        for c in clientes:
            print(
                f"ID: {c.id} | Nome: {c.nome} ({c.apelido}) | "
                f"Dívida: R${c.saldo_devedor:.2f} | Criado em: {c.data_criacao}"
            )
        return clientes

    def atualizar(self, cliente_id):
        print("\n--- ATUALIZAR CLIENTE ---")
        cliente = self.repository.buscar_por_id(cliente_id)
        if cliente:
            nome = input(f"Novo nome ({cliente.nome}): ").strip() or cliente.nome
            apelido = input(f"Novo apelido ({cliente.apelido}): ").strip() or cliente.apelido
            cliente.nome = nome
            cliente.apelido = apelido
            self.repository.atualizar(cliente)
            print("Cliente atualizado com sucesso!")
            return cliente
        print("Cliente não encontrado.")
        return None

    def deletar(self, cliente_id):
        print("\n--- DELETAR CLIENTE ---")
        if self.repository.deletar(cliente_id):
            print("Cliente removido com sucesso!")
            return True

        print("Não foi possível remover o cliente.")
        return False
