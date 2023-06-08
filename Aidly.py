import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import os
import json
from PIL import ImageTk, Image


class JanelaPrincipal(tk.Tk):
    # Esta é uma definição de classe para uma janela que herda da classe tk.Tk
    def __init__(self, *args, **kwargs):
        # Este é o método construtor para a classe JanelaPrincipal

        tk.Tk.__init__(self, *args, **kwargs)
        # Esta linha inicializa a classe pai (tk.Tk)

        self.title("Aidly")
        self.iconbitmap("assets/logo.ico")
        self.option_add("*tearOff", False)
        self.resizable(False, False)
        estilo = ttk.Style(self)
        # Importar o arquivo tcl
        self.tk.call("source", "style.tcl")
        # Definir o tema com o método theme_use
        estilo.theme_use("style")
        # Estas linhas definem o título, ícone e estilo da janela

        self.title_font = tkfont.Font(family='colortube', size=20)
        self.sub_font = tkfont.Font(family='colortube', size=12)
        self.button_font = tkfont.Font(family='colortube', weight="bold")
        # Estas linhas definem algumas fontes a serem usadas posteriormente

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Estas linhas criam um container frame que irá conter outros widgets

        self.container.pack(side="top", fill="both", expand=True)
        self.current_frame = None
        # Estas linhas empacotam o container frame e inicializam uma variável para armazenar o frame atual

        self.mostrar_quadro("PaginaInicial")
        # Esta linha chama o método mostrar_quadro para mostrar o frame inicial

    def mostrar_quadro(self, nome_pagina):
        # Este método cria um novo frame e o empacota no container

        if globals().get(nome_pagina) is not None:
            # Verifica se a página solicitada existe

            if self.current_frame is not None:
                self.current_frame.destroy()
            # Destroi o frame atual se ele existir

            cls = globals()[nome_pagina]
            self.current_frame = cls(self.container, self)
            self.current_frame.pack(fill="both", expand=True)
            # Cria e empacota o novo frame

        else:
            raise ValueError("A página %s não foi encontrada" % nome_pagina)
            # Gera um erro se a página solicitada não existir

    def toast(self, msg, tipo="info"):
        # Este método cria uma mensagem de toast na parte inferior da janela

        switcher = {
            "info": "#333",
            "error": "#f44336",
            "success": "#4caf50",
            "warning": "#ff9800"
        }

        if tipo not in switcher:
            tipo = "info"
        # Estas linhas definem as cores para diferentes tipos de mensagens de toast

        toast = tk.Label(self.container, text=msg, font=self.sub_font,
                         background=switcher[tipo], foreground="white", padx=20, pady=10)
        toast.pack(side="bottom", fill="x", pady=10)
        self.after(2000, toast.destroy)
        # Estas linhas criam e empacotam a mensagem de toast e, em seguida, a destroem após 2 segundos


