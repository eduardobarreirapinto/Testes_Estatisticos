import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandastable import Table, TableModel


def create_tab(tab_control, tab_controller):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Dados')

    ttk.Label(tab, text='').grid(row=0, column=0, columnspan=3, pady=10)

    label_message = ttk.Label(tab, text='')
    label_message.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    tableframe = ttk.Frame(tab)
    tableframe.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    pt = Table(tableframe, showtoolbar=False, showstatusbar=True, showindex=True, width=520, height=170)
    pt.show()

    canvas_frame = ttk.Frame(tab)
    canvas_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    def import_excel(criar_ou_atualizar):
        nonlocal tab
        import_button.config(state='disabled')
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                tab_controller.df = ler_planilha(file_path)
                if criar_ou_atualizar == 'criar_tabela':
                    criar_tabela(tab_controller.df)
                else:
                    atualizar_tabela(tab_controller.df)

            except Exception as e:
                message = "Erro ao importar arquivo."
                label_message.config(text=message)
                label_message.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky='w')
                print("Erro:", e)
                raise
            finally:
                import_button.config(state='normal')
                import_button.config(text='Atualizar Planilha')
                import_button.config(command=lambda: import_excel('atualizar_tabela'))

    def criar_tabela(df):
        tab_controller.df = df
        pt.model.df = df
        pt.redraw()

        tab_controller.grubbs_tab.atualizar_pandastable(df)
        tab_controller.shapiro_wilk_tab.atualizar_pandastable(df)

        plt.figure(figsize=(8, 2))  # Reduzir a altura do gráfico
        for column in df.columns:
            plt.plot(df[column], label=column)

        plt.xlabel('Replicatas')
        plt.ylabel('Intensidade dos Padrões')
        plt.title('Intensidade dos Padrões X Replicatas')
        plt.legend()
        plt.grid(True)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def atualizar_tabela(df):
        tab_controller.df = df
        pt.model.df = df
        pt.redraw()

        tab_controller.grubbs_tab.atualizar_pandastable(df)
        tab_controller.shapiro_wilk_tab.atualizar_pandastable(df)

    import_button = ttk.Button(tab, text='Importar Planilha', command=lambda: import_excel('criar_tabela'),
                               style='Custom.TButton')
    import_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    return tab


def ler_planilha(path):
    df = pd.read_excel(path, sheet_name='Dados')
    df = df.set_index("Replicatas")
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.round(2)
    return df
