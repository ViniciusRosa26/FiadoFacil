import tkinter as tk
from tkinter import messagebox

from view.TelaClientes import TelaClientes
from service.ClienteService import ClienteService
from service.MovimentacaoService import MovimentacaoService
from util.database.init_db import criar_tabelas


def montar_lista_para_tela(clientes, movimentacao_service):
    """
    Converte os objetos ClienteModel (do banco) no formato de dicionário
    que a TelaClientes espera, já buscando a ÚLTIMA movimentação de cada
    cliente pra preencher data/hora/valor de verdade no card.
    """
    lista = []
    for c in clientes:
        movimentacoes = movimentacao_service.listar_por_cliente(c.id)

        if movimentacoes:
            ultima = movimentacoes[-1]  # a mais recente fica por último na lista
            data_parte, hora_parte = ultima.data_hora.split(" ")
            dia, mes, _ano = data_parte.split("/")
            ultima_data = f"{dia}/{mes}"
            ultima_hora = hora_parte
            ultima_valor = ultima.valor
        else:
            ultima_data = "--/--"
            ultima_hora = "--:--"
            ultima_valor = 0.0

        lista.append({
            "id": c.id,
            "nome": c.nome,
            "apelido": c.apelido,
            "saldo_devedor": c.saldo_devedor,
            "ultima_data": ultima_data,
            "ultima_hora": ultima_hora,
            "ultima_valor": ultima_valor,
        })
    return lista


def abrir_dialogo_valor(janela_pai, titulo, texto_botao, ao_confirmar):
    """
    Janela pequena e genérica só com um campo numérico e um botão.
    Usada tanto pra 'Registrar Venda' quanto pra 'Abater Parte' —
    a única diferença entre os dois é o texto e o que 'ao_confirmar' faz.
    """
    janela = tk.Toplevel(janela_pai)
    janela.title(titulo)
    janela.geometry("280x160")
    janela.grab_set()

    tk.Label(janela, text=titulo).pack(pady=(16, 4))
    tk.Label(janela, text="Valor (R$):").pack(pady=(8, 4))
    entry_valor = tk.Entry(janela, width=20)
    entry_valor.pack()
    entry_valor.focus()

    label_erro = tk.Label(janela, text="", fg="red", wraplength=240)
    label_erro.pack(pady=(8, 0))

    def confirmar():
        texto_valor = entry_valor.get().strip().replace(",", ".")
        try:
            valor = float(texto_valor)
        except ValueError:
            label_erro.config(text="Digite um número válido (ex: 25.50).")
            return

        try:
            ao_confirmar(valor)
            janela.destroy()
        except ValueError as erro:
            label_erro.config(text=str(erro))

    tk.Button(janela, text=texto_botao, bg="#3aa15a", fg="white",
              command=confirmar).pack(pady=12)


def main():
    # Garante que as tabelas existem antes de qualquer outra coisa rodar.
    criar_tabelas()

    cliente_service = ClienteService()
    movimentacao_service = MovimentacaoService()

    def carregar_clientes():
        return montar_lista_para_tela(cliente_service.listar(), movimentacao_service)

    def ao_ver_historico(cliente):
        movimentacoes = movimentacao_service.listar_por_cliente(cliente["id"])

        janela_historico = tk.Toplevel(janela)
        janela_historico.title(f"Histórico de {cliente['nome']}")
        janela_historico.geometry("420x360")

        if not movimentacoes:
            tk.Label(janela_historico, text="Nenhuma movimentação registrada ainda.").pack(
                pady=20
            )
            return

        cabecalho = tk.Frame(janela_historico)
        cabecalho.pack(fill="x", padx=12, pady=(12, 4))
        for texto, largura in (("Data", 8), ("Hora", 8), ("Tipo", 12), ("Valor", 10)):
            tk.Label(cabecalho, text=texto, font=("Segoe UI", 9, "bold"), width=largura,
                      anchor="w").pack(side="left")

        area_lista = tk.Frame(janela_historico)
        area_lista.pack(fill="both", expand=True, padx=12)

        # Mostra da mais recente pra mais antiga
        for movi in reversed(movimentacoes):
            data_parte, hora_parte = movi.data_hora.split(" ")
            dia, mes, _ano = data_parte.split("/")

            linha = tk.Frame(area_lista)
            linha.pack(fill="x")
            tk.Label(linha, text=f"{dia}/{mes}", width=8, anchor="w").pack(side="left")
            tk.Label(linha, text=hora_parte, width=8, anchor="w").pack(side="left")
            tk.Label(linha, text=movi.tipo, width=12, anchor="w").pack(side="left")
            cor = "#3aa15a" if movi.tipo == "pagamento" else "#c0392b"
            tk.Label(linha, text=f"R$ {movi.valor:.2f}", width=10, anchor="w",
                      fg=cor).pack(side="left")

    def ao_criar_cliente(nome, apelido):
        cliente_service.criar(nome, apelido)
        tela.atualizar_clientes(carregar_clientes())

    def ao_editar_cliente(cliente_id, nome, apelido):
        cliente_service.atualizar(cliente_id, nome=nome, apelido=apelido)
        tela.atualizar_clientes(carregar_clientes())

    def ao_excluir_cliente(cliente_id):
        cliente_service.deletar(cliente_id)
        tela.atualizar_clientes(carregar_clientes())

    def ao_registrar_venda(cliente):
        def confirmar(valor):
            cliente_model = cliente_service.buscar_por_id(cliente["id"])
            movimentacao_service.criar_movimentacao_divida(cliente_model, valor)
            tela.atualizar_clientes(carregar_clientes())

        abrir_dialogo_valor(
            janela, f"Nova venda para {cliente['nome']}", "Registrar", confirmar
        )

    def ao_abater_tudo(cliente):
        confirmou = messagebox.askyesno(
            "Confirmar",
            f"Abater TODA a dívida de {cliente['nome']} "
            f"(R$ {cliente['saldo_devedor']:.2f})?",
        )
        if not confirmou:
            return

        try:
            cliente_model = cliente_service.buscar_por_id(cliente["id"])
            movimentacao_service.abater_total_saldo(cliente_model)
            tela.atualizar_clientes(carregar_clientes())
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def ao_abater_parte(cliente):
        def confirmar(valor):
            cliente_model = cliente_service.buscar_por_id(cliente["id"])
            movimentacao_service.abater_parcial_saldo(cliente_model, valor)
            tela.atualizar_clientes(carregar_clientes())

        abrir_dialogo_valor(
            janela, f"Abater parte da dívida de {cliente['nome']}", "Abater", confirmar
        )

    janela = tk.Tk()
    janela.title("Fiado Fácil")
    janela.geometry("1000x600")

    tela = TelaClientes(
        janela,
        carregar_clientes(),
        ao_registrar_venda,
        ao_abater_tudo,
        ao_abater_parte,
        on_criar_cliente=ao_criar_cliente,
        on_editar_cliente=ao_editar_cliente,
        on_excluir_cliente=ao_excluir_cliente,
        on_historico_cliente=ao_ver_historico,
    )
    tela.pack(fill="both", expand=True)

    janela.mainloop()


if __name__ == "__main__":
    main()