import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
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

    pt = Table(tableframe, showtoolbar=False, showstatusbar=True, showindex=True, width=500, height=180)
    pt.model.df = tab_controller.df
    pt.show()

    def atualizar_pandastable(df):
        pt.model.df = shapiro_df(df)
        pt.redraw()

    tab.atualizar_pandastable = atualizar_pandastable
    return tab

def shapiro_teste(col):
    stat, p = shapiro(col)
    if p > 0.05:
        return True
    else:
        return False

def shapiro_df(df):
    resultados_shapiro = df.apply(shapiro_teste).apply(lambda x: "Sim" if x else "Não")
    estatisticas_df = pd.DataFrame([resultados_shapiro], index=['Distribuição Normal'])
    df = pd.concat([df, estatisticas_df])
    return df


