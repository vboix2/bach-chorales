import read
import constants as K
from os import listdir
import pandas as pd

FILES = listdir('files')
PATH = 'files/'

# XML dataframe
data = pd.DataFrame(columns=K.COLUMNS)

# Read XML files
for file in FILES:
    data = data.append(read.read_xml(PATH + file))

print(data)