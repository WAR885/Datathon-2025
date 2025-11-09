import numpy as np
import pandas as pd
import re

def process_ingredient_data(path:str) -> dict:
    df = pd.read_csv(path, header=None)
    ingredient_names = df.iloc[0,1:].to_list()
    all_ingredients = {}
    for i in range(1,df.shape[0]):
        item_ingredients = {}
        for j in range(1,df.shape[1]):
            item_ingredients[ingredient_names[j-1]] = normalize(df.iat[i,j])
        all_ingredients[df.iat[i,0]] = item_ingredients
    return all_ingredients

def normalize(item) -> float:
    '''Makes raw output into usuable float form'''
    if(pd.isna(item)):
        return 0
    return float(item)