"""
Tela de listagem de clientes (estilo "cards de papel").

Conceitos de Tkinter usados aqui, comentados pra quem tá aprendendo:
- Frame: uma "caixa" que agrupa outros widgets (como uma <div> no HTML)
- Grid: organiza widgets em linhas e colunas dentro de um Frame
- bind("<Enter>", funcao) / bind("<Leave>", funcao): dispara uma função
  quando o mouse ENTRA ou SAI de cima de um widget (é o "hover")
- pack_forget() / grid_forget(): esconde um widget sem destruí-lo
  (fica na memória, só não aparece na tela)
"""

import tkinter as tk
from tkinter import font as tkfont

# ---------- Configurações visuais (fica fácil de ajustar tudo num lugar só) ----------
COR_FUNDO = "#2b2b2b"
COR_CARD = "#f5e6c8"          # cor "papel"
COR_CARD_BORDA = "#c9a86a"
COR_TEXTO_CARD = "#3a2f1c"
COR_DIVIDA = "#c0392b"
COR_BOTAO_VENDA = "#e6893a"
COR_BOTAO_ABATER_TUDO = "#3aa15a"
COR_BOTAO_ABATER_PARTE = "#3a7bd5"
COR_TOPO = "#1f1f1f"

CLIENTES_POR_PAGINA = 8
COLUNAS = 4


class CardCliente(tk.Frame):
    """
    Representa UM card de cliente na grade.

    cliente: dicionário com as chaves
        id, nome, saldo_devedor, ultima_data ("DD/MM"), ultima_hora ("HH:MM"), ultima_valor
    callbacks: dicionário de funções (on_selecionar, on_nova_venda, on_abater_tudo, on_abater_parte)
        cada uma recebe o cliente como argumento
    """

    def __init__(self, parent, cliente, callbacks):
        super().__init__(parent, bg=COR_CARD, highlightbackground=COR_CARD_BORDA,
                          highlightthickness=2, bd=0, padx=10, pady=8)
        self.cliente = cliente
        self.callbacks = callbacks

        fonte_nome = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        fonte_normal = tkfont.Font(family="Segoe UI", size=9)

        tk.Label(self, text=cliente["nome"], bg=COR_CARD, fg=COR_TEXTO_CARD,
                  font=fonte_nome, anchor="w").pack(fill="x")

        tk.Label(self, text=f"R$ {cliente['saldo_devedor']:.2f}", bg=COR_CARD,
                  fg=COR_DIVIDA, font=fonte_nome, anchor="w").pack(fill="x")

        # Tabela simples: data + hora + valor da última movimentação
        linha_data = f"{cliente['ultima_data']}  {cliente['ultima_hora']}"
        tk.Label(self, text=linha_data, bg=COR_CARD, fg=COR_TEXTO_CARD,
                  font=fonte_normal, anchor="w").pack(fill="x")
        tk.Label(self, text=f"Valor: R$ {cliente['ultima_valor']:.2f}", bg=COR_CARD,
                  fg=COR_TEXTO_CARD, font=fonte_normal, anchor="w").pack(fill="x")

        # Painel de ações que só aparece no hover (começa escondido)
        self.painel_acoes = tk.Frame(self, bg=COR_CARD)
        self._criar_botoes_acao()

        # Clicar no card (fora dos botões) seleciona o cliente pro painel de baixo
        self.bind("<Button-1>", self._ao_clicar)
        for widget in self.winfo_children():
            if widget is not self.painel_acoes:
                widget.bind("<Button-1>", self._ao_clicar)

        # Hover: mostra/esconde o painel de ações
        self.bind("<Enter>", self._mostrar_acoes)
        self.bind("<Leave>", self._esconder_acoes)

    def _criar_botoes_acao(self):
        fonte_botao = tkfont.Font(family="Segoe UI", size=8, weight="bold")

        tk.Button(
            self.painel_acoes, text="Registrar Venda", bg=COR_BOTAO_VENDA, fg="white",
            font=fonte_botao, relief="flat", padx=4,
            command=lambda: self.callbacks["on_nova_venda"](self.cliente),
        ).pack(side="left", expand=True, fill="x", padx=2)

        tk.Button(
            self.painel_acoes, text="Abater Tudo", bg=COR_BOTAO_ABATER_TUDO, fg="white",
            font=fonte_botao, relief="flat", padx=4,
            command=lambda: self.callbacks["on_abater_tudo"](self.cliente),
        ).pack(side="left", expand=True, fill="x", padx=2)

        tk.Button(
            self.painel_acoes, text="Abater Parte", bg=COR_BOTAO_ABATER_PARTE, fg="white",
            font=fonte_botao, relief="flat", padx=4,
            command=lambda: self.callbacks["on_abater_parte"](self.cliente),
        ).pack(side="left", expand=True, fill="x", padx=2)

    def _mostrar_acoes(self, event=None):
        self.painel_acoes.pack(fill="x", pady=(6, 0))

    def _esconder_acoes(self, event=None):
        self.painel_acoes.pack_forget()

    def _ao_clicar(self, event=None):
        self.callbacks["on_selecionar"](self.cliente)


