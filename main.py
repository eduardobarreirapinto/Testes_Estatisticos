import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import pandas as pd
import dados
import grubbs
import shapiro_wilk

class TabController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Testes Estatísticos')
        #self.root.geometry('750x650')
        self.root.state('zoomed')  # Inicializa a janela em tela cheia

        #  font para buttom
        self.custom_font = tkFont.Font(size=18)
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', font=('Helvetica', 12))

        # font para  tab text
        tab_font = ('Helvetica', 8, 'bold')  # You can adjust the font family, size, and style
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=tab_font)

        self.df = pd.DataFrame()

        self.tab_control = ttk.Notebook(self.root)

        self.dados_tab = dados.create_tab(self.tab_control, self)
        self.grubbs_tab = grubbs.create_tab(self.tab_control, self)
        self.shapiro_wilk_tab = shapiro_wilk.create_tab(self.tab_control, self)

        self.tab_control.pack(expand=1, fill='both')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    controller = TabController()
    controller.run()
