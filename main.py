import read, transform
import constants as K
import pandas as pd

chorales = read.get_chorale()

chorales = transform.clean(chorales)
chorales = transform.analyze(chorales)

print(chorales.head())