class PainelConfig(tk.Frame):
    """
    Painel de configuração no topo — hoje é só um botão de engrenagem
    que abre um menuzinho com Editar / Excluir / Histórico do cliente
    SELECIONADO no momento. (A lógica de editar/excluir/histórico de
    verdade você liga depois, chamando o ClienteService/MovimentacaoService.)
    """

    def __init__(self, parent, get_cliente_selecionado, on_criar_cliente,
                 on_editar_cliente=None, on_excluir_cliente=None, on_historico_cliente=None):
        super().__init__(parent, bg=COR_TOPO)
        self.get_cliente_selecionado = get_cliente_selecionado
        self.on_criar_cliente = on_criar_cliente
        self.on_editar_cliente = on_editar_cliente
        self.on_excluir_cliente = on_excluir_cliente
        self.on_historico_cliente = on_historico_cliente

        tk.Label(self, text="Fiado Fácil", bg=COR_TOPO, fg="#e6b84a",
                  font=tkfont.Font(family="Segoe UI", size=16, weight="bold")).pack(
            side="left", padx=12, pady=8
        )

        self.busca_var = tk.StringVar()
        tk.Entry(self, textvariable=self.busca_var, width=30).pack(
            side="left", padx=8, pady=8
        )

        tk.Button(self, text="+", command=self._abrir_janela_novo_cliente, relief="flat",
                   bg=COR_BOTAO_ABATER_TUDO, fg="white", font=("Segoe UI", 12, "bold"),
                   width=3).pack(side="left", padx=4, pady=8)

        tk.Button(self, text="\u2699", command=self._abrir_menu_config, relief="flat",
                   bg=COR_TOPO, fg="white", font=("Segoe UI", 14)).pack(
            side="right", padx=12, pady=8
        )

    def _abrir_janela_novo_cliente(self):
        """
        Abre uma janela secundária (Toplevel) só com dois campos e um
        botão de salvar. Toplevel é como um "popup" que fica por cima
        da janela principal, mas é independente dela.
        """
        janela = tk.Toplevel(self)
        janela.title("Novo Cliente")
        janela.geometry("300x180")
        janela.grab_set()  # trava o foco nessa janela até ela fechar

        tk.Label(janela, text="Nome:").pack(pady=(16, 4))
        entry_nome = tk.Entry(janela, width=30)
        entry_nome.pack()
        entry_nome.focus()

        tk.Label(janela, text="Apelido:").pack(pady=(12, 4))
        entry_apelido = tk.Entry(janela, width=30)
        entry_apelido.pack()

        label_erro = tk.Label(janela, text="", fg="red")
        label_erro.pack(pady=(8, 0))

        def salvar():
            nome = entry_nome.get().strip()
            apelido = entry_apelido.get().strip()
            try:
                self.on_criar_cliente(nome, apelido)
                janela.destroy()
            except ValueError as erro:
                label_erro.config(text=str(erro))

        tk.Button(janela, text="Salvar", bg=COR_BOTAO_ABATER_TUDO, fg="white",
                   command=salvar).pack(pady=12)

    def _abrir_menu_config(self):
        cliente = self.get_cliente_selecionado()
        menu = tk.Menu(self, tearoff=0)
        if cliente is None:
            menu.add_command(label="Selecione um cliente primeiro", state="disabled")
        else:
            menu.add_command(label=f"Editar {cliente['nome']}",
                              command=lambda: self._abrir_janela_editar(cliente))
            menu.add_command(label=f"Excluir {cliente['nome']}",
                              command=lambda: self._confirmar_exclusao(cliente))
            menu.add_command(
                label=f"Histórico de {cliente['nome']}",
                command=lambda: (
                    self.on_historico_cliente(cliente)
                    if self.on_historico_cliente
                    else print("TODO: nenhum callback de histórico configurado", cliente)
                ),
            )
        menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())

    def _abrir_janela_editar(self, cliente):
        """
        Igual a janela de 'Novo Cliente', mas os campos já vêm preenchidos
        com os dados atuais do cliente selecionado.
        """
        if self.on_editar_cliente is None:
            print("TODO: nenhum callback de editar configurado", cliente)
            return

        janela = tk.Toplevel(self)
        janela.title(f"Editar {cliente['nome']}")
        janela.geometry("300x180")
        janela.grab_set()

        tk.Label(janela, text="Nome:").pack(pady=(16, 4))
        entry_nome = tk.Entry(janela, width=30)
        entry_nome.insert(0, cliente["nome"])
        entry_nome.pack()
        entry_nome.focus()

        tk.Label(janela, text="Apelido:").pack(pady=(12, 4))
        entry_apelido = tk.Entry(janela, width=30)
        entry_apelido.insert(0, cliente.get("apelido", ""))
        entry_apelido.pack()

        label_erro = tk.Label(janela, text="", fg="red")
        label_erro.pack(pady=(8, 0))

        def salvar():
            nome = entry_nome.get().strip()
            apelido = entry_apelido.get().strip()
            try:
                self.on_editar_cliente(cliente["id"], nome, apelido)
                janela.destroy()
            except ValueError as erro:
                label_erro.config(text=str(erro))

        tk.Button(janela, text="Salvar alterações", bg=COR_BOTAO_ABATER_PARTE, fg="white",
                   command=salvar).pack(pady=12)

    def _confirmar_exclusao(self, cliente):
        if self.on_excluir_cliente is None:
            print("TODO: nenhum callback de excluir configurado", cliente)
            return

        janela = tk.Toplevel(self)
        janela.title("Confirmar exclusão")
        janela.geometry("300x140")
        janela.grab_set()

        tk.Label(
            janela,
            text=f"Excluir {cliente['nome']} definitivamente?\nEssa ação não pode ser desfeita.",
            wraplength=260, justify="center",
        ).pack(pady=(20, 12))

        frame_botoes = tk.Frame(janela)
        frame_botoes.pack()

        def confirmar():
            self.on_excluir_cliente(cliente["id"])
            janela.destroy()

        tk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(
            side="left", padx=8
        )
        tk.Button(frame_botoes, text="Excluir", bg=COR_DIVIDA, fg="white",
                   command=confirmar).pack(side="left", padx=8)


