import pandas as pd


def clean_txt(file):
    with open(file, 'w') as f:
        pass


def clean_excel(file):
    empty_df = pd.DataFrame()
    empty_df.to_excel(file, engine='openpyxl')
