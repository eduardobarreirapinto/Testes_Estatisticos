import tkinter as tk
from tkinter import ttk
import pandas as pd
from scipy.stats import shapiro

def create_tab(tab_control, tab_controller):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Shapiro Wilk')

    ttk.Label(tab, text='').grid(row=0, column=0)
    label = ttk.Label(tab, text='TESTE SHAPIRO WILK')
    label.grid(row=1, column=0)
    ttk.Label(tab, text='').grid(row=2, column=0)

    tableframe = ttk.Frame(tab)
    tableframe.grid(row=3, column=0)

    columns = tab_controller.df.columns

    tree = ttk.Treeview(tableframe, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.grid(row=0, column=0, sticky='nsew')

    vsb = ttk.Scrollbar(tableframe, orient="vertical", command=tree.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=vsb.set)

    populate_treeview(tree, tab_controller.df)

    def atualizar_pandastable(df):
        clear_tree(tree)
        populate_treeview(tree, df)
        tab.redraw()

    tab.atualizar_pandastable = atualizar_pandastable
    return tab

def populate_treeview(tree, dataframe):
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def shapiro_teste(col):
    stat, p = shapiro(col)
    if p > 0.05:
        return "Sim"
    else:
        return "Não"

def shapiro_estatistica(col):
    stat, p = shapiro(col)
    return stat

def shapiro_p(col):
    stat, p = shapiro(col)
    return p

def shapiro_df(df):
    estatisticas_shapiro = df.apply(shapiro_estatistica)
    estatisticas_df = pd.DataFrame([estatisticas_shapiro], index=['Estatística W'])
    df = pd.concat([df, estatisticas_df], axis=0)

    p_shapiro = df.apply(shapiro_p)
    p_df = pd.DataFrame([p_shapiro], index=['Valor p'])
    df = pd.concat([df, p_df], axis=0)

    normal_shapiro = df.apply(shapiro_teste)
    normal_df = pd.DataFrame([normal_shapiro], index=['Distribuição Normal'])
    df = pd.concat([df, normal_df], axis=0)

    return df

# Restante do código...
