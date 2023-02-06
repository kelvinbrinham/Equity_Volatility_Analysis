'''
Test
'''

import pandas as pd

columns_lst = ['Dataset', 'No. repeated rows', 'No. Missing time stamps', 'No. Missing prices', 'No. Missing volumes', 'No. Negative Values', 'Outliers']

df = pd.DataFrame(columns = columns_lst)

print(df)

df['Dataset'] = ['A']

print(df)