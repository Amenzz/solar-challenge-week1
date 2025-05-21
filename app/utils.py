import os
import pandas as pd
import scipy.stats as stats

def load_country_data(data_dir):
    country_data = {}
    for file in os.listdir(data_dir):
        if file.endswith("_clean.csv"):
            country_name = file.replace("_clean.csv", "").replace("-", " ").title()
            df = pd.read_csv(os.path.join(data_dir, file))
            df['Country'] = country_name
            country_data[country_name] = df
    return country_data

def compute_summary(df):
    metrics = ['GHI', 'DNI', 'DHI']
    return df.groupby('Country')[metrics].agg(['mean', 'median', 'std'])

def run_anova(df_all):
    groups = df_all.groupby("Country")["GHI"].apply(list)
    return stats.f_oneway(*groups)
