from email.policy import default
from pickle import FALSE
from re import A
from site import USER_BASE
from time import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, BooleanVar, END
import os
import configparser
import json


class JanelaPrincipal(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Aidly")
        self.iconbitmap("logo.ico")
        self.option_add("*tearOff", False)
        self.resizable(False, False)
        estilo = ttk.Style(self)
        # Importar o arquivo tcl
        self.tk.call("source", "proxttk-dark.tcl")
        # Definir o tema com o método theme_use
        estilo.theme_use("proxttk-dark")

        self.title_font = tkfont.Font(family='colortube', size=20)
        self.sub_font = tkfont.Font(family='colortube', size=12)
        self.button_font = tkfont.Font(family='colortube', weight="bold")

        # self.container é onde será desenhado os quadros
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.container.pack(side="top", fill="both", expand=True)
        self.current_frame = None

        self.mostrar_quadro("PaginaConfiguracoes")
        self.mostrar_quadro("PaginaInicial")

    def mostrar_quadro(self, nome_pagina):
        # criar a nova página e embalá-la no container
        if globals().get(nome_pagina) is not None:
            # destruir a página antiga, se houver
            if self.current_frame is not None:
                self.current_frame.destroy()

            cls = globals()[nome_pagina]
            self.current_frame = cls(self.container, self)
            self.current_frame.pack(fill="both", expand=True)
        else:
            raise ValueError("A página %s não foi encontrada" % nome_pagina)


class PaginaConfiguracoes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Criar o arquivo de configuração se ele não existir
        config = configparser.ConfigParser()
        if not os.path.exists("config.ini"):

            # Criar a seção de número máximo de linhas e colunas
            config.add_section('max_rows_columns')
            config.set('max_rows_columns', 'max_rows', '3')
            config.set('max_rows_columns', 'max_columns', '2')

            # Criar a seção de hosts conhecidos
            config.add_section('known_hosts')
            config.set('known_hosts', 'value', '')

            # Criar a seção de credenciais
            config.add_section('credentials')
            config.set('credentials', 'user', '')
            config.set('credentials', 'password', '')

            with open("config.ini", "w") as config_file:
                config.write(config_file)

        config_obj = configparser.ConfigParser()
        config_obj.read("config.ini")

        rows_cols = config_obj["max_rows_columns"]

        global MAX_LINHAS
        global MAX_COLUNAS
        MAX_LINHAS = int(rows_cols['max_rows'])
        MAX_COLUNAS = int(rows_cols['max_columns'])

        global USERNAME
        global PASSWORD

        USERNAME = config_obj["credentials"]["user"]
        PASSWORD = config_obj["credentials"]["password"]

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10
        paddingX = 75
        # Título ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Configurações",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20, columnspan=2,
                    padx=(paddingX, 0))

        # Quadro Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        quadro_widgets = ttk.Frame(self)
        quadro_widgets.grid(row=1, column=0, columnspan=2,
                            padx=(paddingX, 0))

        # Máximo de Linhas e Colunas -------------------------------------------------------------------------------------------------------------------
        subtitulo_max_linhas_cols = ttk.Label(
            quadro_widgets, text="Máximo de Linhas e Colunas", font=controller.sub_font, foreground='grey', justify="right")
        subtitulo_max_linhas_cols.grid(row=0, column=0, columnspan=2, pady=5)

        # Máximo de Linhas
        var_max_linhas = tk.IntVar()
        entrada_max_linhas = ttk.Spinbox(quadro_widgets, from_=2,
                                         to=10, textvariable=var_max_linhas)
        entrada_max_linhas.grid(row=1, column=0, pady=paddingY,
                                sticky="we", padx=(0, paddingY))

        entrada_max_linhas.delete(0, END)
        entrada_max_linhas.insert(0, MAX_LINHAS.__str__())

        label_max_linhas = ttk.Label(
            quadro_widgets, text="Máximo de Linhas", font="colortube 11")
        label_max_linhas.grid(row=entrada_max_linhas.grid_info()['row'], column=entrada_max_linhas.grid_info()[
            'column'], sticky="nw", padx=5)

        # Máximo de Colunas
        var_max_colunas = tk.IntVar()
        entrada_max_colunas = ttk.Spinbox(quadro_widgets, from_=1,
                                          to=10, textvariable=var_max_colunas)
        entrada_max_colunas.grid(row=1, column=1, pady=paddingY, sticky="we")

        label_max_colunas = ttk.Label(
            quadro_widgets, text="Máximo de Colunas", font="colortube 11")
        label_max_colunas.grid(row=entrada_max_colunas.grid_info()['row'], column=entrada_max_colunas.grid_info()[
                               'column'], sticky="nw", padx=5)

        entrada_max_colunas.delete(0, END)
        entrada_max_colunas.insert(0, MAX_COLUNAS.__str__())

        # Credenciais do Usuário -------------------------------------------------------------------------------------------------------------------------------------
        label_subtitulo = ttk.Label(quadro_widgets, text="Credenciais", font=controller.sub_font, foreground='grey',
                                    justify="center")
        label_subtitulo.grid(row=2, column=0, columnspan=2,
                             pady=(paddingY*2, paddingY/2))

        # Usuário
        var_usuario = tk.StringVar()
        entrada_usuario = ttk.Entry(quadro_widgets, textvariable=var_usuario)
        entrada_usuario.grid(column=0, row=3, pady=paddingY,
                             sticky="we", padx=(0, paddingY))
        label_usuario = ttk.Label(
            quadro_widgets, text="Usuário", font="colortube 11")
        label_usuario.grid(column=entrada_usuario.grid_info()[
                           "column"], row=entrada_usuario.grid_info()["row"], sticky="nw", padx=5)

        # Senha
        var_senha = tk.StringVar()
        entrada_senha = ttk.Entry(
            quadro_widgets, textvariable=var_senha)
        entrada_senha.grid(column=1, row=3, pady=paddingY,
                           sticky="we")
        label_senha = ttk.Label(
            quadro_widgets, text="Senha", font="colortube 11")
        label_senha.grid(column=entrada_senha.grid_info()[
            "column"], row=entrada_senha.grid_info()["row"], sticky="nw", padx=5)

        # Função delete_credentials
        def delete_credentials():
            """Limpa as credenciais armazenadas no arquivo de configuração"""

            config_obj["credentials"]["user"] = ""
            config_obj["credentials"]["password"] = ""
            with open("config.ini", "w") as config_file:
                config_obj.write(config_file)
            entrada_usuario.delete(0, END)
            entrada_senha.delete(0, END)

        # Switch para conectar automaticamente
        global var_conectar_auto
        var_conectar_auto = tk.BooleanVar()
        switch_conectar_auto = ttk.Checkbutton(
            quadro_widgets, text="Conectar Automaticamente", variable=var_conectar_auto, style='Switch')
        switch_conectar_auto.grid(column=0, row=4, pady=paddingY,
                                  sticky="we")

        # Botão para deletar as credenciais
        botao_deletar_credenciais = ttk.Button(
            quadro_widgets, text="Deletar Credenciais", command=delete_credentials)
        botao_deletar_credenciais.grid(column=1, row=4, pady=paddingY,
                                       sticky="news")

        # Função update_config
        def update_config():
            global MAX_LINHAS
            global MAX_COLUNAS
            MAX_LINHAS = int(var_max_linhas.get())
            MAX_COLUNAS = int(var_max_colunas.get())
            config_obj["max_rows_columns"]["max_rows"] = str(MAX_LINHAS)
            config_obj["max_rows_columns"]["max_columns"] = str(MAX_COLUNAS)

            entrada_max_colunas.delete(0, END)
            entrada_max_colunas.insert(0, MAX_COLUNAS.__str__())

            entrada_max_linhas.delete(0, END)
            entrada_max_linhas.insert(0, MAX_LINHAS.__str__())

            global USERNAME
            global PASSWORD

            if entrada_usuario.get() != "":
                USERNAME = entrada_usuario.get()
                config_obj["credentials"]["user"] = USERNAME
                entrada_usuario.delete(0, END)
                entrada_usuario.insert(0, USERNAME)
                time.sleep(3)
                entrada_usuario.delete(0, END)

            if entrada_senha.get() != "":
                PASSWORD = entrada_senha.get()
                config_obj["credentials"]["password"] = PASSWORD
                entrada_senha.delete(0, END)
                entrada_senha.insert(0, PASSWORD)
                time.sleep(3)
                entrada_senha.delete(0, END)

            with open("config.ini", "w") as config_file:
                config_obj.write(config_file)

        # Navegação -----------------------------------------------------------------------------------------------------------------------------------------
        botao_aplicar = ttk.Button(
            self, text="Aplicar", style="AccentButton", command=update_config)
        botao_aplicar.grid(row=11, column=1, padx=10, pady=(
            paddingY*4, paddingY/2), sticky='nswe')
        botao_voltar = ttk.Button(self, text="Voltar ao início",
                                  command=lambda: controller.mostrar_quadro("PaginaInicial"))
        botao_voltar.grid(row=11, column=0, padx=(
            paddingX, 10), pady=(paddingY*4, paddingY/2), sticky='nswe')


