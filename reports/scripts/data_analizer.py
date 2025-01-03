import pandas as pd
import os
from ium_fij_niew.utils import DATA_FOLDER_PATH
#from ium_fij_niew.globals import DATA_FOLDER_PATH

DATA_FOLDER_PATH = os.path.join("data_analize_scripts", "dane", "v2_raw/")

"""
This module is responsible for data analysis.
"""


def get_nulls(file_path):
    """
    Return number of rows with null-s in data. and number of nulls in each column.
    :param file_path: path to file
    :return: nulls in data
    """
    file_path = os.path.abspath(file_path)
    print(f"Processing file: {file_path}")
    data = pd.read_json(file_path, lines=True)
    no_rows = data.shape[0]
    rows_with_nulls = data.isnull().any(axis=1).sum()
    nulls_per_column = data.isnull().sum()
    return no_rows, rows_with_nulls, nulls_per_column


def print_null_report(file_path):
    """
    Print report about nulls in data.
    :param file_path: path to file
    :return: None
    """
    no_rows, rows_nulls, nulls_per_column = get_nulls(file_path)
    print("File: ", file_path)
    print("Rows: ", no_rows)
    print("Rows with nulls: ", rows_nulls)
    print("Nulls per column:\n-----------------\n", nulls_per_column)
    print("-----------------")
    print("Percent of nulls in data: ", rows_nulls / no_rows * 100, "%")


def analyze_files():
    """
    Analyze all files in data folder.
    :return: None
    """
    for file in os.listdir(DATA_FOLDER_PATH):
        if file.endswith(".jsonl"):
            print_null_report(DATA_FOLDER_PATH + file)
            # add different analysis here

analyze_files()
#print(sys.path)
#sys.path.append('C:/Users/Bartek/Projekty24Z/IUM-Fijalkowski-Niewiarowski/ium_fij_niew')