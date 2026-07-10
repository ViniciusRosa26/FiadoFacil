from util.database.connection import get_connection
from model.ClienteModel import ClienteModel

class ClienteRepository:

    def salvar(self, cliente):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO cliente(nome, apelido, data_criacao, saldo_devedor)
            VALUES (?, ?, ?, ?)
            """,
            (
                cliente.nome,
                cliente.apelido,
                cliente.data_criacao,
                cliente.saldo_devedor
            )
        )

        cliente.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cliente

    def buscar_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, apelido, data_criacao, saldo_devedor FROM cliente")
        rows = cursor.fetchall()

        conn.close()
        return [self._row_to_model(row) for row in rows]

    def buscar_por_id(self, cliente_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, apelido, data_criacao, saldo_devedor FROM cliente WHERE id = ?",
            (cliente_id,)
        )
        row = cursor.fetchone()
        conn.close()

        return self._row_to_model(row) if row else None

    def atualizar(self, cliente):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE cliente
            SET nome = ?, apelido = ?, data_criacao = ?, saldo_devedor = ?
            WHERE id = ?
            """,
            (
                cliente.nome,
                cliente.apelido,
                cliente.data_criacao,
                cliente.saldo_devedor,
                cliente.id
            )
        )

        conn.commit()
        conn.close()
        return cliente

    def deletar(self, cliente_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cliente WHERE id = ?", (cliente_id,))
        deleted = cursor.rowcount

        conn.commit()
        conn.close()
        return deleted > 0

    def _row_to_model(self, row):
        if not row:
            return None

        id, nome, apelido, data_criacao, saldo_devedor = row
        return ClienteModel(id=id, nome=nome, apelido=apelido, data_criacao=data_criacao, saldo_devedor=saldo_devedor)
