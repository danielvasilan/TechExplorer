import pandas as pd
import codecs


file_name = "c:\\work\\others\\db_challenge_2\\vehicles_dataset\\vehicles_dataset.csv"
#with codecs.open(file_name, 'r', encoding='utf-8', errors='ignore') as fdata:
#    pass
data = pd.read_csv(file_name, engine='python')

print('csv loaded')