class PaginaInicial(ttk.Frame):

    def __init__(self, parent, controller):
        margem = 55
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitulo = ttk.Label(
            self, text="Aidly: Juntos pela\nsolidariedade", font=controller.title_font, justify="center")
        labelTitulo.grid(column=0, row=0, pady=(20, 0), padx=margem)
        labelSubtitulo = ttk.Label(self, text="Bem-vindo!\nEscolha uma opção abaixo", font=controller.sub_font, foreground='grey',
                                   justify="center")
        labelSubtitulo.grid(column=0, row=1,
                            pady=(10, 20), padx=margem + 20)

        botao1 = ttk.Button(self, text="Sou uma ONG", style="AccentButton",
                            command=lambda: controller.mostrar_quadro("DadosOng"))
        botao1.grid(sticky='we', column=0, row=3, pady=10, padx=20)

        botao2 = ttk.Button(self, text="Sou uma Empresa", style="AccentButton",
                            command=lambda: controller.mostrar_quadro("PaginaEmpresa"))
        botao2.grid(sticky='we', column=0, row=4, pady=10, padx=20)

        botao3 = ttk.Button(self, text="Configurações", style="AccentButton",
                            command=lambda: controller.mostrar_quadro("PaginaConfiguracoes"))
        botao3.grid(sticky='we', column=0, row=5, pady=10, padx=20)


