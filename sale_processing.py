import pandas as pd
import re

def process_sale_data(path:str) -> tuple:
    sheet_names = ["data 1","data 2", "data 3"]
    all_data_raw = "" #Kind of unhinged, but puts all the product data into one colossal string
    total_sales_raw = "" #Puts all of the sales data into one colossal string
    for sheet in sheet_names:
        temp_data = pd.read_excel(path,sheet_name=sheet)
        str_data = temp_data.to_string()
        if "Group" in str_data:
            total_sales_raw += str_data
        else:
            all_data_raw += str_data
    all_data_raw = re.sub(r"\s+(source_page)\s+(source_table).+","",all_data_raw)
    total_sales_raw = re.sub(r"\s+(source_page)\s+(source_table).+","",total_sales_raw)
    return make_dictionary(total_sales_raw),make_dictionary(all_data_raw)

def make_dictionary(raw_data:str) -> dict:
    rows = raw_data.split('\n')
    data_for_items = []
    for row in rows:
        if row == "":
            continue
        data_for_item = {}
        info = re.split(pattern=r"\s{2,}(?![\(-])",string=row)
        data_for_item["name"] = info[3]
        data_for_item["count"] = int(re.sub(r"[$,]","",info[4]))
        data_for_item["amount"] = float(re.sub(r"[$,]","",info[5]))
        data_for_items.append(data_for_item)
    return data_for_items


data_for_items = process_sale_data("mai-shen-yun-main\October_Data_Matrix_20251103_214000.xlsx")