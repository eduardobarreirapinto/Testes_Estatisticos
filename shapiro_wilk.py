import tkinter as tk
from tkinter import ttk

def create_tab(tab_control):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Teste Shapiro Wilk')
    label = ttk.Label(tab, text='Teste Shapiro Wilk')
    label.pack()