class DadosOng(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        global REQUERIMENTO
        REQUERIMENTO = {
            "id": "",
            "dados_ong": {
                "nome_ong": "",
                "nome_responsavel": "",
                "nome_projeto": "",
                "cnpj": "",
                "telefone": "",
                "endereco": {
                    "rua": "",
                    "numero": "",
                    "bairro": "",
                    "cidade": "",
                    "estado": "",
                    "cep": ""
                }
            },
            "lista_itens": [
                {
                    "nome_item": "",
                    "quantidade": "",
                    "categoria": ""
                }
            ]
        }

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Título ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Digite os dados da ONG",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20,
                    columnspan=MAX_COLUNAS+1, padx=100, sticky="we")

        # Frame Coluna 1   -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='news',
                           padx=paddingY)

        # Nome da ONG
        nome_ong = ttk.Entry(widgets_frame)
        nome_ong.grid(column=2, row=1,
                      pady=paddingY, sticky="we")
        nome_ong_label = ttk.Label(
            widgets_frame, text="Nome da ONG", font="colortube 11")
        nome_ong_label.grid(column=2, row=1,
                            sticky="nw",
                            padx=5)

        # Nome do Responsável
        nome_responsavel = ttk.Entry(widgets_frame)
        nome_responsavel.grid(column=2, row=2,
                              pady=paddingY, sticky="we")
        nome_responsavel_label = ttk.Label(
            widgets_frame, text="Nome do Responsável", font="colortube 11")
        nome_responsavel_label.grid(column=2, row=2,
                                    sticky="nw",
                                    padx=5)

        # Nome do Projeto
        nome_projeto = ttk.Entry(widgets_frame)
        nome_projeto.grid(column=2, row=3,
                          pady=paddingY, sticky="we")
        nome_projeto_label = ttk.Label(
            widgets_frame, text="Nome do Projeto", font="colortube 11")
        nome_projeto_label.grid(column=2, row=3,
                                sticky="nw",
                                padx=5)

        # CNPJ
        cnpj_var = tk.StringVar()
        cnpj = ttk.Entry(widgets_frame, textvariable=cnpj_var)
        cnpj.grid(column=2, row=4,
                  pady=paddingY, sticky="we")
        cnpj_label = ttk.Label(
            widgets_frame, text="CNPJ", font="colortube 11")
        cnpj_label.grid(column=2, row=4,
                        sticky="nw",
                        padx=5)

        def format_cnpj(*args):  # Formata o CNPJ para o padrão 00.000.000/0000-00
            s = ''.join(filter(str.isdigit, cnpj_var.get()))

            # adiciona os pontos e traços
            if len(s) == 0:
                s = ''
            elif len(s) < 3:
                s = s[:2] + '.' + s[2:]
            elif len(s) < 6:
                s = s[:2] + '.' + s[2:5] + '.' + s[5:]
            elif len(s) < 9:
                s = s[:2] + '.' + s[2:5] + '.' + s[5:8] + '/' + s[8:]
            elif len(s) < 13:
                s = s[:2] + '.' + s[2:5] + '.' + s[5:8] + '/' + \
                    s[8:12] + '-' + s[12:]
            else:
                s = s[:2] + '.' + s[2:5] + '.' + s[5:8] + '/' + \
                    s[8:12] + '-' + s[12:14]

            cnpj_var.set(s)

            # atualizar texto dentro do Entry
            cnpj.icursor(len(s))

        # Listener para formatar CNPJ
        cnpj_var.trace('w', format_cnpj)

        # Telefone
        telefone_var = tk.StringVar()
        telefone = ttk.Entry(
            widgets_frame, textvariable=telefone_var)
        telefone.grid(column=2, row=5,
                      pady=paddingY, sticky="we")
        telefone_label = ttk.Label(
            widgets_frame, text="Telefone", font="colortube 11")
        telefone_label.grid(column=2, row=5,
                            sticky="nw",
                            padx=5)

        def format_phone(*args):  # Formata o telefone para (xx) xxxx-xxxx
            s = ''.join(filter(str.isdigit, telefone_var.get()))

            if len(s) == 0:
                s = ''
            elif len(s) < 3:
                s = '(' + s + ')'
            elif len(s) < 7:
                s = '(' + s[:2] + ') ' + s[2:]
            elif len(s) < 11:
                s = '(' + s[:2] + ') ' + s[2:6] + '-' + s[6:]
            else:
                s = '(' + s[:2] + ') ' + s[2:7] + '-' + s[7:11]
            telefone_var.set(s)

            # atualizar texto dentro do Entry
            telefone.icursor(len(s))

        # Listener para formatar telefone
        telefone_var.trace('w', format_phone)

        # Frame Coluna 2 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky='news',
                            padx=(paddingY, 0))  # Cria widgets_frame2 na janela

        # Rua
        rua = ttk.Entry(widgets_frame2)
        rua.grid(column=2, row=1, columnspan=2,
                 pady=paddingY, sticky="we")
        rua_label = ttk.Label(
            widgets_frame2, text="Rua", font="colortube 11")
        rua_label.grid(column=2, row=1,
                       sticky="nw",
                       padx=5)

        # Número
        numero = ttk.Entry(widgets_frame2)
        numero.grid(column=2, row=2, columnspan=2,
                    pady=paddingY, sticky="we")
        numero_label = ttk.Label(
            widgets_frame2, text="Número", font="colortube 11")
        numero_label.grid(column=2, row=2,
                          sticky="nw",
                          padx=5)

        # Bairro
        bairro = ttk.Entry(widgets_frame2)
        bairro.grid(column=2, row=3, columnspan=2,
                    pady=paddingY, sticky="we")
        bairro_label = ttk.Label(
            widgets_frame2, text="Bairro", font="colortube 11")
        bairro_label.grid(column=2, row=3,
                          sticky="nw",
                          padx=5)

        # Cidade
        cidade = ttk.Entry(widgets_frame2)
        cidade.grid(column=2, row=4, columnspan=2,
                    pady=paddingY, sticky="we")
        cidade_label = ttk.Label(
            widgets_frame2, text="Cidade", font="colortube 11")
        cidade_label.grid(column=2, row=4,
                          sticky="nw",
                          padx=5)

        # Estado
        estado = ttk.Entry(widgets_frame2)
        estado.grid(column=2, row=5,
                    pady=paddingY, padx=(0, paddingY))
        estado_label = ttk.Label(
            widgets_frame2, text="Estado", font="colortube 11")
        estado_label.grid(column=2, row=5,
                          sticky="nw",
                          padx=5)

        # CEP
        cep_var = tk.StringVar()
        cep = ttk.Entry(widgets_frame2, textvariable=cep_var)
        cep.grid(column=3, row=5,
                 pady=paddingY)
        cep_label = ttk.Label(
            widgets_frame2, text="CEP", font="colortube 11")
        cep_label.grid(column=3, row=5,
                       sticky="nw",
                       padx=5)

        def format_cep(*args):  # Formata o CEP para xxxxx-xxx
            s = ''.join(filter(str.isdigit, cep_var.get()))

            if len(s) == 0:
                s = ''
            elif len(s) < 6:
                s = s
            else:
                s = s[:5] + '-' + s[5:8]
            cep_var.set(s)

            # atualizar texto dentro do Entry
            cep.icursor(len(s))

        # Listener para formatar CEP
        cep_var.trace('w', format_cep)

        def save():  # Salva os dados no arquivo de configuração
            global REQUERIMENTO
            REQUERIMENTO = {
                "dados_ong": {
                    "nome_ong": nome_ong.get(),
                    "nome_responsavel": nome_responsavel.get(),
                    "nome_projeto": nome_projeto.get(),
                    "cnpj": cnpj_var.get(),
                    "telefone": telefone_var.get(),
                    "endereco": {
                        "rua": rua.get(),
                        "numero": numero.get(),
                        "bairro": bairro.get(),
                        "cidade": cidade.get(),
                        "estado": estado.get(),
                        "cep": cep_var.get()
                    }
                }
            }

            print(REQUERIMENTO)

            controller.mostrar_quadro("PaginaItens")

        # Botões ---------------------------------------------------------------------------------------------------------------------------------------------
        accentbutton = ttk.Button(
            self, text="Próximo passo", style="AccentButton", command=save)
        accentbutton.grid(row=11, column=1, padx=(
            paddingY, 0), pady=20, sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.mostrar_quadro("PaginaInicial"))
        button.grid(row=11, column=0, padx=paddingY, pady=20, sticky='nswe')


