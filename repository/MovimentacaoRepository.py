from util.database.connection import get_connection
from model.MovimentacaoModel import MovimentacaoModel

class MovimentacaoRepository:
    def salvar(self, movimentacao):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO movimentacao(cliente_id, descricao, valor, tipo, data_hora)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                movimentacao.cliente_id,
                movimentacao.descricao,
                movimentacao.valor,
                movimentacao.tipo,
                movimentacao.data_hora,
            )
        )

        movimentacao.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return movimentacao

    def buscar_por_cliente(self, cliente_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, cliente_id, descricao, valor, tipo, data_hora FROM movimentacao WHERE cliente_id = ? ORDER BY id",
            (cliente_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_model(row) for row in rows]

    def _row_to_model(self, row):
        if not row:
            return None

        id, cliente_id, descricao, valor, tipo, data_hora = row
        return MovimentacaoModel(
            id=id,
            cliente_id=cliente_id,
            valor=valor,
            data_hora=data_hora,
            tipo=tipo,
            descricao=descricao,
        )
