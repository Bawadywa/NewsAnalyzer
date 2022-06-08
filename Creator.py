import os
import pandas as pd


def create_txt(file_name):
    file_exists = os.path.exists(file_name)
    if not file_exists:
        with open(file_name, 'w') as file:
            pass


def create_excel(file_name):
    file_exists = os.path.exists(file_name)
    if not file_exists:
        df = pd.DataFrame()
        df.to_excel(file_name, engine='openpyxl')