class PaginaItens(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        global MAX_LINHAS
        global MAX_COLUNAS
        global REQUERIMENTO
        print(REQUERIMENTO)

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Título ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Adicione os itens requeridos",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20,
                    columnspan=MAX_COLUNAS+2, padx=100, sticky="we")

        # Frame Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='news',
                           padx=paddingY)

        # Itens
        global itens
        global start_col
        global criarItem
        global removerItem
        global frames
        itens = []
        start_col = -2
        # Frame
        frames = []

        def criarFrame():
            global frames
            defaultFrame = ttk.Frame(widgets_frame)
            frames.append(defaultFrame)

        def resetarWidgets(start_row, start_col, frame):
            global criarItem
            global removerItem

            criarItem = ttk.Button(
                frame, text="+ Item", command=criarItens)
            removerItem = ttk.Button(
                frame, text="- Item", command=removerItens)

            if len(itens) > 1:
                removerItem.grid(
                    column=1+start_col, row=start_row+9, sticky="nwe", pady=paddingY*2.5, padx=(2.5, 0))
                criarItem.grid(
                    column=start_col, row=start_row+9, sticky="new", pady=paddingY*2.5, padx=(0, 2.5))
            else:
                removerItem.grid_forget()
                criarItem.grid(
                    column=start_col, row=start_row+9, columnspan=2, sticky="new", pady=paddingY*2.5)

            if start_col == 2:
                criarItem.grid_configure(
                    padx=(paddingY*2, 2.5), pady=paddingY)
                removerItem.grid_configure(pady=paddingY)
                if MAX_COLUNAS*MAX_LINHAS == len(itens):
                    print("Não é possível adicionar mais itens")
                    criarItem.grid_forget()
                    removerItem.grid_forget()
                    removerItem = ttk.Button(
                        widgets_frame2, text="- Itens", command=removerItens)
                    removerItem.grid(
                        row=8, column=2, columnspan=2, sticky="ew", pady=paddingY)

        def criarItens():
            global start_col
            global MAX_LINHAS
            global itens
            if MAX_COLUNAS*MAX_LINHAS == len(itens):
                return

            criarItem.grid_forget()
            removerItem.grid_forget()

            start_row = (len(itens) % MAX_LINHAS) * 8

            if len(itens) % MAX_LINHAS == 0:
                start_col += 2
                criarFrame()

            frame = frames[-1]

            if len(itens) % MAX_LINHAS == 0:
                frame.grid(row=start_row, column=start_col,
                           sticky="new", padx=(paddingY, paddingY))

            # Nome do item widget
            nome_item = ttk.Entry(frame)
            label_nome_produto = ttk.Label(frame, text="Nome do item",
                                           font="colortube 11")
            # Categoria widget
            categoria = ttk.Entry(frame)
            label_categoria = ttk.Label(frame, text="Categoria",
                                        font="colortube 11")

            # Quantidade widget
            var_quantidade = tk.IntVar()
            quantidade = ttk.Spinbox(
                frame, from_=1, to=99, width=5, textvariable=var_quantidade)
            quantidade_label = ttk.Label(
                frame, text='Quantidade', font="colortube 11")

            # Separator
            separator = ttk.Separator(frame, orient="horizontal")

            itens.append({
                "frame": frame,
                "nome_item": nome_item,
                "label_nome_item": label_nome_produto,
                "categoria": categoria,
                "label_categoria": label_categoria,
                "quantidade": quantidade,
                "quantidade_label": quantidade_label,
                "var_quantidade": var_quantidade,
                "separator": separator
            })
            # Changes labels based on owner count
            if len(itens) > 1:
                itens[0]["label_nome_item"].configure(text="Nome item 1")
                itens[0]["label_categoria"].configure(text="Categoria 1")
                itens[0]["quantidade_label"].configure(
                    text="Quantidade 1")
                label_nome_produto.config(text="Nome item "+str(len(itens)))
                label_categoria.config(text="Categoria "+str(len(itens)))
                quantidade_label.config(
                    text='Quantidade '+str(len(itens)))
                itens[0]["separator"].grid()

            # Separator
            separator.grid(row=start_row, column=0, columnspan=2,
                           sticky='we')

            # Nome item Origem
            nome_item.grid(column=0, row=start_row+1, columnspan=2,
                           pady=(paddingY*2.5, paddingY), sticky="we")
            label_nome_produto.grid(column=0, row=start_row+1, columnspan=2, sticky="nw",
                                    padx=5, pady=5)
            if len(itens) % MAX_LINHAS == 1:
                nome_item.grid_configure(pady=paddingY)
                label_nome_produto.grid_configure(pady=0, padx=5)

            # Owner Destino
            categoria.grid(
                column=0, row=start_row+3, pady=paddingY, columnspan=2, sticky="we")
            label_categoria.grid(column=0, row=start_row+3,
                                 sticky="nw", columnspan=2, padx=5)

            # Quantidade
            quantidade.grid(column=0, row=start_row+4,
                            pady=(paddingY, paddingY*2), columnspan=2, sticky="we")
            quantidade_label.grid(column=0, row=start_row+4,
                                  sticky="nw", columnspan=2, padx=5)

            # Remover separador no ultimo item
            if len(itens) % MAX_LINHAS == 1:
                separator.grid_forget()

            bstart_col = 0
            bstart_row = start_row
            if len(itens) % MAX_LINHAS == 0:
                bstart_col = 2
                bstart_row = -8

            # print("Start row: " + str(bstart_row), " | Start col: " + str(start_col), " | Start frame: " + str(frame.grid_info()["column"])+","+ str(frame.grid_info()["row"]))
            resetarWidgets(bstart_row, bstart_col, frame)

        def removerItens():
            criarItem.grid_forget()
            removerItem.grid_forget()
            # offset row by lenght of items
            owner = itens.pop()
            owner["nome_item"].grid_forget()
            owner["label_nome_item"].grid_forget()
            owner["categoria"].grid_forget()
            owner["label_categoria"].grid_forget()
            owner["quantidade"].grid_forget()
            owner["quantidade_label"].grid_forget()
            owner["separator"].grid_forget()

            start_row = ((len(itens)) % MAX_LINHAS) * 8
            bstart_col = 0

            if len(itens) < 2:
                itens[0]["label_nome_item"].configure(text="Nome item")
                itens[0]["label_categoria"].configure(text="Categoria")
                itens[0]["quantidade_label"].configure(
                    text="Quantidade")

            bstart_row = start_row
            if len(itens) % MAX_LINHAS == 0:
                frames.pop().grid_forget()
                bstart_col = 2
                bstart_row = -8

            frame = frames[-1]

            resetarWidgets(bstart_row, bstart_col, frame)

        criarItem = ttk.Button(
            widgets_frame, text="+ Item", command=criarItens)
        criarItem.grid(
            column=0, row=7, columnspan=2, sticky="we", pady=paddingY)
        removerItem = ttk.Button(
            widgets_frame, text="- Item", command=removerItens)
        criarItens()

        # Frame Coluna 2    -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1)  # Cria widgets_frame2 na janela

        def salvar():
            global REQUERIMENTO
            print("Salvando...")
            # converter itens para json
            itens_json = []
            for item in itens:
                itens_json.append({
                    "nome_item": item["nome_item"].get(),
                    "categoria": item["categoria"].get(),
                    "quantidade": item["quantidade"].get()
                })

            # Salvar dados em requerimentos.json
            import os
            import json

            REQUERIMENTO = {
                "dados_ong": REQUERIMENTO.get("dados_ong")
            }

            if os.path.exists("requerimentos.json"):
                with open("requerimentos.json", "r") as r:
                    requerimentos = json.load(r)
            else:
                requerimentos = []

            REQUERIMENTO.update({
                "id": len(requerimentos) + 1,
                "itens": itens_json,
            })

            requerimentos.append(REQUERIMENTO)

            with open("requerimentos.json", "w") as w:
                json.dump(requerimentos, w, indent=2)
                print("Salvo!")

            # controller.mostrar_quadro("DadosOng")

        accentbutton = ttk.Button(
            self, text="Criar", style="AccentButton", command=salvar)
        accentbutton.grid(row=11, column=1, padx=10, pady=20, sticky='nswe')
        button = ttk.Button(self, text="Voltar",
                            command=lambda: controller.mostrar_quadro("DadosOng"))
        button.grid(row=11, column=0, padx=10, pady=20, sticky='nswe')


