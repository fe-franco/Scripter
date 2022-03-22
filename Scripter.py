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
                           padx=(paddingY + 15, paddingY))

        # Owner
        ownerBox = ttk.Entry(widgets_frame)
        ownerBox.grid(column=0, row=1, pady=paddingY, sticky="we")
        ownerBoxLabel = ttk.Label(widgets_frame, text="Owner", font="colortube 11").grid(column=0, row=1, sticky="nw",
                                                                                         padx=5)

        # Senha
        def toggleSenha():
            if varSenhaCheck.get():
                SenhaBox.grid(column=0, row=2, pady=paddingY, sticky="we")
                SenhaBoxLabel.grid(column=0, row=2, sticky="nw", padx=5)
            else:
                SenhaBox.grid_forget()
                SenhaBoxLabel.grid_forget()

        SenhaBox = ttk.Entry(widgets_frame)
        SenhaBoxLabel = ttk.Label(
            widgets_frame, text="Senha", font="colortube 11")

        # Owner Destino
        def toggleRemap():
            if varRemapCheck.get():
                owner_destinoBox.grid(
                    column=0, row=3, pady=paddingY, sticky="we")
                owner_destinoBoxLabel.grid(
                    column=0, row=3, sticky="nw", padx=5)
            else:
                owner_destinoBox.grid_forget()
                owner_destinoBoxLabel.grid_forget()

        owner_destinoBox = ttk.Entry(widgets_frame)
        owner_destinoBoxLabel = ttk.Label(
            widgets_frame, text="Owner Destino", font="colortube 11")

        # Senha CheckBox
        varSenhaCheck = BooleanVar()
        SenhaCheck = ttk.Checkbutton(widgets_frame, variable=varSenhaCheck, text="Senha", command=toggleSenha,
                                     style='Switch')
        SenhaCheck.grid(row=6, column=0, sticky='w', pady=(0, 5))

        # Remap CheckBox
        varRemapCheck = BooleanVar()
        RemapCheck = ttk.Checkbutton(widgets_frame, text='Remap Owner', variable=varRemapCheck, command=toggleRemap,
                                     style='Switch')
        RemapCheck.grid(row=7, column=0, sticky='w', pady=(0, 5))

        # Drop CheckBox
        varDropCheck = BooleanVar()
        DropCheck = ttk.Checkbutton(
            widgets_frame, text='Dropar Owner', variable=varDropCheck, style='Switch')
        DropCheck.grid(row=8, column=0, sticky='w', pady=(0, 5))
        drop_text = ""

        # Version CheckBox
        varVerCheck = BooleanVar()
        VerCheck = ttk.Checkbutton(
            widgets_frame, text='Version 12.1', variable=varVerCheck, style='Switch')
        VerCheck.grid(row=9, column=0, sticky='w', pady=(0, 5))

        # Metadata CheckBox
        varMetaCheck = BooleanVar()
        MetaCheck = ttk.Checkbutton(
            widgets_frame, text='Metadata Only', variable=varMetaCheck, style='Switch')
        MetaCheck.grid(row=10, column=0, sticky='w')

        # Frame Coluna 2    -----------------------------------------------------------------------------------------------------------------------------------
        widgets_frame2 = tk.Frame(self)
        widgets_frame2.grid(row=1, column=1, sticky='nw',
                            padx=(paddingY, paddingY + 15))  # Cria widgets_frame2 na janela

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

        # Nº DataFiles
        varData = tk.IntVar()
        dataFileSpin = ttk.Spinbox(
            widgets_frame2, from_=1, to=99, width=5, textvariable=varData)
        dataFileSpin.grid(row=8, column=2, columnspan=2, pady=7)
        dataFileSpinLabel = ttk.Label(
            widgets_frame2, text='Nº de DataFiles', font="colortube 11")
        dataFileSpinLabel.grid(row=7, column=2, columnspan=2)

        def script():  # Gera o script de Import
            ticket = ticketBox.get()
            owner = ownerBox.get().upper()
            senha = SenhaBox.get()
            base_origem = base_origemBox.get()
            base_destino = base_destinoBox.get().lower()
            dataNum = dataNumSpin.get()
            dataFile = int(dataFileSpin.get())
            List = []
            if varRemapCheck.get():
                owner_destino = owner_destinoBox.get().upper()
            else:
                owner_destino = ownerBox.get().upper()

            def dataDivid():  # Gera DataFiles adicionais
                if dataFile > 1:
                    for i in range(dataFile - 1):
                        List.append(
                            f"""ALTER TABLESPACE {owner_destino}_DAT ADD DATAFILE '/storage/{base_destino}/data0{dataNum}/{owner_destino}_DAT{i + 2}.dbf' SIZE 100M AUTOEXTEND ON NEXT 100M; \n""")
                    return "".join(List)
                else:
                    return ""

            def drop():
                if varDropCheck.get():  # Adiciona drop_text se Drop estiver com check
                    drop_text = f"""DROP USER {owner_destino} CASCADE;
DROP TABLESPACE {owner_destino}_DAT INCLUDING CONTENTS AND DATAFILES;
DROP TABLESPACE {owner_destino}_IDX INCLUDING CONTENTS AND DATAFILES;
                """
                    return drop_text
                else:
                    return ""

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

            def senhafunc():
                if varSenhaCheck.get():
                    return senha
                else:
                    return owner_destino

            def meta():
                if varMetaCheck.get():
                    Meta_text = f""" CONTENT=METADATA_ONLY"""
                    return Meta_text
                else:
                    return ""

            # Subistitui valores no script
            script = f"""--ORIGEM: {base_origem.upper()}
export ORACLE_SID={base_origem.lower()}
export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
expdp BKP_EXPORT/AxxxM0 directory=DBA schemas={owner} dumpfile={ticket}.dmp logfile=exp_{ticket}.log exclude=statistics{version()}{meta()}

--Destino: {base_destino.upper()}
{drop()}
create tablespace {owner_destino}_DAT datafile '/storage/{base_destino}/data0{dataNum}/{owner_destino}_DAT.dbf' size 100m autoextend on next 100m;
{dataDivid()}
create tablespace {owner_destino}_IDX datafile '/storage/{base_destino}/data0{dataNum}/{owner_destino}_IDX.dbf' size 100m autoextend on next 100m;

create user {owner_destino} identified by {senhafunc()} default tablespace {owner_destino}_DAT temporary tablespace TEMP quota unlimited on {owner_destino}_DAT quota unlimited on {owner_destino}_IDX quota 0k on SYSTEM;

export NLS_LANG="BRAZILIAN PORTUGUESE_BRAZIL.WE8MSWIN1252"
impdp BKP_IMPORT/AxxxM0 directory=DBA dumpfile={ticket}.dmp logfile=imp_{ticket}.log{remap()}

alter user {owner_destino} identified by {senhafunc()} account unlock;

BEGIN
DBMS_NETWORK_ACL_ADMIN.append_host_ace (
    host       => '*',
    ace        => xs$ace_type(privilege_list => xs$name_list('connect','resolve'),
                            principal_name => '{owner_destino}',
                            principal_type => XS_ACL.PTYPE_DB));
END;
/"""

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
            if len(tabelas) > 0:
                removeTabelasButton.grid_forget()
                removeTabelasButton.grid(column=1, row=len(tabelas)+tabRow+1, sticky="w", pady=paddingY, padx=(2.5,0))
                createTabelasButton.grid(column=0, row=len(tabelas)+tabRow+1, sticky="e", pady=paddingY, padx=(0,2.5))
            else:
                createTabelasButton.grid(column=0, row=len(tabelas)+tabRow+1, columnspan=2, sticky="we", pady=paddingY)
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

            TabelasBox.grid(column=0, row=len(tabelas)+tabRow, columnspan=2, pady=paddingY, sticky="we")
            label = ttk.Label(widgets_frame, text="Tabela "+str(len(tabelas)+1),
                              font="colortube 11")
            label.grid(column=0, row=len(tabelas)+tabRow, sticky="nw",
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
        createTabelasButton.grid(column=0, row=len(tabelas)+tabRow+1, columnspan=2, sticky="we", pady=paddingY)
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
