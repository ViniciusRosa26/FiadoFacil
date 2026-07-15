import unittest
from repository.ClienteRepository import ClienteRepository
from model.ClienteModel import ClienteModel

class test_cliente_repository(unittest.TestCase):
    
        def setUp(self):
            self.repository = ClienteRepository()

        def test_salvar_cliente(self):
            cliente = ClienteModel(
                nome= "vinicius",
                apelido= "vini",
                data_criacao= "2026-07-24",
                saldo_devedor= 0

            )

            cliente_salvo = self.repository.salvar(cliente)

            self.assertIsNotNone(cliente_salvo.id)