class PaginaInicial(ttk.Frame):
    # Esta classe representa a página inicial da aplicação
    # Ela herda de ttk.Frame, que é um widget que fornece um container para conter outros widgets

    def __init__(self, parent, controller):
        # Este é o construtor da classe
        # Ele recebe dois parâmetros: parent e controller
        # parent é o widget pai deste frame
        # controller é o controlador principal da aplicação

        margem = 55
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Abrir a imagem do logo e redimensioná-la
        logo = Image.open(
            "assets/logo.png").resize((300, 100), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        # Criar um rótulo com a imagem do logo e adicioná-lo ao frame
        labelLogo = ttk.Label(self, image=logo)
        labelLogo.image = logo  # type: ignore
        labelLogo.grid(column=0, row=0, pady=(20, 0), padx=margem)

        # Criar um rótulo com o subtítulo e adicioná-lo ao frame
        labelSubtitulo = ttk.Label(self, text="Bem-vindo!\nEscolha uma opção abaixo",
                                   font=controller.sub_font, foreground='grey', justify="center")
        labelSubtitulo.grid(column=0, row=1, pady=(10, 20), padx=margem + 20)

        # Criar um botão para cadastrar uma ONG e adicioná-lo ao frame
        botao1 = ttk.Button(self, text="Cadastrar uma ONG", style="AccentButton",
                            command=lambda: controller.mostrar_quadro("CriarOng"))
        botao1.grid(sticky='we', column=0, row=3, pady=10, padx=20)

        # Criar um botão para criar um requerimento e adicioná-lo ao frame
        botao2 = ttk.Button(self, text="Criar um requerimento", style="AccentButton",
                            command=lambda: controller.mostrar_quadro("CriarRequerimento"))
        botao2.grid(sticky='we', column=0, row=4, pady=(10, 20), padx=20)


class CriarOng(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        paddingY = 10

        # Cria um rótulo com o texto "Digite os dados da ONG" e o adiciona ao frame
        titulo = ttk.Label(self, text="Digite os dados da ONG",
                           font=controller.title_font, foreground="Black")
        titulo.grid(row=0, column=0, pady=20, columnspan=3,
                    padx=100, sticky="we")

        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='news',
                           padx=paddingY)

        # Cria uma caixa de entrada (entry) para o nome da ONG e a adiciona ao frame
        nome_ong = ttk.Entry(widgets_frame, foreground="black")
        nome_ong.grid(column=2, row=1,
                      pady=paddingY, sticky="we")
        # Cria um rótulo para a caixa de entrada do nome da ONG
        nome_ong_label = ttk.Label(
            widgets_frame, text="Nome da ONG", font="colortube 11", foreground="grey")
        nome_ong_label.grid(column=2, row=1,
                            sticky="nw",
                            padx=5)

        # Cria uma caixa de entrada (entry) para o nome do responsável e a adiciona ao frame
        nome_responsavel = ttk.Entry(widgets_frame, foreground="black")
        nome_responsavel.grid(column=2, row=2,
                              pady=paddingY, sticky="we")
        # Cria um rótulo para a caixa de entrada do nome do responsável
        nome_responsavel_label = ttk.Label(
            widgets_frame, text="Nome do Responsável", font="colortube 11", foreground="grey")
        nome_responsavel_label.grid(column=2, row=2,
                                    sticky="nw",
                                    padx=5)

        # Cria uma caixa de entrada (entry) para o nome do projeto e a adiciona ao frame
        nome_projeto = ttk.Entry(widgets_frame, foreground="black")
        nome_projeto.grid(column=2, row=3,
                          pady=paddingY, sticky="we")
        # Cria um rótulo para a caixa de entrada do nome do projeto
        nome_projeto_label = ttk.Label(
            widgets_frame, text="Nome do Projeto", font="colortube 11", foreground="grey")
        nome_projeto_label.grid(column=2, row=3,
                                sticky="nw",
                                padx=5)

        cnpj_var = tk.StringVar()
        # Cria uma caixa de entrada (entry) para o CNPJ e a associa à variável cnpj_var
        cnpj = ttk.Entry(widgets_frame, foreground="black",
                         textvariable=cnpj_var)
        cnpj.grid(column=2, row=4,
                  pady=paddingY, sticky="we")
        # Cria um rótulo para a caixa de entrada do CNPJ
        cnpj_label = ttk.Label(
            widgets_frame, text="CNPJ", font="colortube 11", foreground="grey")
        cnpj_label.grid(column=2, row=4,
                        sticky="nw",
                        padx=5)

        # Função para formatar o CNPJ conforme é digitado
        def format_cnpj(*args):
            s = ''.join(filter(str.isdigit, cnpj_var.get()))

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

            # Define o valor formatado do CNPJ na variável cnpj_var
            cnpj_var.set(s)

            # Move o cursor para o final da string formatada
            cnpj.icursor(len(s))

        # Adiciona um rastreador (trace) na variável cnpj_var, para chamar a função format_cnpj sempre que o valor da variável for modificado
        cnpj_var.trace('w', format_cnpj)

        # Cria uma variável para armazenar o número de telefone
        telefone_var = tk.StringVar()

        # Cria um campo de entrada para o telefone, associado à variável telefone_var
        telefone = ttk.Entry(widgets_frame, foreground="black",
                             textvariable=telefone_var)
        telefone.grid(column=2, row=5, pady=paddingY, sticky="we")

        # Cria um rótulo para o campo de telefone
        telefone_label = ttk.Label(
            widgets_frame, text="Telefone", font="colortube 11", foreground="grey")
        telefone_label.grid(column=2, row=5, sticky="nw", padx=5)

        # Função para formatar o número de telefone

        def format_phone(*args):
            # Remove caracteres não numéricos do valor da variável telefone_var
            s = ''.join(filter(str.isdigit, telefone_var.get()))

            # Formata o número de acordo com o tamanho
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

            # Define o valor formatado na variável telefone_var
            telefone_var.set(s)

            # Posiciona o cursor no final do valor formatado
            telefone.icursor(len(s))

        # Adiciona um rastreador (trace) à variável telefone_var para chamar a função format_phone quando o valor da variável é modificado
        telefone_var.trace('w', format_phone)

        # Cria um novo frame para os widgets
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky='news', padx=(paddingY, 0))

        # Cria um campo de entrada para a rua
        rua = ttk.Entry(widgets_frame2, foreground="black")
        rua.grid(column=2, row=1, columnspan=2, pady=paddingY, sticky="we")

        # Cria um rótulo para o campo de rua
        rua_label = ttk.Label(widgets_frame2, text="Rua",
                              font="colortube 11", foreground="grey")
        rua_label.grid(column=2, row=1, sticky="nw", padx=5)

        # Cria um campo de entrada para o número
        numero = ttk.Entry(widgets_frame2, foreground="black")
        numero.grid(column=2, row=2, columnspan=2, pady=paddingY, sticky="we")

        # Cria um rótulo para o campo de número
        numero_label = ttk.Label(
            widgets_frame2, text="Número", font="colortube 11", foreground="grey")
        numero_label.grid(column=2, row=2, sticky="nw", padx=5)

        # Cria um campo de entrada para o bairro
        bairro = ttk.Entry(widgets_frame2, foreground="black")
        bairro.grid(column=2, row=3, columnspan=2, pady=paddingY, sticky="we")

        # Cria um rótulo para o campo de bairro
        bairro_label = ttk.Label(
            widgets_frame2, text="Bairro", font="colortube 11", foreground="grey")
        bairro_label.grid(column=2, row=3, sticky="nw", padx=5)

        # Cria um campo de entrada para a cidade
        cidade = ttk.Entry(widgets_frame2, foreground="black")
        cidade.grid(column=2, row=4, columnspan=2, pady=paddingY, sticky="we")

        # Cria um rótulo para o campo de cidade
        cidade_label = ttk.Label(
            widgets_frame2, text="Cidade", font="colortube 11", foreground="grey")
        cidade_label.grid(column=2, row=4, sticky="nw", padx=5)

        # Cria um campo de entrada para o estado
        estado = ttk.Entry(widgets_frame2, foreground="black")
        estado.grid(column=2, row=5, pady=paddingY, padx=(0, paddingY))

        # Cria um rótulo para o campo de estado
        estado_label = ttk.Label(
            widgets_frame2, text="Estado", font="colortube 11", foreground="grey")
        estado_label.grid(column=2, row=5, sticky="nw", padx=5)

        # Cria uma variável para armazenar o CEP
        cep_var = tk.StringVar()

        # Cria um campo de entrada para o CEP, associado à variável cep_var
        cep = ttk.Entry(widgets_frame2, foreground="black",
                        textvariable=cep_var)
        cep.grid(column=3, row=5, pady=paddingY)

        # Cria um rótulo para o campo de CEP
        cep_label = ttk.Label(widgets_frame2, text="CEP",
                              font="colortube 11", foreground="grey")
        cep_label.grid(column=3, row=5, sticky="nw", padx=5)

        # Função para formatar o CEP
        def format_cep(*args):
            # Remove caracteres não numéricos do valor da variável cep_var
            s = ''.join(filter(str.isdigit, cep_var.get()))

            # Formata o CEP de acordo com o tamanho
            if len(s) == 0:
                s = ''
            elif len(s) < 6:
                s = s
            else:
                s = s[:5] + '-' + s[5:8]

            # Define o valor formatado na variável cep_var
            cep_var.set(s)

            # Posiciona o cursor no final do valor formatado
            cep.icursor(len(s))

        # Adiciona um rastreador (trace) à variável cep_var para chamar a função format_cep quando o valor da variável é modificado
        cep_var.trace('w', format_cep)

        # Função para salvar os dados
        def save():
            # Verifica se todos os campos estão preenchidos
            if nome_ong.get() == "" or nome_responsavel.get() == "" or nome_projeto.get() == "" or cnpj_var.get() == "" or telefone_var.get() == "" or rua.get() == "" or numero.get() == "" or bairro.get() == "" or cidade.get() == "" or estado.get() == "" or cep_var.get() == "":
                controller.toast("Preencha todos os campos!", "error")
                return

            # Cria um dicionário com os dados da ONG
            dados_ong = {
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

            print("Salvando...")

            # Verifica se o arquivo "ongs.json" existe e carrega os dados existentes
            if os.path.exists("ongs.json"):
                with open("ongs.json", "r") as r:
                    ongs = json.load(r)
            else:
                ongs = []

            # Atribui um ID único para a nova ONG
            dados_ong["id"] = len(ongs) + 1

            # Adiciona os dados da ONG à lista de ongs
            ongs.append(dados_ong)

            # Salva os dados no arquivo "ongs.json"
            with open("ongs.json", "w") as w:
                json.dump(ongs, w, indent=2)
                controller.toast("Dados salvos com sucesso!", "success")

            # Mostra o quadro "PaginaInicial" no controller
            controller.mostrar_quadro("PaginaInicial")

        accentbutton = ttk.Button(
            self, text="Criar", style="AccentButton", command=save)
        # Cria um botão chamado "accentbutton" com o texto "Criar".
        # O botão usa o estilo "AccentButton".
        # Quando o botão é clicado, ele executa a função "save".
        accentbutton.grid(row=11, column=1, padx=(
            paddingY, 0), pady=20, sticky='nswe')
        # Posiciona o botão na linha 11 e coluna 1 da interface.
        # Define o preenchimento horizontal do botão usando o valor de "paddingY" como espaço à esquerda.
        # Define o preenchimento vertical do botão como 20 pixels.
        # O botão se expande tanto na direção norte-sul (ns) quanto na direção oeste-leste (we).

        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.mostrar_quadro("PaginaInicial"))
        # Cria um botão chamado "button" com o texto "Voltar ao início".
        # Quando o botão é clicado, ele chama a função "mostrar_quadro" do objeto "controller" com o argumento "PaginaInicial".
        button.grid(row=11, column=0, padx=paddingY,
                    pady=20, sticky='nswe')
        # Posiciona o botão na linha 11 e coluna 0 da interface.
        # Define o preenchimento horizontal do botão usando o valor de "paddingY".
        # Define o preenchimento vertical do botão como 20 pixels.
        # O botão se expande tanto na direção norte-sul (ns) quanto na direção oeste-leste (we).


