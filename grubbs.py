import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.stattools as stattools
from scipy.stats import mstats
from scipy.stats import zscore

def create_tab(tab_control, tab_controller):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Grubbs')
    ttk.Label(tab, text='').grid(row=0, column=0) # pular linha
    label = ttk.Label(tab, text='AVALIAÇÃO DE OUTLIERS - GRUBBS')
    # label = ttk.Label(tab, text='AVALIAÇÃO DE OUTLIERS - GRUBBS , font=tab_controller.custom_font)
    label.grid(row=1, column=0)
    ttk.Label(tab, text='').grid(row=2, column=0)# pular linha

    # Tabela 1 com barra de rolagem vertical
    tableframe = ttk.Frame(tab)
    tableframe.grid(row=3, column=0)

    yscrollbar1 = ttk.Scrollbar(tableframe, orient='vertical')
    yscrollbar1.grid(row=0, column=1, sticky='ns')

    pt = Table(tableframe, showtoolbar=False, showstatusbar=True, showindex=True,
               width=500, height=180)
    pt.model.df = tab_controller.df
    pt.show()
    yscrollbar1.config(command=pt.yview)

    ttk.Label(tab, text='').grid(row=4, column=0)

    # Tabela 2 com barra de rolagem vertical
    tableframe1 = ttk.Frame(tab)
    tableframe1.grid(row=5, column=0)

    yscrollbar2 = ttk.Scrollbar(tableframe1, orient='vertical')
    yscrollbar2.grid(row=0, column=1, sticky='ns')

    pt1 = Table(tableframe1, showtoolbar=False, showstatusbar=True, showindex=True,
                width=500, height=180)
    pt1.model.df = tab_controller.df
    pt1.show()
    yscrollbar2.config(command=pt1.yview)

    def atualizar_pandastable(df):
        pt.model.df = grubbs(df)
        pt1.model.df = grubbs_outlier(df)
        pt.redraw()
        pt1.redraw()

    tab.atualizar_pandastable = atualizar_pandastable
    return tab

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

    estatisticas_df = pd.DataFrame([resultados_outlier],index=['OUTLIERS'])

    df = pd.concat([df, estatisticas_df])

    return df

def grubbs(df):

    medias = df.mean().round(2)
    medias_sem_min = df.apply(lambda col: col[col != col.min()].mean(), axis=0).round(2)
    medias_sem_max = df.apply(lambda col: col[col != col.max()].mean(), axis=0).round(2)
    desvios_padrao = df.std().round(2)
    variancias = df.var().round(2)

    gmin = ((medias - df.min()) / desvios_padrao).round(3)
    gmax = ((df.max() - medias) / desvios_padrao).round(3)

    soma_quadratica = df.apply(lambda col: ((col[1:7] - medias[col.name])**2).sum(), axis=0).round(2)


    estatisticas_df = pd.DataFrame([medias,medias_sem_min,medias_sem_max,variancias,desvios_padrao, gmin, gmax,soma_quadratica],
                                   index=['Média','Média Sem Min','Média Sem Max', 'Variância', 'Stand. Dev.', 'Gmin', 'Gmax', 'S02 (com)'])

    df = pd.concat([df, estatisticas_df])

    return df




