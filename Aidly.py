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


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Scripter")
        self.iconbitmap("logo.ico")
        self.option_add("*tearOff", False)
        self.resizable(False, False)
        style = ttk.Style(self)
        # Import the tcl file
        self.tk.call("source", "proxttk-dark.tcl")
        # Set the theme with the theme_use method
        style.theme_use("proxttk-dark")

        self.title_font = tkfont.Font(family='colortube', size=20)
        self.sub_font = tkfont.Font(family='colortube', size=12)
        self.button_font = tkfont.Font(family='colortube', weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Configuration, StartPage, ItensPage, CompanyPage, DadosOng):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Configuration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create the configuration file if it doesn't exist
        config = configparser.ConfigParser()
        if not os.path.exists("config.ini"):

            # Create Max columns and rows section
            config.add_section('max_rows_columns')
            config.set('max_rows_columns', 'max_rows', '3')
            config.set('max_rows_columns', 'max_columns', '2')

            # Create known hosts section
            config.add_section('known_hosts')
            config.set('known_hosts', 'value', '')

            # Create credetials section
            config.add_section('credentials')
            config.set('credentials', 'user', '')
            config.set('credentials', 'password', '')

            with open("config.ini", "w") as config_file:
                config.write(config_file)

        config_obj = configparser.ConfigParser()
        config_obj.read("config.ini")

        rows_cols = config_obj["max_rows_columns"]

        global MAX_ROWS
        global MAX_COLS
        MAX_ROWS = int(rows_cols['max_rows'])
        MAX_COLS = int(rows_cols['max_columns'])

        global USERNAME
        global PASSWORD

        USERNAME = config_obj["credentials"]["user"]
        PASSWORD = config_obj["credentials"]["password"]

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10
        paddingX = 75
        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Configurações",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20, columnspan=2,
                    padx=(paddingX, 0))

        # Frame Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, columnspan=2,
                           padx=(paddingX, 0))

        # Max Columns and Rows -------------------------------------------------------------------------------------------------------------------
        subtitle_max_rows_cols = ttk.Label(
            widgets_frame, text="Max Rows and Columns", font=controller.sub_font, foreground='grey', justify="right")
        subtitle_max_rows_cols.grid(row=0, column=0, columnspan=2, pady=5)

        # Max Rows
        max_rows_var = tk.IntVar()
        max_rows_entry = ttk.Spinbox(widgets_frame, from_=2,
                                     to=10, textvariable=max_rows_var)
        max_rows_entry.grid(row=1, column=0, pady=paddingY,
                            sticky="we", padx=(0, paddingY))

        max_rows_entry.delete(0, END)
        max_rows_entry.insert(0, MAX_ROWS.__str__())

        max_rows_label = ttk.Label(
            widgets_frame, text="Max Rows", font="colortube 11")
        max_rows_label.grid(row=max_rows_entry.grid_info()['row'], column=max_rows_entry.grid_info()[
                            'column'], sticky="nw", padx=5)

        # Max Columns
        max_cols_var = tk.IntVar()
        max_cols_entry = ttk.Spinbox(widgets_frame, from_=1,
                                     to=10, textvariable=max_cols_var)
        max_cols_entry.grid(row=1, column=1, pady=paddingY, sticky="we")

        max_cols_label = ttk.Label(
            widgets_frame, text="Max Columns", font="colortube 11")
        max_cols_label.grid(row=max_cols_entry.grid_info()['row'], column=max_cols_entry.grid_info()[
                            'column'], sticky="nw", padx=5)

        max_cols_entry.delete(0, END)
        max_cols_entry.insert(0, MAX_COLS.__str__())

        # User Credentials -------------------------------------------------------------------------------------------------------------------------------------
        labelSubtitle = ttk.Label(widgets_frame, text="Credencias", font=controller.sub_font, foreground='grey',
                                  justify="center")
        labelSubtitle.grid(row=2, column=0, columnspan=2,
                           pady=(paddingY*2, paddingY/2))

        # Usuário
        varUser = tk.StringVar()
        user_entry = ttk.Entry(widgets_frame, textvariable=varUser)
        user_entry.grid(column=0, row=3, pady=paddingY,
                        sticky="we", padx=(0, paddingY))
        userBoxLabel = ttk.Label(
            widgets_frame, text="Usuário", font="colortube 11")
        userBoxLabel.grid(column=user_entry.grid_info()[
                          "column"], row=user_entry.grid_info()["row"], sticky="nw", padx=5)

        # Senha
        varPass = tk.StringVar()
        password_entry = ttk.Entry(
            widgets_frame, textvariable=varPass)
        password_entry.grid(column=1, row=3, pady=paddingY,
                            sticky="we")
        passBoxLabel = ttk.Label(
            widgets_frame, text="Senha", font="colortube 11")
        passBoxLabel.grid(column=password_entry.grid_info()[
                          "column"], row=password_entry.grid_info()["row"], sticky="nw", padx=5)

        # delete_credentials function
        def delete_credentials():
            """Clear the credentials stored in the config file"""

            config_obj["credentials"]["user"] = ""
            config_obj["credentials"]["password"] = ""
            with open("config.ini", "w") as config_file:
                config_obj.write(config_file)
            user_entry.delete(0, END)
            password_entry.delete(0, END)

        # Switch para conectar automaticamente
        global auto_connect_var
        auto_connect_var = tk.BooleanVar()
        auto_connect_switch = ttk.Checkbutton(
            widgets_frame, text="Auto-connect", variable=auto_connect_var, style='Switch')
        auto_connect_switch.grid(column=0, row=4, pady=paddingY,
                                 sticky="we")

        # Botão de apagar credenciais
        delete_credentials_button = ttk.Button(
            widgets_frame, text="Deletar Credenciais", command=delete_credentials)
        delete_credentials_button.grid(column=1, row=4, pady=paddingY,
                                       sticky="news")

        # update_config function

        def update_config():
            global MAX_ROWS
            global MAX_COLS
            MAX_ROWS = int(max_rows_var.get())
            MAX_COLS = int(max_cols_var.get())
            config_obj["max_rows_columns"]["max_rows"] = str(MAX_ROWS)
            config_obj["max_rows_columns"]["max_columns"] = str(MAX_COLS)

            max_cols_entry.delete(0, END)
            max_cols_entry.insert(0, MAX_COLS.__str__())

            max_rows_entry.delete(0, END)
            max_rows_entry.insert(0, MAX_ROWS.__str__())

            global USERNAME
            global PASSWORD

            if user_entry.get() != "":
                USERNAME = user_entry.get()
                config_obj["credentials"]["user"] = USERNAME
                user_entry.delete(0, END)
                user_entry.insert(0, USERNAME)
                time.sleep(3)
                user_entry.delete(0, END)

            if password_entry.get() != "":
                PASSWORD = password_entry.get()
                config_obj["credentials"]["password"] = PASSWORD
                password_entry.delete(0, END)
                password_entry.insert(0, PASSWORD)
                time.sleep(3)
                password_entry.delete(0, END)

            with open("config.ini", "w") as config_file:
                config_obj.write(config_file)

        # Navigation -----------------------------------------------------------------------------------------------------------------------------------------
        accentbutton = ttk.Button(
            self, text="Aplicar", style="AccentButton", command=update_config)
        accentbutton.grid(row=11, column=1, padx=10, pady=(
            paddingY*4, paddingY/2), sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=11, column=0, padx=(
            paddingX, 10), pady=(paddingY*4, paddingY/2), sticky='nswe')


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        pad = 79
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = ttk.Label(
            self, text="Aidly: Juntos pela\nsolidariedade", font=controller.title_font, justify="center")
        labelTitle.grid(column=0, row=0, pady=(20, 0), padx=pad)
        labelSubtitle = ttk.Label(self, text="Bem vindo!\n Escolha uma opção abaixo", font=controller.sub_font, foreground='grey',
                                  justify="center")
        labelSubtitle.grid(column=0, row=1,
                           pady=(10, 20), padx=pad + 20)

        button1 = ttk.Button(self, text="Sou uma ONG", style="AccentButton",
                             command=lambda: controller.show_frame("DadosOng"))
        button1.grid(sticky='we', column=0, row=3, pady=10, padx=20)

        button2 = ttk.Button(self, text="Sou uma Empresa", style="AccentButton",
                             command=lambda: controller.show_frame("CompanyPage"))
        button2.grid(sticky='we', column=0, row=4, pady=10, padx=20)


class ItensPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Criação de Requerimentos",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20, columnspan=4)

        # Frame Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='new',
                           padx=(paddingY, paddingY))

        # Owners
        global items
        global MAX_ROWS
        global MAX_COLS
        global start_col
        global createItem
        global removeItem
        global frames
        STARTING = 1
        items = []
        start_col = -2
        # Frame
        frames = []

        def createFrame():
            global frames
            defaultFrame = ttk.Frame(widgets_frame)
            frames.append(defaultFrame)

        def resetWidgets(start_row, start_col, frame):
            global createItem
            global removeItem

            createItem = ttk.Button(
                frame, text="+ Item", command=createItems)
            removeItem = ttk.Button(
                frame, text="- Item", command=removeItems)

            if len(items) > 1:
                removeItem.grid(
                    column=1+start_col, row=start_row+9, sticky="nwe", pady=paddingY*2.5, padx=(2.5, 0))
                createItem.grid(
                    column=start_col, row=start_row+9, sticky="new", pady=paddingY*2.5, padx=(0, 2.5))
            else:
                removeItem.grid_forget()
                createItem.grid(
                    column=start_col, row=start_row+9, columnspan=2, sticky="new", pady=paddingY*2.5)

            if start_col == 2:
                createItem.grid_configure(
                    padx=(paddingY*2, 2.5), pady=paddingY)
                removeItem.grid_configure(pady=paddingY)
                if MAX_COLS*MAX_ROWS == len(items):
                    print("Não é possível adicionar mais itens")
                    createItem.grid_forget()
                    removeItem.grid_forget()
                    removeItem = ttk.Button(
                        widgets_frame2, text="- Items", command=removeItems)
                    removeItem.grid(
                        row=8, column=2, columnspan=2, sticky="ew", pady=paddingY)


        def createItems():
            global start_col
            global MAX_ROWS
            global items
            if MAX_COLS*MAX_ROWS == len(items):
                return

            createItem.grid_forget()
            removeItem.grid_forget()

            start_row = (len(items) % MAX_ROWS) * 8

            if len(items) % MAX_ROWS == 0:
                start_col += 2
                createFrame()

            frame = frames[len(frames) - 1]

            if len(items) % MAX_ROWS == 0:
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

            items.append({
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
            if len(items) > 1:
                items[0]["label_nome_item"].configure(text="Nome item 1")
                items[0]["label_categoria"].configure(text="Categoria 1")
                items[0]["quantidade_label"].configure(
                    text="Quantidade 1")
                label_nome_produto.config(text="Nome item "+str(len(items)))
                label_categoria.config(text="Categoria "+str(len(items)))
                quantidade_label.config(
                    text='Quantidade '+str(len(items)))
                items[0]["separator"].grid()

            # Separator
            separator.grid(row=start_row, column=0, columnspan=2,
                           sticky='we')

            # Nome item Origem
            nome_item.grid(column=0, row=start_row+1, columnspan=2,
                           pady=(paddingY*2.5, paddingY), sticky="we")
            label_nome_produto.grid(column=0, row=start_row+1, columnspan=2, sticky="nw",
                                    padx=5, pady=paddingY*((nome_item.grid_info()["pady"][0]/paddingY)-1))
            if len(items) % MAX_ROWS == 1:
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
                                  sticky="nw", columnspan=2, padx=(5, 55))

            # Remover separador no ultimo item
            if len(items) % MAX_ROWS == 1:
                separator.grid_forget()

            bstart_col = 0
            bstart_row = start_row
            if len(items) % MAX_ROWS == 0:
                bstart_col = 2
                bstart_row = -8

            # print("Start row: " + str(bstart_row), " | Start col: " + str(start_col), " | Start frame: " + str(frame.grid_info()["column"])+","+ str(frame.grid_info()["row"]))
            resetWidgets(bstart_row, bstart_col, frame)

        def removeItems():
            createItem.grid_forget()
            removeItem.grid_forget()
            # offset row by lenght of items
            owner = items.pop()
            owner["nome_item"].grid_forget()
            owner["label_nome_item"].grid_forget()
            owner["categoria"].grid_forget()
            owner["label_categoria"].grid_forget()
            owner["quantidade"].grid_forget()
            owner["quantidade_label"].grid_forget()
            owner["separator"].grid_forget()

            start_row = ((len(items)) % MAX_ROWS) * 8
            bstart_col = 0

            if len(items) < 2:
                items[0]["label_nome_item"].configure(text="Nome item")
                items[0]["label_categoria"].configure(text="Categoria")
                items[0]["quantidade_label"].configure(
                    text="Quantidade")

            bstart_row = start_row
            if len(items) % MAX_ROWS == 0:
                frames.pop().grid_forget()
                bstart_col = 2
                bstart_row = -8

            frame = frames[len(frames) - 1]

            resetWidgets(bstart_row, bstart_col, frame)

        createItem = ttk.Button(
            widgets_frame, text="+ Item", command=createItems)
        createItem.grid(
            column=0, row=7, columnspan=2, sticky="we", pady=paddingY)
        removeItem = ttk.Button(
            widgets_frame, text="- Item", command=removeItems)

        # Frame Coluna 2    -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky='nw',
                            padx=(paddingY, paddingY + 15))  # Cria widgets_frame2 na janela
        createItems()

        # Nome da ONG
        nome_ong = ttk.Entry(widgets_frame2)
        nome_ong.grid(column=2, row=1, columnspan=2,
                      pady=paddingY, sticky="we")
        nome_ong_label = ttk.Label(
            widgets_frame2, text="Nome da ONG", font="colortube 11")
        nome_ong_label.grid(column=2, row=1,
                            sticky="nw",
                            padx=5)

        # CNPJ
        cnpj_var = tk.StringVar()
        cnpj = ttk.Entry(widgets_frame2, textvariable=cnpj_var)
        cnpj.grid(column=2, row=2, pady=paddingY,
                  columnspan=2, sticky="we")
        cnpj_label = ttk.Label(
            widgets_frame2, text="CNPJ", font="colortube 11")
        cnpj_label.grid(column=2, row=2,
                        sticky="nw",
                        padx=5)
        
        def format_cnpj():  # Formata o CNPJ para o padrão 00.000.000/0000-00
            s = cnpj_var.get()
            # remove todos os caracteres e letras que não são números
            s = s.replace('.', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('-', '')
            s = s.replace(' ', '')
            s = s.replace('/', '')
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
            widgets_frame2, textvariable=telefone_var)
        telefone.grid(column=2, row=3, sticky="we", pady=paddingY)
        telefone_label = ttk.Label(
            widgets_frame2, text="Telefone", font="colortube 11")
        telefone_label.grid(column=2, row=3,
                            sticky="nw",
                            padx=5)

       

        def format_phone():  # Formata o telefone para (xx) xxxx-xxxx
            s = telefone_var.get()
            # remove todos os caracteres e letras que não são números
            s = s.replace('.', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('-', '')
            s = s.replace(' ', '')
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



        def script():  # Gera o script de Import
            ticket = nome_ong.get()
            base_origem = cnpj.get()
            base_destino = telefone.get()
            caminho = caminhoBox.get()

            if varVerCheck.get():
                version = " version=12.1"
            else:
                version = ""

            if varMetaCheck.get():
                metadata = " CONTENT=METADATA_ONLY"
            else:
                metadata = ""

            schemas = []
            schemas_remap = []
            tablespaces = []
            drops = []
            datafiles_comand = []
            unlock = []
            remap = ""
            for ownerData in items:
                owner = ownerData["owner_origem"].get().upper()
                destino = ownerData["owner_destino"].get().upper()
                senha = ownerData["senha"].get()
                dataFiles = int(ownerData["data_file_spin"].get())

                schemas.append(f"{owner},")
                schemas_remap.append(f"{owner}:{destino},")
                tablespaces.append(
                    f"{owner}_DAT:{destino}_DAT,{owner}_IDX:{destino}_IDX,")

                if ownerData["var_remap_check"].get():
                    owner = destino

                if not ownerData["var_senha_check"].get():
                    senha = owner

                if ownerData["var_drop_check"].get():
                    drops.append(
                        f"DROP USER {owner} CASCADE;\nDROP TABLESPACE {owner}_DAT INCLUDING CONTENTS AND DATAFILES;\nDROP TABLESPACE {owner}_IDX INCLUDING CONTENTS AND DATAFILES;\n\n")

                datafiles_comand.append(
                    f"create tablespace {owner}_DAT datafile '{caminho}/{owner}_DAT.dbf' size 100m autoextend on next 100m;\n")
                for datafile in range(dataFiles-1):
                    if dataFiles > 1:
                        datafiles_comand.append(
                            f"alter tablespace {owner}_DAT add datafile '{caminho}/{owner}_DAT{datafile+2}.dbf' size 100m autoextend on next 100m;\n")

                datafiles_comand.append(
                    f"create tablespace {owner}_IDX datafile '{caminho}/{owner}_IDX.dbf' size 100m autoextend on next 100m;\n")
                datafiles_comand.append(
                    f"create user {owner} identified by {owner} default tablespace {owner}_DAT temporary tablespace TEMP quota unlimited on {owner}_DAT quota unlimited on {owner}_IDX quota 0k on SYSTEM;\n\n")

                unlock.append(f"""alter user {owner} identified by {senha} account unlock;\n

BEGIN
DBMS_NETWORK_ACL_ADMIN.append_host_ace (
    host       => '*',
    ace        => xs$ace_type(privilege_list => xs$name_list('connect','resolve'),
                            principal_name => '{owner}',
                            principal_type => XS_ACL.PTYPE_DB));
END;
/\n\n""")
            if ownerData["var_remap_check"].get():
                a = "".join(schemas_remap)[:-1].upper()
                b = "".join(tablespaces)[:-1].upper()
                remap = remap + f" REMAP_SCHEMA={a} REMAP_TABLESPACE={b}"

            script = f"""--ORIGEM: {base_origem.upper()}
export ORACLE_SID={base_origem.lower()}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
expdp BKP_EXPORT/AxxxM0 directory=DBA schemas={"".join(schemas)[:-1].upper()} dumpfile={ticket}.dmp logfile=exp_{ticket}.log exclude=statistics{version}{metadata}

--DESTINO: {base_destino.upper()}

{"".join(drops)}{"".join(datafiles_comand)}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
impdp BKP_IMPORT/AxxxM0 directory=DBA dumpfile={ticket}.dmp logfile=imp_{ticket}.log{remap}

{"".join(unlock)}
"""

            # Cria ou sobreescreve o aquivo import.txt
            f = open("import.txt", "w+")
            f.write(script)  # Escreve o script gerado
            f.close()  # Fecha o arquivo import.txt
            os.startfile("import.txt")  # Abre o arquivo import.txt

        accentbutton = ttk.Button(
            self, text="Proximo Paço", style="AccentButton", command=lambda: controller.show_frame("DadosOng"))
        accentbutton.grid(row=11, column=1, padx=10, pady=20, sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=11, column=0, padx=10, pady=20, sticky='nswe')


class DadosOng(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Cadastro de ONG",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20, columnspan=4)

        # Frame Coluna 1   -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = tk.Frame(self)
        widgets_frame.grid(row=1, column=1, sticky='nw',
                            padx=(paddingY, paddingY + 15))  # Cria widgets_frame2 na janela

        # Nome da ONG
        nome_ong = ttk.Entry(widgets_frame)
        nome_ong.grid(column=2, row=1, columnspan=2,
                      pady=paddingY, sticky="we")
        nome_ong_label = ttk.Label(
            widgets_frame, text="Nome da ONG", font="colortube 11")
        nome_ong_label.grid(column=2, row=1,
                            sticky="nw",
                            padx=5)

        # CNPJ
        cnpj_var = tk.StringVar()
        cnpj = ttk.Entry(widgets_frame, textvariable=cnpj_var)
        cnpj.grid(column=2, row=2, pady=paddingY,
                  columnspan=2, sticky="we")
        cnpj_label = ttk.Label(
            widgets_frame, text="CNPJ", font="colortube 11")
        cnpj_label.grid(column=2, row=2,
                        sticky="nw",
                        padx=5)
        
        def format_cnpj():  # Formata o CNPJ para o padrão 00.000.000/0000-00
            s = cnpj_var.get()
            # remove todos os caracteres e letras que não são números
            s = s.replace('.', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('-', '')
            s = s.replace(' ', '')
            s = s.replace('/', '')
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
        telefone.grid(column=2, row=3, sticky="we", pady=paddingY)
        telefone_label = ttk.Label(
            widgets_frame, text="Telefone", font="colortube 11")
        telefone_label.grid(column=2, row=3,
                            sticky="nw",
                            padx=5)

       

        def format_phone():  # Formata o telefone para (xx) xxxx-xxxx
            s = telefone_var.get()
            # remove todos os caracteres e letras que não são números
            s = s.replace('.', '')
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace('-', '')
            s = s.replace(' ', '')
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
      




class CompanyPage(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Import de Tabela",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20,
                    columnspan=4, padx=(paddingY + 50, 0))

        # Frame Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='new',
                           padx=(paddingY + 40, paddingY + 10))

        # Owner
        ownerBox = ttk.Entry(widgets_frame)
        ownerBox.grid(column=0, row=1, columnspan=2,
                      pady=paddingY, sticky="we")
        ownerBoxLabel = ttk.Label(widgets_frame, text="Owner", font="colortube 11").grid(column=0, row=1, columnspan=2, sticky="nw",
                                                                                         padx=5)

        # Owner Destino
        def toggleRemap():
            if varRemapCheck.get():
                owner_destinoBox.grid(
                    column=0, row=2, columnspan=2, pady=paddingY, sticky="we")
                owner_destinoBoxLabel.grid(
                    column=0, row=2, columnspan=2, sticky="nw", padx=5)
            else:
                owner_destinoBox.grid_forget()
                owner_destinoBoxLabel.grid_forget()

        owner_destinoBox = ttk.Entry(widgets_frame)
        owner_destinoBoxLabel = ttk.Label(
            widgets_frame, text="Owner Destino", font="colortube 11")

        # Tabela
        tabelaBox = ttk.Entry(widgets_frame)
        tabelaBox.grid(column=0, row=3, columnspan=2,
                       pady=paddingY, sticky="we")
        ttk.Label(widgets_frame, text="Tabela", font="colortube 11").grid(column=0, row=3, columnspan=2, sticky="nw",
                                                                          padx=5)
        # Tabelas
        tabRow = tabelaBox.grid_info()["row"]+1
        tabelas = []
        labels = []

        def resetWidgets():
            rowLen = len(tabelas)+tabRow
            if len(tabelas) > 0:
                removeTabelasButton.grid_forget()
                removeTabelasButton.grid(column=1, row=len(
                    tabelas)+tabRow+1, sticky="w", pady=paddingY, padx=(2.5, 0))
                createTabelasButton.grid(column=0, row=len(
                    tabelas)+tabRow+1, sticky="e", pady=paddingY, padx=(0, 2.5))
            else:
                createTabelasButton.grid(column=0, row=len(
                    tabelas)+tabRow+1, columnspan=2, sticky="we", pady=paddingY)
            RemapCheck.grid_forget()
            RemapCheck.grid(row=len(tabelas)+tabRow+2, column=0,
                            columnspan=2, sticky='w', pady=(0, 5))
            VerCheck.grid_forget()
            VerCheck.grid(row=len(tabelas)+tabRow+3, column=0,
                          columnspan=2, sticky='w', pady=(0, 5))
            ArchiveCheck.grid_forget()
            ArchiveCheck.grid(row=len(tabelas)+tabRow+4, column=0, columnspan=2,
                              sticky='w', pady=(0, 5))

        def createtabelas():
            global widgetNames
            createTabelasButton.grid_forget()
            removeTabelasButton.grid_forget()
            TabelasBox = ttk.Entry(widgets_frame)
            tabelas.append(TabelasBox)

            TabelasBox.grid(column=0, row=len(tabelas)+tabRow, columnspan=2,
                            pady=paddingY, sticky="we")
            label = ttk.Label(widgets_frame, text="Tabela "+str(len(tabelas)+1),
                              font="colortube 11")
            label.grid(column=0, row=len(tabelas)+tabRow, columnspan=2, sticky="nw",
                       padx=5)
            labels.append(label)
            resetWidgets()

        def removetabelas():
            createTabelasButton.grid_forget()
            removeTabelasButton.grid_forget()
            tabelas.pop().grid_forget()
            labels.pop().grid_forget()
            resetWidgets()

        createTabelasButton = ttk.Button(
            widgets_frame, text="+ Tabela", command=createtabelas)
        createTabelasButton.grid(column=0, row=len(
            tabelas)+tabRow+1, columnspan=2, sticky="we", pady=paddingY)
        removeTabelasButton = ttk.Button(
            widgets_frame, text="- Tabela", command=removetabelas)

        # Remap CheckBox
        varRemapCheck = BooleanVar()
        RemapCheck = ttk.Checkbutton(widgets_frame, text='Remap Owner', variable=varRemapCheck, command=toggleRemap,
                                     style='Switch')
        RemapCheck.grid(row=len(tabelas)+tabRow+2, column=0,
                        columnspan=2, sticky='w', pady=(0, 5))

        # Version CheckBox
        varVerCheck = BooleanVar()
        VerCheck = ttk.Checkbutton(
            widgets_frame, text='Version 12.1', variable=varVerCheck, style='Switch')
        VerCheck.grid(row=len(tabelas)+tabRow+3, column=0,
                      columnspan=2, sticky='w', pady=(0, 5))

        # Archive CheckBox
        varArchiveCheck = BooleanVar()
        ArchiveCheck = ttk.Checkbutton(
            widgets_frame, text='Disable Archive', variable=varArchiveCheck, style='Switch')
        ArchiveCheck.grid(row=len(tabelas)+tabRow+4, column=0, columnspan=2,
                          sticky='w', pady=(0, 5))

        # Frame Coluna 2    -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        # Cria widgets_frame2 na janela
        widgets_frame2.grid(row=1, column=1, sticky='nw')

        # Ticket
        ticketBox = ttk.Entry(widgets_frame2)
        ticketBox.grid(column=2, row=1,
                       pady=paddingY, sticky="we")
        ticketBoxLabel = ttk.Label(widgets_frame2, text="Nº Ticket", font="colortube 11").grid(column=2, row=1,
                                                                                                sticky="nw",
                                                                                                padx=5)

        # Base Origem
        base_origemBox = ttk.Entry(widgets_frame2)
        base_origemBox.grid(column=2, row=2, pady=paddingY,
                            sticky="we")
        base_origemBoxLabel = ttk.Label(widgets_frame2, text="Base Origem", font="colortube 11").grid(column=2, row=2,
                                                                                                      sticky="nw",
                                                                                                      padx=5)

        # Base Destino
        varBaseDes = tk.StringVar()
        base_destinoBox = ttk.Entry(
            widgets_frame2, textvariable=varBaseDes)
        base_destinoBox.grid(column=2, row=3, pady=paddingY,
                             sticky="we")
        base_destinoBoxLabel = ttk.Label(widgets_frame2, text="Base Destino", font="colortube 11").grid(column=2, row=3,
                                                                                                        sticky="nw",
                                                                                                        padx=5)

        def script():  # Gera o script de Import
            ticket = ticketBox.get()
            owner = ownerBox.get().upper()
            owner_destino = owner_destinoBox.get().upper()
            base_origem = base_origemBox.get()
            base_destino = base_destinoBox.get().lower()
            tabListName = []
            tabela = tabListName.append(tabelaBox.get().upper())

            def version():
                if varVerCheck.get():
                    ver_text = f""" version=12.1"""
                    return ver_text
                else:
                    return ""

            def remap():
                if varRemapCheck.get():
                    remap_text = f" REMAP_SCHEMA={owner}:{owner_destino} REMAP_TABLESPACE={owner}_DAT:{owner_destino}_DAT,{owner}_IDX:{owner_destino}_IDX"
                    return remap_text
                else:
                    return ""

            def archive():
                if varArchiveCheck.get():
                    archive_text = f" transform=disable_archive_logging:y"
                    return archive_text
                else:
                    return ""

            for tabNames in tabelas:
                tabListName.append(tabNames.get().upper())

            List = []

            def tabs():
                for tabName in tabListName:
                    List.append(f"{owner}.{tabName}, ")
                return "".join(List)[:-2]

            # Subistitui valores no script
            script = f"""--ORIGEM: {base_origem.upper()}
export ORACLE_SID={base_origem.lower()}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
expdp BKP_EXPORT/AxxxM0 directory=DBA tables={tabs()} dumpfile={ticket}.dmp logfile=exp_{ticket}.log exclude=statistics{version()}

--Destino: {base_destino.upper()}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
impdp BKP_IMPORT/AxxxM0 directory=DBA dumpfile={ticket}.dmp logfile=imp_{ticket}.log{remap()}{archive()}"""

            # Cria ou sobreescreve o aquivo import.txt
            f = open("import.txt", "w+")
            f.write(script)  # Escreve o script gerado
            f.close()  # Fecha o arquivo import.txt
            os.startfile("import.txt")  # Abre o arquivo import.txt

        accentbutton = ttk.Button(
            self, text="Gerar", style="AccentButton", command=script)
        accentbutton.grid(row=11, column=1, pady=20, sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=11, column=0, padx=(
            paddingY + 30, paddingY), pady=20, sticky='nswe')


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
