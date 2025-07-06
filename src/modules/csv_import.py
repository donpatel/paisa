import pandas as pd
import os

def import_csv(folder, filename):
    """Import CSV file and return as pandas DataFrame"""
    filepath = os.path.join(folder, filename)
    df = pd.read_csv(filepath)
    return df