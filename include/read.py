import pandas as pd

def read_csv():
    df = pd.read_csv('so_tags.csv')
    return df['Tags'].values.tolist()


def read_excel():
    df = pd.read_excel('so_tags.xlsx')
    return df['Tags'].values.tolist()

