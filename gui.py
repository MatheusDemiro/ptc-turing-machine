from tkinter import *

from tm import TM


class GUI:
    def __init__(self):
        self.root = Tk()
        self.cTableContainer = Canvas(self.root)

        self.homeFrame = Frame(self.root)
        self.runFrame = Frame(self.root)
        self.commandsFrame = Frame(self.root)

        self.responseScroll = Scrollbar(self.runFrame, orient='vertical')
        self.transitionsScroll = Scrollbar(self.runFrame, orient='vertical')

        self.fileNameInput = Text(self.homeFrame, height=1, width=20)
        self.machineInput = Text(self.runFrame, height=1, width=20)
        self.lt = Text(self.runFrame, height=1, width=6)
        self.rt = Text(self.runFrame, height=1, width=6)

        self.response = Text(self.runFrame, width=50)
        self.transitionsResponse = Text(self.runFrame, width=50)
        self.fileNameErrorLabel = Label(self.homeFrame, text="", fg="red")
        self.machineInputErrorLabel = Label(self.runFrame, text="", fg="red")

        self.play = Button(self.runFrame, text="Executar", command=self.on_click_play)
        self.next = Button(self.runFrame, text="Continuar", state="disabled")
        self.btnLoad = None

        self.selectedMode = StringVar(self.runFrame, value=0)
        self.dropdown = OptionMenu(self.runFrame, self.selectedMode, "0", "1", "2")

        self.tm = TM(self.response, self.transitionsResponse, self.next)

        self.next.configure(command=lambda: self.on_click_next())

    def initialize_frames(self):
        for frame in (self.homeFrame, self.runFrame):
            frame.grid(row=0, column=0, sticky="news")

        self.create_home_frame()
        self.create_run_frame()

        self.open_frame(self.homeFrame)
        self.root.title("Máquina de Turing Ingênua")
        self.root.maxsize(1000, 1000)
        self.root.minsize(1000, 400)
        self.root.mainloop()

    def create_home_frame(self):
        Label(self.homeFrame, text="Informe o nome do arquivo '.tm'").pack(pady=(200, 0))

        self.fileNameInput.pack(padx=210)
        self.fileNameErrorLabel.pack()

        self.btnLoad = Button(self.homeFrame, text="Carregar arquivo", command=self.on_click_load_file)

        self.btnLoad.pack(pady=(0, 10))

        Label(self.homeFrame, text="OBS.: informe o nome do arquivo '.tm' da pasta machines que deseja executar.",
              fg="red").pack(pady=(0, 10), padx=10)

    def create_run_frame(self):
        Button(self.runFrame, text="Voltar", command=lambda: self.open_frame(self.homeFrame)).grid(row=0, column=0,
                                                                                                   padx=(0, 400),
                                                                                                   pady=(10, 0))

        Label(self.runFrame, text="Entrada da Máquina de Turing").grid(row=1, padx=(0, 50))
        Label(self.runFrame, text="S").grid(row=1, padx=(425, 0))
        Label(self.runFrame, text="RT").grid(row=1, padx=(300, 0))
        Label(self.runFrame, text="LT").grid(row=1, padx=(190, 0))

        self.machineInput.grid(row=2, padx=(0, 50))
        self.dropdown.grid(row=2, column=0, padx=(425, 0))
        self.rt.grid(row=2, padx=(300, 0))
        self.lt.grid(row=2, padx=(190, 0))

        self.machineInputErrorLabel.grid(row=5, padx=(100, 0))

        self.play.grid(row=6, column=0, padx=(30, 0))
        self.next.grid(row=6, column=0, padx=(180, 0))

        Label(self.runFrame, text="FITA").grid(row=7, padx=(100, 0), pady=(20, 0))
        Label(self.runFrame, text="TRANSIÇÕES").grid(row=7, column=2, padx=(20, 0))

        self.response.grid(row=8, pady=20, padx=(100, 0))
        self.transitionsResponse.grid(row=8, column=2, padx=(50, 0))

        self.response.config(yscrollcommand=self.responseScroll.set)
        self.transitionsResponse.config(yscrollcommand=self.transitionsScroll.set)

        self.responseScroll.config(command=self.response.xview)
        self.transitionsScroll.config(command=self.transitionsResponse.xview)

        self.responseScroll.grid(row=8, column=1, sticky=NS, pady=20)
        self.transitionsScroll.grid(row=8, column=3, sticky=NS, pady=20)

    def loading(self):
        self.btnLoad.configure(state="disabled")
        self.fileNameErrorLabel.configure(text="Carregando arquivo...", fg="green")
        self.root.after(1000, lambda: self.fileNameErrorLabel.configure(text="Arquivo carregado com sucesso!",
                                                                        fg="green"))
        self.root.after(1000, lambda: self.open_frame(self.runFrame))
        self.root.after(1000, lambda: self.btnLoad.configure(state="normal"))
        self.root.after(1000, lambda: self.clear_home_frame())

    def clear_home_frame(self):
        self.fileNameErrorLabel.configure(text="", fg="red")

    def on_click_load_file(self):
        if self.tm.load_turing_machine(self.fileNameInput.get("1.0", "end-1c")):
            self.loading()
        else:
            self.show_error(self.fileNameErrorLabel, "Arquivo não localizado na pasta 'machines'.")

    def on_click_play(self):
        machineInput = self.machineInput.get("1.0", "end-1c")
        lt = self.lt.get("1.0", "end-1c")
        rt = self.rt.get("1.0", "end-1c")
        fileName = self.fileNameInput.get("1.0", "end-1c")

        if machineInput == "" or machineInput is None:
            self.show_error(self.machineInputErrorLabel, "Entrada inválida.")
        elif not lt.isdecimal() or not rt.isdecimal():
            self.show_error(self.machineInputErrorLabel, "RT e LT devem ser números inteiros.")
        else:
            self.response.delete('1.0', END)
            self.transitionsResponse.delete('1.0', END)
            self.machineInputErrorLabel.configure(text="")

            if self.selectedMode.get() == "1":
                self.next.configure(state="normal")
            else:
                self.next.configure(state="disabled")

            self.tm.execute(fileName, machineInput, lt, rt, self.selectedMode.get())

    def on_click_next(self):
        self.response.yview_moveto('1.0')
        self.transitionsResponse.yview_moveto('1.0')

        self.tm.var.set(1)

    @staticmethod
    def show_error(label, message):
        label.configure(text=message)

    @staticmethod
    def open_frame(frame):
        frame.tkraise()