class CriarRequerimento(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        global MAX_LINHAS
        global MAX_COLUNAS
        MAX_LINHAS = 2  # Número máximo de linhas para exibir os itens
        MAX_COLUNAS = 3  # Número máximo de colunas para exibir os itens

        paddingY = 10  # Espaçamento vertical entre os widgets

        titulo = ttk.Label(self, text="Criar Requerimento",
                           font=controller.title_font, foreground="black")
        titulo.grid(row=0, column=0, pady=20,
                    columnspan=MAX_COLUNAS+2, padx=100, sticky="we")

        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='news',
                           padx=paddingY)

        global itens
        global start_col
        global criarItem
        global removerItem
        global frames
        itens = []  # Lista para armazenar os itens
        start_col = -2  # Coluna inicial para posicionar os botões "criarItem" e "removerItem"
        frames = []  # Lista para armazenar os frames

        def criarFrame():
            """Cria um novo frame de widget"""
            global frames
            defaultFrame = ttk.Frame(widgets_frame)
            frames.append(defaultFrame)

        def resetarWidgets(start_row, start_col, frame):
            """Reseta e configura os botões 'criarItem' e 'removerItem'"""
            global criarItem
            global removerItem

            # Criação dos botões "criarItem" e "removerItem" usando ttk.Button
            criarItem = ttk.Button(
                frame, text="+ Item", command=criarItens)
            removerItem = ttk.Button(
                frame, text="- Item", command=removerItens)

            # Configuração da posição dos botões "criarItem" e "removerItem" com base no número de itens
            if len(itens) > 1:
                removerItem.grid(
                    column=1+start_col, row=start_row+9, sticky="nwe", pady=paddingY*2.5, padx=(2.5, 0))
                criarItem.grid(
                    column=start_col, row=start_row+9, sticky="new", pady=paddingY*2.5, padx=(0, 2.5))
            else:
                removerItem.grid_forget()
                criarItem.grid(
                    column=start_col, row=start_row+9, columnspan=2, sticky="new", pady=paddingY*2.5)

            # Configuração dos botões quando a coluna inicial é 2
            if start_col == 2:
                criarItem.grid_configure(
                    padx=(paddingY*2, 2.5), pady=paddingY)
                removerItem.grid_configure(pady=paddingY)
                # Verifica se o número máximo de itens é alcançado e, nesse caso, remove os botões "criarItem" e "removerItem" e cria um novo botão "removerItem" com texto diferente
                if MAX_COLUNAS*MAX_LINHAS == len(itens):
                    print("Não é possível adicionar mais itens")
                    criarItem.grid_forget()
                    removerItem.grid_forget()
                    removerItem = ttk.Button(
                        widgets_frame2, text="- Itens", command=removerItens)
                    removerItem.grid(
                        row=8, column=0, columnspan=2, sticky="news", pady=paddingY, padx=(0, paddingY*2))

        def criarItens():
            global start_col  # Variável global para controlar a coluna de início
            global MAX_LINHAS  # Número máximo de linhas por coluna
            global itens  # Lista de itens

            # Verifica se o número máximo de itens foi atingido
            if MAX_COLUNAS*MAX_LINHAS == len(itens):
                return

            # Remove os botões de criar e remover item
            criarItem.grid_forget()
            removerItem.grid_forget()

            # Define a linha de início com base no número atual de itens
            start_row = (len(itens) % MAX_LINHAS) * 8

            # Incrementa a coluna de início e cria um novo frame se a coluna atual estiver cheia
            if len(itens) % MAX_LINHAS == 0:
                start_col += 2
                criarFrame()

            # Obtém o último frame criado
            frame = frames[-1]

            # Posiciona o frame na grade se for o primeiro item da coluna
            if len(itens) % MAX_LINHAS == 0:
                frame.grid(row=start_row, column=start_col,
                           sticky="new", padx=(paddingY, paddingY))

            # Cria os widgets para o novo item
            nome_item = ttk.Entry(frame, foreground="black")
            label_nome_produto = ttk.Label(frame, text="Nome do item",
                                           font="colortube 11", foreground="black")
            categoria = ttk.Entry(frame, foreground="black")
            label_categoria = ttk.Label(frame, text="Categoria",
                                        font="colortube 11", foreground="black")

            var_quantidade = tk.IntVar()
            quantidade = ttk.Spinbox(
                frame, from_=1, to=99, width=5, textvariable=var_quantidade, foreground="black")
            quantidade_label = ttk.Label(
                frame, text='Quantidade', font="colortube 11", foreground="black")

            separator = ttk.Separator(frame, orient="horizontal")

            # Adiciona o novo item à lista de itens
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

            # Altera os rótulos com base na contagem de itens
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

            # Cria um separador horizontal entre os itens
            separator.grid(row=start_row, column=0, columnspan=2,
                           sticky='we')

            # Posiciona o campo de entrada para o nome do item
            nome_item.grid(column=0, row=start_row+1, columnspan=2,
                           pady=(paddingY*2.5, paddingY), sticky="we")
            label_nome_produto.grid(column=0, row=start_row+1, columnspan=2, sticky="nw",
                                    padx=5, pady=5)

            # Ajusta o espaçamento se for o primeiro item da coluna
            if len(itens) % MAX_LINHAS == 1:
                nome_item.grid_configure(pady=paddingY)
                label_nome_produto.grid_configure(pady=0, padx=5)

            # Posiciona o campo de entrada para a categoria
            categoria.grid(
                column=0, row=start_row+3, pady=paddingY, columnspan=2, sticky="we")
            label_categoria.grid(column=0, row=start_row+3,
                                 sticky="nw", columnspan=2, padx=5)

            # Posiciona o Spinbox para a quantidade
            quantidade.grid(column=0, row=start_row+4,
                            pady=(paddingY, paddingY*2), columnspan=2, sticky="we")
            quantidade_label.grid(column=0, row=start_row+4,
                                  sticky="nw", columnspan=2, padx=5)

            # Remove o separador no último item da coluna
            if len(itens) % MAX_LINHAS == 1:
                separator.grid_forget()

            bstart_col = 0
            bstart_row = start_row
            if len(itens) % MAX_LINHAS == 0:
                bstart_col = 2
                bstart_row = -8

            # Chama a função para redefinir os widgets na posição correta
            resetarWidgets(bstart_row, bstart_col, frame)

        def removerItens():
            # Remove os itens anteriores do layout
            criarItem.grid_forget()
            removerItem.grid_forget()

            # Remove o último item da lista 'itens'
            owner = itens.pop()

            # Remove os widgets do item removido do layout
            owner["nome_item"].grid_forget()
            owner["label_nome_item"].grid_forget()
            owner["categoria"].grid_forget()
            owner["label_categoria"].grid_forget()
            owner["quantidade"].grid_forget()
            owner["quantidade_label"].grid_forget()
            owner["separator"].grid_forget()

            # Calcula a posição inicial para adicionar o próximo item
            start_row = ((len(itens)) % MAX_LINHAS) * 8
            bstart_col = 0

            # Verifica se há apenas um item na lista
            if len(itens) < 2:
                # Atualiza os textos dos rótulos do primeiro item
                itens[0]["label_nome_item"].configure(text="Nome item")
                itens[0]["label_categoria"].configure(text="Categoria")
                itens[0]["quantidade_label"].configure(text="Quantidade")

            bstart_row = start_row
            # Verifica se a quantidade de itens é um múltiplo do número máximo de linhas
            if len(itens) % MAX_LINHAS == 0:
                # Remove o último frame da lista 'frames' do layout
                frames.pop().grid_forget()
                bstart_col = 2
                bstart_row = -8

            # Obtém o último frame da lista 'frames'
            frame = frames[-1]

            # Redefine os widgets no layout a partir da posição inicial
            resetarWidgets(bstart_row, bstart_col, frame)

        # Criação do botão "Criar Item" e definição da função "criarItens" como comando ao ser clicado
        criarItem = ttk.Button(
            widgets_frame, text="+ Item", command=criarItens)
        criarItem.grid(
            column=0, row=7, columnspan=2, sticky="we", pady=paddingY)

        # Criação do botão "Remover Item" e definição da função "removerItens" como comando ao ser clicado
        removerItem = ttk.Button(
            widgets_frame, text="- Item", command=removerItens)

        # Chamada da função "criarItens"
        criarItens()

        # Criação de um novo frame denominado "widgets_frame2"
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky="news")

        # Criação do rótulo "Selecione uma ONG" dentro do frame "widgets_frame2"
        ongs_label = ttk.Label(
            widgets_frame2, text='Selecione uma ONG', font="colortube 11", foreground="black")
        ongs_label.grid(column=0, row=0, sticky="we", pady=paddingY)

        # Criação de um novo frame denominado "ongs_frame" dentro do frame "widgets_frame2"
        ongs_frame = tk.Frame(widgets_frame2)
        ongs_frame.grid(row=1, column=0, sticky="we",
                        pady=paddingY, padx=(0, paddingY))

        # Criação de uma barra de rolagem vertical
        scrollbar = ttk.Scrollbar(ongs_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Criação de uma lista (Listbox) com a opção de rolagem vertical usando a barra de rolagem
        lista = tk.Listbox(ongs_frame, yscrollcommand=scrollbar.set,
                           foreground="black", selectmode=tk.SINGLE, relief=tk.FLAT, borderwidth=1, highlightthickness=2, highlightbackground="#cccccc")
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        print("Carregando ONGs...")

        # Verifica se o arquivo "ongs.json" existe
        if os.path.exists("ongs.json"):
            # Abre o arquivo JSON e carrega os dados
            with open('ongs.json', 'r') as json_file:
                ongs_raw = json.load(json_file)
                # Insere cada ONG na lista, exibindo o nome e o ID
                for ong in ongs_raw:
                    lista.insert(
                        tk.END, ong["nome_ong"] + "-" + str(ong["id"]))
        else:
            print("Arquivo ongs.json não encontrado")

        # Configura a barra de rolagem para controlar a visualização da lista
        scrollbar.config(command=lista.yview)

        # Variável global para armazenar o índice da ONG selecionada na lista
        global selecionada
        selecionada = -1

        # Função de callback para lidar com a seleção de um item na lista
        def callback(event):
            global selecionada
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                selecionada = int(data.split("-")[1])
            else:
                selecionada = -1

        # Vincula a função de callback ao evento de seleção na lista
        lista.bind("<<ListboxSelect>>", callback)

        def salvar():
            # Função responsável por salvar os dados em um arquivo JSON

            print("Salvando...")

            # Cria uma lista vazia para armazenar os itens no formato JSON
            itens_json = []

            # Itera sobre cada item na lista "itens"
            for item in itens:
                # Obtém os valores dos campos "nome_item", "categoria" e "quantidade" do item atual
                # e adiciona esses valores a um dicionário no formato JSON
                itens_json.append({
                    "nome_item": item["nome_item"].get(),
                    "categoria": item["categoria"].get(),
                    "quantidade": int(item["quantidade"].get())
                })

            # Verifica se não foi selecionada uma ONG
            if selecionada < 0:
                controller.toast("Selecione uma ONG", "error")
                return

            # Verifica se não há nenhum item ou se o nome do primeiro item está vazio
            if len(itens) == 0 or itens_json[0]["nome_item"] == "":
                controller.toast("Preencha os campos", "error")
                return

            # Cria um dicionário "data" contendo o ID da ONG selecionada e a lista de itens no formato JSON
            data = {
                "id_ong": selecionada,
                "itens": itens_json
            }

            # Verifica se o arquivo "requisicoes.json" já existe
            if os.path.exists("requisicoes.json"):
                # Se o arquivo existir, abre-o em modo de leitura
                with open('requisicoes.json', 'r') as json_file:
                    # Carrega o conteúdo do arquivo JSON em uma lista chamada "requisicoes"
                    requisicoes = json.load(json_file)
                    # Adiciona o novo dado à lista "requisicoes"
                    requisicoes.append(data)
                    # Abre o arquivo em modo de escrita e sobrescreve o conteúdo com a lista atualizada "requisicoes"
                    with open('requisicoes.json', 'w') as outfile:
                        json.dump(requisicoes, outfile)
            else:
                # Se o arquivo não existir, cria um novo arquivo "requisicoes.json" e escreve nele a lista "data" em formato JSON
                with open('requisicoes.json', 'w') as outfile:
                    json.dump([data], outfile)

            # Exibe uma mensagem de sucesso
            controller.toast("Requisição salva com sucesso", "success")
            controller.mostrar_quadro("PaginaInicial")

        # Cria um frame chamado "quadro"
        quadro = tk.Frame(self)
        quadro.grid(row=11, column=0, sticky="ew", columnspan=10)

        # Cria um botão chamado "accentbutton" com o texto "Criar", estilo "AccentButton" e a função "salvar" como comando
        accentbutton = ttk.Button(
            quadro, text="Criar", style="AccentButton", command=salvar)
        accentbutton.grid(row=0, column=1, padx=10, pady=20, sticky='nswe')

        # Cria um botão chamado "button" com o texto "Voltar" e a função lambda que chama "mostrar_quadro" passando "PaginaInicial" como argumento
        button = ttk.Button(
            quadro, text="Voltar", command=lambda: controller.mostrar_quadro("PaginaInicial"))
        button.grid(row=0, column=0, padx=10, pady=20, sticky='nswe')


if __name__ == "__main__":
    # Cria uma instância da classe JanelaPrincipal e a atribui à variável 'app'
    app = JanelaPrincipal()

    # Inicia o loop principal da interface gráfica, permitindo que a janela seja exibida
    app.mainloop()

