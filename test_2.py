import pandas as pd

df = pd.DataFrame({"Numbers": [1, 2, 3]})

def subtract(x, y):
    return x - y 

df = df.apply(subtract, args=))

print(df)