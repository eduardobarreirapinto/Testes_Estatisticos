import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
from dados import get_df

def create_tab(tab_control):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Grubbs')
    label = ttk.Label(tab, text='AVALIAÇÃO DE OUTLIERS - GRUBBS')
    label.pack()
    def atualizar_tabela():
        df = get_df()
        tableframe = ttk.Frame(tab)
        tableframe.pack()
        #df = TableModel.getSampleData()
        pt = Table(tableframe, dataframe=df,showtoolbar=True, showstatusbar=True)
        pt.show()

    update_button = ttk.Button(tab, text='Atualizar Tabela', command=atualizar_tabela)
    update_button.pack()
