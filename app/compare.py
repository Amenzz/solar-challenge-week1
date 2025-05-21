import pandas as pd
import glob
import os

def load_country_data(data_dir):
    pattern = os.path.join(data_dir, "*_clean.csv")
    country_data = {}

    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        country = filename.replace("_clean.csv", "")
        df = pd.read_csv(filepath)
        country_data[country] = df

    return country_data
