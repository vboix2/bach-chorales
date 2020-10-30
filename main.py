import read, transform
import pandas as pd

chorales = read.read_files('xml')
chorales.to_csv('chorales_xml.csv', index=False)



