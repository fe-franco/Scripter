from email.policy import default
from pickle import FALSE
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, BooleanVar, END
import os

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
        for F in (StartPage, PageOne, PageTwo):
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


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        pad = 79
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        labelTitle = ttk.Label(
            self, text="Gerador de Scripts", font=controller.title_font, justify="center")
        labelTitle.grid(sticky='we', column=0, row=0, pady=(20, 0), padx=pad)
        labelSubtitle = ttk.Label(self, text="Escolha uma opção abaixo", font=controller.sub_font, foreground='grey',
                                  justify="center")
        labelSubtitle.grid(sticky='we', column=0, row=1,
                           pady=(10, 20), padx=pad + 20)

        button1 = ttk.Button(self, text="Import de Owner", style="AccentButton",
                             command=lambda: controller.show_frame("PageOne"))
        button2 = ttk.Button(self, text="Import de Tabela", style="AccentButton",
                             command=lambda: controller.show_frame("PageTwo"))
        button1.grid(sticky='we', column=0, row=2, pady=10, padx=20)
        button2.grid(sticky='we', column=0, row=3, pady=10, padx=20)
        


class PageOne(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Localização das caixas -----------------------------------------------------------------------------------------------------------------------------
        paddingY = 10

        # Titulo ---------------------------------------------------------------------------------------------------------------------------------------------
        titulo = ttk.Label(self, text="Import de Owner",
                           font=controller.title_font, foreground="white")
        titulo.grid(row=0, column=0, pady=20, columnspan=4)

        # Frame Coluna 1 -------------------------------------------------------------------------------------------------------------------------------------
        widgets_frame = ttk.Frame(self)
        widgets_frame.grid(row=1, column=0, sticky='new',
                           padx=(paddingY, paddingY))

        # Owners
        global owners
        global MAX_ROWS
        global start_col
        global createOwnersButton
        global removeOwnersButton
        global frames
        TESTE = 1
        MAX_ROWS = 3
        MAX_COLS = 2
        owners = []
        start_col = -2
        # Frame
        frames = []

        def validate(input):
            if input.isdigit():
                print(input)
                return True

            elif input == "":
                print(input)
                return True

            else:
                print(input)
                return False

        def createFrame():
            global frames
            defaultFrame = ttk.Frame(widgets_frame)
            frames.append(defaultFrame)

        def resetWidgets(start_row, start_col, frame):
            global createOwnersButton
            global removeOwnersButton

            createOwnersButton = ttk.Button(
                frame, text="+ Owner", command=createOwners)
            removeOwnersButton = ttk.Button(
                frame, text="- Owner", command=removeOwners)

            if len(owners) > 1:
                removeOwnersButton.grid(
                    column=1+start_col, row=start_row+9, sticky="nwe", pady=paddingY*2.5, padx=(2.5, 0))
                createOwnersButton.grid(
                    column=start_col, row=start_row+9, sticky="new", pady=paddingY*2.5, padx=(0, 2.5))
            else:
                removeOwnersButton.grid_forget()
                createOwnersButton.grid(
                    column=start_col, row=start_row+9, columnspan=2, sticky="new", pady=paddingY*2.5)

            if start_col == 2:
                createOwnersButton.grid_configure(
                    padx=(paddingY*2, 2.5), pady=paddingY)
                removeOwnersButton.grid_configure(pady=paddingY)
                if MAX_COLS*MAX_ROWS == len(owners):
                    print("Não é possível adicionar mais owners")
                    createOwnersButton.grid_forget()
                    removeOwnersButton.grid_forget()
                    removeOwnersButton = ttk.Button(
                        widgets_frame2, text="- Owner", command=removeOwners)
                    removeOwnersButton.grid(
                        row=8, column=2, columnspan=2, sticky="ew", pady=paddingY)

            print("Final row: " + str(start_row+7), " | Final col: " + str(start_col), " | Final frame: " + str(frame.grid_info()["column"])+","+ str(frame.grid_info()["row"])+"\n")
            # print(str(MAX_COLS*MAX_ROWS))
            # print(str(len(owners))+"\n")

        def createOwners():
            global start_col
            global MAX_ROWS
            global owners
            if MAX_COLS*MAX_ROWS == len(owners):
                return

            createOwnersButton.grid_forget()
            removeOwnersButton.grid_forget()

            # Mostrar ou esconder Senha
            def toggleSenha():
                if var_senha_check.get():
                    senha.grid()
                    label_senha.grid()
                else:
                    senha.grid_remove()
                    label_senha.grid_remove()

            # Mostrar ou esconder Owner Destino
            def toggleRemap():
                if var_remap_check.get():
                    my_string = label_origem.config()["text"][4]
                    split_strings = my_string.split()
                    split_strings.insert(1, 'Origem')
                    label_origem.config(text=split_strings)
                    owner_destino.grid()
                    label_destino.grid()
                else:
                    my_string = label_origem.config()["text"][4]
                    split_strings = my_string.split()
                    split_strings.pop(1)
                    label_origem.config(text=split_strings)
                    owner_destino.grid_remove()
                    label_destino.grid_remove()

            start_row = (len(owners) % MAX_ROWS) * 8
            #print("Remainder of "+str(MAX_ROWS)+": "+str((len(owners)) % MAX_ROWS))
            #print(str((len(owners)) % MAX_ROWS)+"*7 = "+str(start_row))
            if len(owners) % MAX_ROWS == 0:
                start_col += 2
                createFrame()

            frame = frames[len(frames) - 1]

            if len(owners) % MAX_ROWS == 0:
                frame.grid(row=start_row, column=start_col,
                           sticky="new", padx=(paddingY, paddingY))

            # Owner Origem widget
            reg = frame.register(validate)
            owner_origem = ttk.Entry(
                frame, validate="key", validatecommand=(reg, '%P'))
            label_origem = ttk.Label(frame, text="Owner",
                                     font="colortube 11")
            # Owner Destino widget
            owner_destino = ttk.Entry(frame)
            label_destino = ttk.Label(frame, text="Owner Destino",
                                      font="colortube 11")

            # Senha widget
            senha = ttk.Entry(frame)
            label_senha = ttk.Label(frame, text="Senha",
                                    font="colortube 11")

            # Senha CheckBox widget
            var_senha_check = tk.BooleanVar()
            senha_check = ttk.Checkbutton(frame, variable=var_senha_check, text="Senha", command=toggleSenha,
                                          style='Switch')
            # Remap CheckBox widget
            var_remap_check = tk.BooleanVar()
            remap_check = ttk.Checkbutton(frame, text='Remap Owner', variable=var_remap_check, command=toggleRemap,
                                          style='Switch')

            # Drop CheckBox widget
            var_drop_check = BooleanVar()
            drop_check = ttk.Checkbutton(
                frame, text='Dropar Owner', variable=var_drop_check, style='Switch')

            # Nº DataFiles widget
            var_data = tk.IntVar()
            data_file_spin = ttk.Spinbox(
                frame, from_=1, to=99, width=5, textvariable=var_data)
            data_file_spin_label = ttk.Label(
                frame, text='N° de DataFiles', font="colortube 11")

            # Separator
            separator = ttk.Separator(frame, orient="horizontal")

            owners.append({
                "frame": frame,
                "owner_origem": owner_origem,
                "label_origem": label_origem,
                "owner_destino": owner_destino,
                "label_destino": label_destino,
                "senha_check": senha_check,
                "senha": senha,
                "label_senha": label_senha,
                "var_senha_check": var_senha_check,
                "remap_check": remap_check,
                "var_remap_check": var_remap_check,
                "drop_check": drop_check,
                "var_drop_check": var_drop_check,
                "data_file_spin": data_file_spin,
                "data_file_spin_label": data_file_spin_label,
                "var_data": var_data,
                "separator": separator
            })
            # Changes labels based on owner count
            if len(owners) > 1:
                owners[0]["label_origem"].configure(text="Owner 1")
                owners[0]["label_destino"].configure(text="Owner Destino 1")
                owners[0]["label_senha"].configure(text="Senha 1")
                owners[0]["data_file_spin_label"].configure(
                    text="N° de DataFiles 1")
                label_origem.config(text="Owner "+str(len(owners)))
                label_destino.config(text="Owner Destino "+str(len(owners)))
                label_senha.config(text="Senha "+str(len(owners)))
                data_file_spin_label.config(
                    text='N° de DataFiles '+str(len(owners)))
                owners[0]["separator"].grid()

                if owners[0]["var_remap_check"].get():
                    owners[0]["label_origem"].configure(text="Owner Origem 1")

            # Separator
            separator.grid(row=start_row, column=0, columnspan=2,
                           sticky='we')
        
                
            # Owner Origem
            owner_origem.grid(column=0, row=start_row+1, columnspan=2,
                              pady=(paddingY*2.5, paddingY), sticky="we")
            label_origem.grid(column=0, row=start_row+1, columnspan=2, sticky="nw",
                              padx=5, pady=paddingY*((owner_origem.grid_info()["pady"][0]/paddingY)-1))
            if len(owners) % MAX_ROWS == 1:
                owner_origem.grid_configure(pady=paddingY)
                label_origem.grid_configure(pady=0, padx=5)

            # Senha
            senha.grid(column=0, row=start_row+2, pady=paddingY,
                       columnspan=2, sticky="we")
            senha.grid_remove()

            label_senha.grid(column=0, row=start_row+1,
                             columnspan=2, sticky="nw", padx=5)
            label_senha.grid_remove()

            # Owner Destino
            owner_destino.grid(
                column=0, row=start_row+3, pady=paddingY, columnspan=2, sticky="we")
            owner_destino.grid_remove()
            label_destino.grid(column=0, row=start_row+2,
                               sticky="nw", columnspan=2, padx=5)
            label_destino.grid_remove()

            # Nº DataFiles
            data_file_spin.grid(column=0, row=start_row+4,
                                pady=paddingY, columnspan=2, sticky="we")
            data_file_spin_label.grid(column=0, row=start_row+3,
                                      sticky="nw", columnspan=2, padx=(5, 55))

            # Senha CheckBox
            senha_check.grid(column=0, row=start_row+5,
                             columnspan=2, sticky='w', pady=(0, paddingY/2))

            # Remap CheckBox
            remap_check.grid(column=0, row=start_row+6,
                             columnspan=2, sticky='w', pady=(0, paddingY/2))

            # Drop CheckBox
            drop_check.grid(column=0, row=start_row+7,
                            columnspan=2, sticky='w', pady=(0, paddingY*2.5))

            if len(owners) % MAX_ROWS == 1:
                separator.grid_forget()

            bstart_col = 0
            bstart_row = start_row
            if len(owners) % MAX_ROWS == 0:
                bstart_col = 2
                bstart_row = -8

            #print("Start row: " + str(bstart_row), " | Start col: " + str(start_col), " | Start frame: " + str(frame.grid_info()["column"])+","+ str(frame.grid_info()["row"]))
            resetWidgets(bstart_row, bstart_col, frame)

        def removeOwners():
            createOwnersButton.grid_forget()
            removeOwnersButton.grid_forget()
            # offset row by lenght of owners
            owner = owners.pop()
            owner["owner_origem"].grid_forget()
            owner["label_origem"].grid_forget()
            owner["owner_destino"].grid_forget()
            owner["label_destino"].grid_forget()
            owner["senha_check"].grid_forget()
            owner["senha"].grid_forget()
            owner["label_senha"].grid_forget()
            owner["remap_check"].grid_forget()
            owner["drop_check"].grid_forget()
            owner["data_file_spin"].grid_forget()
            owner["data_file_spin_label"].grid_forget()
            owner["separator"].grid_forget()

            start_row = ((len(owners)) % MAX_ROWS) * 8
            bstart_col = 0
            #print("Remainder of "+str(MAX_ROWS)+": "+str((len(owners)) % MAX_ROWS))
            #print(str((len(owners)) % MAX_ROWS)+"*7 = "+str(start_row))

            if len(owners) < 2:
                owners[0]["label_origem"].configure(text="Owner")
                owners[0]["label_destino"].configure(text="Owner Destino")
                owners[0]["label_senha"].configure(text="Senha")
                owners[0]["data_file_spin_label"].configure(
                    text="N° de DataFiles")
                if owners[0]["var_remap_check"].get():
                    owners[0]["label_origem"].configure(text="Owner Origem")

            bstart_row = start_row
            if len(owners) % MAX_ROWS == 0:
                frames.pop().grid_forget()
                bstart_col = 2
                bstart_row = -8

            frame = frames[len(frames) - 1]

            #print("Start row: " + str(bstart_row), " | Start col: " + str(start_col), " | Start frame: " + str(frame.grid_info()["column"])+","+ str(frame.grid_info()["row"]))
            resetWidgets(bstart_row, bstart_col, frame)

        createOwnersButton = ttk.Button(
            widgets_frame, text="+ Owner", command=createOwners)
        createOwnersButton.grid(
            column=0, row=7, columnspan=2, sticky="we", pady=paddingY)
        removeOwnersButton = ttk.Button(
            widgets_frame, text="- Owner", command=removeOwners)

        # Frame Coluna 2    -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky='nw',
                            padx=(paddingY, paddingY + 15))  # Cria widgets_frame2 na janela
        for i in range(TESTE):
            createOwners()
        # Ticket
        ticketBox = ttk.Entry(widgets_frame2)
        ticketBox.grid(column=2, row=1, columnspan=2,
                       pady=paddingY, sticky="we")
        ticketBoxLabel = ttk.Label(widgets_frame2, text="Nº Ticket", font="colortube 11").grid(column=2, row=1,
                                                                                               sticky="nw",
                                                                                               padx=5)

        # Base Origem
        base_origemBox = ttk.Entry(widgets_frame2)
        base_origemBox.grid(column=2, row=2, pady=paddingY,
                            columnspan=2, sticky="we")
        base_origemBoxLabel = ttk.Label(widgets_frame2, text="Base Origem", font="colortube 11").grid(column=2, row=2,
                                                                                                      sticky="nw",
                                                                                                      padx=5)

        # Base Destino
        varBaseDes = tk.StringVar()
        base_destinoBox = ttk.Entry(
            widgets_frame2, textvariable=varBaseDes, width=13)
        base_destinoBox.grid(column=2, row=3, sticky="we")
        base_destinoBoxLabel = ttk.Label(widgets_frame2, text="Base Destino", font="colortube 11").grid(column=2, row=3,
                                                                                                        sticky="nw",
                                                                                                        padx=5)

        # DataNum
        varDataNum = tk.StringVar()
        dataNumSpin = ttk.Spinbox(
            widgets_frame2, from_=1, to=99, width=5, textvariable=varDataNum)
        dataNumSpin.grid(column=3, row=3, sticky="we", pady=paddingY)

        # Caminho
        def resize(*args):  # Atuliza width da caminhoBox baseado no texto
            text = ("/storage/" + varBaseDes.get().lower() +
                    "/data0" + varDataNum.get())
            caminhoBox.configure(state='enabled')
            caminhoBox.delete(0, 'end')
            widget_width = 0
            if len(text) != widget_width:
                widget_width = len(text) + 1
                caminhoBox.insert(END, text)
                caminhoBox.configure(width=widget_width, state='disabled')
                caminhoBox.grid(row=5, column=2, pady=10, sticky='we')

        caminhoBox = ttk.Entry(widgets_frame2, justify='center')
        caminhoBox.insert(0, "/storage/----/data0-")
        caminhoBox.configure(state='disabled')
        caminhoBoxLabel = ttk.Label(
            widgets_frame2, text='Caminho DataFiles', font="colortube 11")
        caminhoBoxLabel.grid(row=5, column=2, sticky="nw", padx=5)
        caminhoBox.grid(row=5, column=2, columnspan=2, pady=10, sticky='we')

        # Listener para varBaseDes chama função resize
        varBaseDes.trace('w', resize)

        # Listener para varDataNum chama função resize
        varDataNum.trace('w', resize)

        # Version CheckBox
        varVerCheck = BooleanVar()
        VerCheck = ttk.Checkbutton(
            widgets_frame2, text='Version 12.1', variable=varVerCheck, style='Switch')
        VerCheck.grid(row=6, column=2, columnspan=2, sticky='w', pady=(0, 5))

        # Metadata CheckBox
        varMetaCheck = BooleanVar()
        MetaCheck = ttk.Checkbutton(
            widgets_frame2, text='Metadata Only', variable=varMetaCheck, style='Switch')
        MetaCheck.grid(row=8, column=2, columnspan=2, sticky='w')

        def script():  # Gera o script de Import
            ticket = ticketBox.get()
            base_origem = base_origemBox.get()
            base_destino = base_destinoBox.get()
            data_num = dataNumSpin.get()
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
            for ownerData in owners:
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
                    f"create tablespace {owner}_DAT '{caminho}/{owner}_DAT.dbf' size 100m autoextend on next 100m;\n")
                for datafile in range(dataFiles-1):
                    if dataFiles > 1:
                        datafiles_comand.append(
                            f"alter tablespace {owner}_DAT add datafile '{caminho}/{owner}_DAT{datafile+2}.dbf' size 100m autoextend on next 100m;\n")

                datafiles_comand.append(
                    f"create tablespace {owner}_IDX '{caminho}/{owner}_IDX.dbf' size 100m autoextend on next 100m;\n")
                datafiles_comand.append(
                    f"create user {owner} identified by {owner} default tablespace {owner}_DAT temporary tablespace TEMP quota unlimited on {owner}_DAT quota unlimited on {owner}_IDX quota 0k on SYSTEM;\n\n")

                if ownerData["var_remap_check"].get():
                    a = "".join(schemas_remap)[:-1].upper()
                    b = "".join(tablespaces)[:-1].upper()
                    remap = remap + f" REMAP_SCHEMA={a} REMAP_SCHEMA={b}"

                unlock.append(f"""alter user {owner} identified by {senha} account unlock;\n
BEGIN
DBMS_NETWORK_ACL_ADMIN.append_host_ace (
    host       => '*',
    ace        => xs$ace_type(privilege_list => xs$name_list('connect','resolve'),
                            principal_name => '{owner}',
                            principal_type => XS_ACL.PTYPE_DB));
END;
/\n\n""")

            script = f"""--ORIGEM: {base_origem.upper()}
export ORACLE_SID={base_origem.lower()}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
expdp BKP_EXPORT/AxxxM0 directory=DBA schemas={"".join(schemas)[:-1].upper()} dumpfile={ticket}.dmp logfile=exp_{ticket}.log exclude=statistics{version}{metadata}

--DESTINO: {base_destino.upper()}

{"".join(drops)}{"".join(datafiles_comand)}
impdp BKP_IMPORT/AxxxM0 directory=DBA dumpfile={ticket}.dmp logfile=imp_{ticket}.log{remap}

{"".join(unlock)}
"""

            # Cria ou sobreescreve o aquivo import.txt
            f = open("import.txt", "w+")
            f.write(script)  # Escreve o script gerado
            f.close()  # Fecha o arquivo import.txt
            os.startfile("import.txt")  # Abre o arquivo import.txt

        accentbutton = ttk.Button(
            self, text="Gerar", style="AccentButton", command=script)
        accentbutton.grid(row=11, column=1, padx=10, pady=20, sticky='nswe')
        button = ttk.Button(self, text="Voltar ao início",
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=11, column=0, padx=10, pady=20, sticky='nswe')


class PageTwo(tk.Frame):

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
            widgets_frame2, textvariable=varBaseDes, width=13)
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
