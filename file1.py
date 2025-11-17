#import libraries
import pandas as pd
import numpy as np

#load dataset
df = pd.read_csv('Airbnb_NYC_2019.csv')
#print(df.head())

# Step 3: Basic Overview
'''print(df.shape)
print(df.info())
print(df.describe(include='all').T)
print(df.describe())
'''
# Missing values
print(df.isnull().sum().sort_values(ascending=False))