class PaginaEmpresa(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Import de Tabela",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20,
                    columnspan=4, padx=paddingY)

        # Frame lista de requerimentos ----------------------------------------------------------------------------------------------------------------------
        requerimentos_frame = tk.Frame(self)
        requerimentos_frame.grid(
            row=1, column=0, columnspan=4, sticky="nswe", padx=paddingY, pady=paddingY)

        # Lista de requerimentos
        requerimentos = []
        if os.path.exists("requerimentos.json"):
            with open("requerimentos.json", "r") as r:
                requerimentos = json.load(r)

        # Scrollbar
        scrollbar = ttk.Scrollbar(requerimentos_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista
        lista = tk.Listbox(requerimentos_frame, yscrollcommand=scrollbar.set, )
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Adicionar requerimentos à lista
        for requerimento in requerimentos:
            lista.insert(tk.END, requerimento["dados_ong"]["nome_ong"]+" - " +str(requerimento["id"]))

        # Configurar scrollbar
        scrollbar.config(command=lista.yview)

        label = ttk.Label(self, text="", font=controller.title_font)
        label.grid(row=2, column=0, pady=20, padx=paddingY)

        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                label.configure(text=data)
            else:
                label.configure(text="")

        lista.bind("<<ListboxSelect>>", callback)

        accentbutton = ttk.Button(
            self, text="Gerar", style="AccentButton")
        accentbutton.grid(row=11, column=1, pady=20,
                          padx=paddingY, sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.mostrar_quadro("PaginaInicial"))
        button.grid(row=11, column=0, padx=paddingY, pady=20, sticky='nswe')


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()
