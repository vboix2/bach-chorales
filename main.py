import read, transform, works
from os import path
import pandas as pd

# Get Chorale works
if path.exists('csv/chorales_xml.csv'):
    chorales = pd.read_csv('csv/chorales_xml.csv')
else:
    chorales = read.read_files('xml')
    chorales.to_csv('csv/chorales_xml.csv', index=False)

# Get works list
if path.exists('csv/bach_works.csv'):
    works = pd.read_csv('csv/bach_works.csv')
else:
    works = works.get_works()
    works.to_csv('csv/bach_works.csv', index=False)


