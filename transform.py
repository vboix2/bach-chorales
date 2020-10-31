
import pandas as pd
import re

def clean(df):

    # Work title
    works = pd.read_csv('csv/bach_works.csv')

    df['bwv'] = df['bwv'].apply(lambda x: int(x.split(" ")[1]))

    df['title'] = pd.merge(df, works, how='left', on='bwv')['title']


    return df