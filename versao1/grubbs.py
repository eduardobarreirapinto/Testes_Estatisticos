import tkinter as tk
from tkinter import ttk
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.stattools as stattools
from scipy.stats import mstats
from scipy.stats import zscore

def create_tab(tab_control, tab_controller):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Grubbs')

    ttk.Label(tab, text='').grid(row=0, column=0)
    label = ttk.Label(tab, text='AVALIAÇÃO DE OUTLIERS - GRUBBS')
    label.grid(row=1, column=0)
    ttk.Label(tab, text='').grid(row=2, column=0)

    treeframe = ttk.Frame(tab)
    treeframe.grid(row=3, column=0)

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

    treeframe1 = ttk.Frame(tab)
    treeframe1.grid(row=4, column=0)

    columns1 = ["OUTLIERS"]

    tree1 = ttk.Treeview(treeframe1, columns=columns1, show='headings')
    for col in columns1:
        tree1.heading(col, text=col)
        tree1.column(col, width=100)

    tree1.grid(row=0, column=0, sticky='nsew')

    vsb1 = ttk.Scrollbar(treeframe1, orient="vertical", command=tree1.yview)
    vsb1.grid(row=0, column=1, sticky='ns')
    tree1.configure(yscrollcommand=vsb1.set)

    populate_treeview(tree1, tab_controller.df)

    def atualizar_pandastable(df):
        clear_tree(tree)
        populate_treeview(tree, df)
        clear_tree(tree1)
        populate_treeview(tree1, grubbs_outlier(df))
        tab.redraw()

    tab.atualizar_pandastable = atualizar_pandastable
    return tab

def populate_treeview(tree, dataframe):
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)

def grubbs_teste(df):
    mean = df.mean()
    std_dev = df.std()
    n = len(df)

    max_outlier = max(df)
    min_outlier = min(df)

    z = (max_outlier - mean) / std_dev if max_outlier > mean else (min_outlier - mean) / std_dev

    critical_value = stats.t.ppf(1 - 0.05 / (2 * n), n - 2)

    return z > critical_value

def grubbs_outlier(df):
    resultados_outlier = df.apply(grubbs_teste).apply(lambda x: "Sim" if x else "Não")
    estatisticas_df = pd.DataFrame([resultados_outlier], index=['OUTLIERS'])
    df = pd.concat([df, estatisticas_df], axis=0)
    return df

def grubbs(df):
    medias = df.mean().round(2)
    medias_sem_min = df.apply(lambda col: col[col != col.min()].mean(), axis=0).round(2)

    # Resto do código permanece o mesmo...

    return df

# Restante do código...
