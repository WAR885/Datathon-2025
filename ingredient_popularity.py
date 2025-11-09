def get_monthly_item_popularity(data:list):
    sorted_data = sorted(data, key=lambda d: d["count"])
    item_popularities = {}
    for item in sorted_data:
        item_popularities[item["name"]] = item["count"]
    return item_popularities
def get_monthly_ingredient_popularity(monthly_sales:list,item_ingredient_quantity:dict):
    ingredient_popularity = {}
    for item in item_ingredient_quantity["Beef Tossed Ramen"].keys():
        ingredient_popularity[item] = 0
    for sale in monthly_sales:
        if sale["name"] in item_ingredient_quantity.keys():
            for key in ingredient_popularity.keys():
                ingredient_popularity[key] += item_ingredient_quantity[sale["name"]][key]*sale["count"]
                #Pork cutlet doesn't work, fix it tomorrow
    return ingredient_popularity

