from tkinter import *

from tm import TM


class GUI:
    def __init__(self):
        self.root = Tk()
        self.homeFrame = Frame(self.root)
        self.runFrame = Frame(self.root)
        self.response = Label(self.runFrame, text="")
        self.input = Text(self.homeFrame, height=1, width=20)
        self.fileNameErrorLabel = Label(self.homeFrame, text="", fg="red")
        self.btnLoad = None
        self.tm = TM(self.response)

    def initialize_frames(self):
        for frame in (self.homeFrame, self.runFrame):
            frame.grid(row=0, column=0, sticky="news")

        self.create_home_frame()
        self.create_input_frame()

        self.open_frame(self.homeFrame)
        self.root.title("Máquina de Turing ingênua")
        self.root.mainloop()

    def create_home_frame(self):
        Label(self.homeFrame, text="Informe o nome do arquivo '.tm'").pack()
        self.input.pack(padx=50)
        self.fileNameErrorLabel.pack()

        self.btnLoad = Button(self.homeFrame, text="Carregar arquivo",
                              command=lambda: self.loading()
                              if self.tm.load_turing_machine(self.input.get("1.0", "end-1c"))
                              else self.show_error())

        self.btnLoad.pack(pady=(0, 10))

    def create_input_frame(self):
        Button(self.runFrame, text="Voltar", command=lambda: self.open_frame(self.homeFrame)).pack()

        self.response.pack()

    def show_error(self):
        self.fileNameErrorLabel.configure(text="Arquivo não localizado na pasta 'machines'.")

    def loading(self):
        self.btnLoad.configure(state="disabled")
        self.fileNameErrorLabel.configure(text="Carregando arquivo...", fg="green")
        self.root.after(1000, lambda: self.fileNameErrorLabel.configure(text="Arquivo carregado com sucesso!",
                                                                        fg="green"))
        self.root.after(1000, lambda: self.open_frame(self.runFrame))
        self.root.after(1000, lambda: self.btnLoad.configure(state="normal"))
        self.root.after(1000, lambda: self.clear_home_frame())

    def clear_home_frame(self):
        self.fileNameErrorLabel.configure(text="")

    @staticmethod
    def open_frame(frame):
        frame.tkraise()
