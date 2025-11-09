import pandas as pd
import re

def process_shipment_data(path:str) -> dict:
    ingredients_data = []
    all_data_raw = ""
    temp_data = pd.read_csv(path)
    all_data_raw = temp_data.to_string()
    rows = all_data_raw.split("\n")
    rows.pop(0)
    shipment_amount = {"weekly":4,"biweekly":8,"monthly":1}
    for row in rows:
        temp = re.split(pattern=r"\s{2,}",string=row)
        ingredient_data = {}
        ingredient_data["ingredient"] = temp[1]
        ingredient_data["unit_of_shipment"] = temp[3]
        ingredient_data["amount_per_month"] = int(temp[2])*int(temp[4])*shipment_amount[temp[5].lower()]
        ingredients_data.append(ingredient_data)
    return ingredients_data