class TelaClientes(tk.Frame):
    """
    Tela principal: grade de cards (8 por página) + paginação + painel
    do cliente selecionado (parecido com a barra de baixo da imagem).
    """

    def __init__(self, parent, clientes, on_nova_venda, on_abater_tudo, on_abater_parte,
                 on_criar_cliente=None, on_editar_cliente=None, on_excluir_cliente=None,
                 on_historico_cliente=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.clientes = clientes
        self.pagina_atual = 0
        self.cliente_selecionado = None
        self.on_criar_cliente = on_criar_cliente

        self.callbacks = {
            "on_selecionar": self._selecionar_cliente,
            "on_nova_venda": on_nova_venda,
            "on_abater_tudo": on_abater_tudo,
            "on_abater_parte": on_abater_parte,
        }

        self.painel_config = PainelConfig(
            self, lambda: self.cliente_selecionado, self._ao_criar_cliente,
            on_editar_cliente=on_editar_cliente, on_excluir_cliente=on_excluir_cliente,
            on_historico_cliente=on_historico_cliente,
        )
        self.painel_config.pack(fill="x")

        self.frame_grade = tk.Frame(self, bg=COR_FUNDO)
        self.frame_grade.pack(fill="both", expand=True, padx=16, pady=16)

        self.frame_paginacao = tk.Frame(self, bg=COR_FUNDO)
        self.frame_paginacao.pack(fill="x")
        self.btn_anterior = tk.Button(self.frame_paginacao, text="< Anterior",
                                        command=self._pagina_anterior)
        self.btn_anterior.pack(side="left", padx=16, pady=4)
        self.label_pagina = tk.Label(self.frame_paginacao, bg=COR_FUNDO, fg="white")
        self.label_pagina.pack(side="left", expand=True)
        self.btn_proxima = tk.Button(self.frame_paginacao, text="Próxima >",
                                       command=self._proxima_pagina)
        self.btn_proxima.pack(side="right", padx=16, pady=4)

        self.frame_selecionado = tk.Frame(self, bg="#1f1f1f", height=60)
        self.frame_selecionado.pack(fill="x", side="bottom")
        self._montar_painel_selecionado()

        self._renderizar_pagina()

    def _total_paginas(self):
        if not self.clientes:
            return 1
        resto = 1 if len(self.clientes) % CLIENTES_POR_PAGINA else 0
        return len(self.clientes) // CLIENTES_POR_PAGINA + resto

    def _renderizar_pagina(self):
        for widget in self.frame_grade.winfo_children():
            widget.destroy()

        inicio = self.pagina_atual * CLIENTES_POR_PAGINA
        fim = inicio + CLIENTES_POR_PAGINA
        pagina_de_clientes = self.clientes[inicio:fim]

        for indice, cliente in enumerate(pagina_de_clientes):
            linha = indice // COLUNAS
            coluna = indice % COLUNAS
            card = CardCliente(self.frame_grade, cliente, self.callbacks)
            card.grid(row=linha, column=coluna, padx=8, pady=8, sticky="nsew")

        for coluna in range(COLUNAS):
            self.frame_grade.grid_columnconfigure(coluna, weight=1)

        total_paginas = self._total_paginas()
        self.label_pagina.config(text=f"Página {self.pagina_atual + 1} de {total_paginas}")
        self.btn_anterior.config(state="normal" if self.pagina_atual > 0 else "disabled")
        self.btn_proxima.config(
            state="normal" if self.pagina_atual < total_paginas - 1 else "disabled"
        )

    def _proxima_pagina(self):
        if self.pagina_atual < self._total_paginas() - 1:
            self.pagina_atual += 1
            self._renderizar_pagina()

    def _pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self._renderizar_pagina()

    def _montar_painel_selecionado(self):
        for widget in self.frame_selecionado.winfo_children():
            widget.destroy()

        if self.cliente_selecionado is None:
            tk.Label(self.frame_selecionado, text="Nenhum cliente selecionado",
                      bg="#1f1f1f", fg="#999999").pack(side="left", padx=16, pady=16)
            return

        cliente = self.cliente_selecionado
        tk.Label(self.frame_selecionado, text=cliente["nome"], bg="#1f1f1f", fg="white",
                  font=("Segoe UI", 11, "bold")).pack(side="left", padx=(16, 8), pady=12)
        tk.Label(self.frame_selecionado, text=f"Saldo atual: R$ {cliente['saldo_devedor']:.2f}",
                  bg="#1f1f1f", fg=COR_DIVIDA).pack(side="left", padx=8)

        tk.Button(self.frame_selecionado, text="Abater Tudo", bg=COR_BOTAO_ABATER_TUDO,
                   fg="white", relief="flat",
                   command=lambda: self.callbacks["on_abater_tudo"](cliente)).pack(
            side="left", padx=6
        )
        tk.Button(self.frame_selecionado, text="Abater Parte", bg=COR_BOTAO_ABATER_PARTE,
                   fg="white", relief="flat",
                   command=lambda: self.callbacks["on_abater_parte"](cliente)).pack(
            side="left", padx=6
        )
        tk.Button(self.frame_selecionado, text="Registrar Nova Venda", bg=COR_BOTAO_VENDA,
                   fg="white", relief="flat",
                   command=lambda: self.callbacks["on_nova_venda"](cliente)).pack(
            side="right", padx=16
        )

    def _selecionar_cliente(self, cliente):
        self.cliente_selecionado = cliente
        self._montar_painel_selecionado()

    def _ao_criar_cliente(self, nome, apelido):
        """
        Chamado pela janela de "Novo Cliente". Delega a criação de verdade
        pra função que veio do main.py (que fala com o ClienteService),
        e se der certo, recarrega a grade com a lista atualizada do banco.
        """
        if self.on_criar_cliente is None:
            print(f"TODO: criar cliente {nome} ({apelido}) — nenhum callback configurado")
            return
        self.on_criar_cliente(nome, apelido)

    def atualizar_clientes(self, novos_clientes):
        """Chame isso depois de criar/editar/abater algo, pra recarregar a tela com dados frescos do banco."""
        self.clientes = novos_clientes
        self.pagina_atual = 0
        self._renderizar_pagina()


# ---------------------------------------------------------------------------
# Bloco de teste isolado: roda SÓ essa tela, com dados de mentira (mock),
# sem precisar do banco/service reais. Ótimo pra testar o visual sozinho.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    clientes_mock = [
        {"id": 1, "nome": "Carlos Silva", "saldo_devedor": 85.00, "ultima_data": "11/07", "ultima_hora": "15:34", "ultima_valor": 85.00},
        {"id": 2, "nome": "João Pedro", "saldo_devedor": 40.00, "ultima_data": "10/07", "ultima_hora": "17:20", "ultima_valor": 40.00},
        {"id": 3, "nome": "Maria Souza", "saldo_devedor": 310.00, "ultima_data": "11/07", "ultima_hora": "09:15", "ultima_valor": 310.00},
        {"id": 4, "nome": "Pedro Santos", "saldo_devedor": 15.00, "ultima_data": "09/07", "ultima_hora": "13:10", "ultima_valor": 15.00},
        {"id": 5, "nome": "Ana Clara", "saldo_devedor": 120.00, "ultima_data": "11/07", "ultima_hora": "18:45", "ultima_valor": 120.00},
        {"id": 6, "nome": "Uedi Oliveira", "saldo_devedor": 530.00, "ultima_data": "08/07", "ultima_hora": "10:05", "ultima_valor": 530.00},
        {"id": 7, "nome": "Lucas Lima", "saldo_devedor": 60.00, "ultima_data": "12/07", "ultima_hora": "17:20", "ultima_valor": 60.00},
        {"id": 8, "nome": "Fernanda", "saldo_devedor": 22.00, "ultima_data": "11/07", "ultima_hora": "07:00", "ultima_valor": 22.00},
        {"id": 9, "nome": "Rafael Costa", "saldo_devedor": 95.00, "ultima_data": "10/07", "ultima_hora": "14:22", "ultima_valor": 95.00},
        {"id": 10, "nome": "Beatriz", "saldo_devedor": 75.00, "ultima_data": "09/07", "ultima_hora": "19:05", "ultima_valor": 75.00},
    ]

    def mock_nova_venda(cliente):
        print(f"Abrir tela de nova venda para {cliente['nome']}")

    def mock_abater_tudo(cliente):
        print(f"Abater tudo do saldo de {cliente['nome']}")

    def mock_abater_parte(cliente):
        print(f"Abrir tela de abater parte para {cliente['nome']}")

    def mock_criar_cliente(nome, apelido):
        if not nome:
            raise ValueError("O nome é obrigatório.")
        print(f"Criar cliente de mentira: {nome} ({apelido})")

    janela = tk.Tk()
    janela.title("Fiado Fácil")
    janela.geometry("1000x600")
    janela.configure(bg=COR_FUNDO)

    tela = TelaClientes(
        janela, clientes_mock, mock_nova_venda, mock_abater_tudo, mock_abater_parte,
        on_criar_cliente=mock_criar_cliente,
    )
    tela.pack(fill="both", expand=True)

    janela.mainloop()