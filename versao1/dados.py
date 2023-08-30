import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def create_tab(tab_control, tab_controller):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Dados')

    ttk.Label(tab, text='').grid(row=0, column=0, columnspan=3, pady=10)

    label_message = ttk.Label(tab, text='')
    label_message.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    treeframe = ttk.Frame(tab)
    treeframe.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    columns = tab_controller.df.columns

    tree = ttk.Treeview(treeframe, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.grid(row=0, column=0, sticky='nsew')

    vsb = ttk.Scrollbar(treeframe, orient="vertical", command=tree.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=vsb.set)

    populate_treeview(tree, tab_controller.df)

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
                    populate_treeview(tree, tab_controller.df)
                else:
                    atualizar_treeview(tree, tab_controller.df)

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

    def atualizar_treeview(tree, df):
        clear_tree(tree)
        populate_treeview(tree, df)

        tab_controller.grubbs_tab.atualizar_pandastable(df)
        tab_controller.shapiro_wilk_tab.atualizar_pandastable(df)

        plt.figure(figsize=(8, 2))
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

    import_button = ttk.Button(tab, text='Importar Planilha', command=lambda: import_excel('criar_tabela'),
                               style='Custom.TButton')
    import_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky='w')

    return tab

def populate_treeview(tree, dataframe):
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def ler_planilha(path):
    df = pd.read_excel(path, sheet_name='Dados')
    df = df.set_index("Replicatas")
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.round(4)
    return df

# Restante do código...
