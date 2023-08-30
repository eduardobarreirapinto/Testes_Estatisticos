import pandas as pd
from scipy.stats import shapiro

def shapiro_teste(col):
    stat, p = shapiro(col)
    if p > 0.05:
        return True
    else:
        return False

def shapiro_estatistica(col):
    stat, p = shapiro(col)
    return stat

def shapiro_p(col):
    stat, p = shapiro(col)
    return p

def shapiro_df(df):
    estatisticas_shapiro = df.apply(shapiro_estatistica)
    estatisticas_df = pd.DataFrame([estatisticas_shapiro], index=['Estatística W'])
    df = pd.concat([df, estatisticas_df])

    p_shapiro = df.apply(shapiro_p)
    p_df = pd.DataFrame([p_shapiro], index=['Valor p'])
    df = pd.concat([df, p_df])

    normal_shapiro = df.apply(shapiro_teste).apply(lambda x: "Sim" if x else "Não")
    normal_df = pd.DataFrame([normal_shapiro], index=['Distribuição Normal'])
    df = pd.concat([df, normal_df])
    return df

# Exemplo de uso
data = {
    'Amostra 1': [73439.33, 74709.57, 75383.99, 76085.28, 76761.00, 76516.32, 76067.53],
    'Amostra 2': [114422.95,114855.20,116134.25,117401.73,117268.61,117733.62,115657.58],
    'Amostra 3': [137847.37,136493.41,135820.57,136135.26,137848.39,138811.59,138185.08],
    'Amostra 4': [168777.89,172028.96,172089.50,173948.81,175236.13,175135.40,175373.97]
}
df = pd.DataFrame(data)

resultados = shapiro_df(df)
print(resultados)
