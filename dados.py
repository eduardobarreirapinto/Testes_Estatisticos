import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from pandastable import Table, TableModel

df = None

def get_df():
    return df

def create_tab(tab_control):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Dados')
    label_message = ttk.Label(tab, text='')
    tableframe = ttk.Frame(tab)
    tableframe.pack()
    pt = Table(tableframe, showtoolbar=False, showstatusbar=False)

    def import_excel(criar_ou_atualizar):
        global df
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                df = ler_planilha(file_path)
                if criar_ou_atualizar == 'criar_tabela':
                    criar_tabela(df)
                else:
                    atualizar_tabela(df)

            except Exception as e:
                message = "Erro ao importar arquivo."
                label_message.config(text=message)
                label_message.pack()
                print("Erro:", e)

    def criar_tabela(df):
        pt.model.df = df
        pt.show()
        import_button.configure(text='Atualizar Planilha')
        import_button.configure(command=lambda: import_excel('atualizar_tabela'))

    def atualizar_tabela(df):
        pt.model.df = df
        pt.redraw()

    import_button = ttk.Button(tab, text='Importar Planilha',  command=lambda: import_excel('criar_tabela'))
    import_button.pack()

def ler_planilha(path):
    df = pd.read_excel(path, sheet_name='Dados')
    df = df.set_index("Replicatas")  # df.set_index("Replicatas", inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')  # Converter as colunas para formato numérico, se necessário
    df = df.round(2)
    return df
