def predict_next_monthly_earnings(month_count:int,monthly_earnings:list):
    return sum(monthly_earnings)/month_count
def predict_all_item_popularities(all_month_item_popularities:list[dict], month_count:int):
    items_popularity = {}
    for i in range(len(all_month_item_popularities)):
        for item in all_month_item_popularities[i].keys():
            items_popularity[item] = 0
    for month_item_pop in all_month_item_popularities:
        for item in month_item_pop.keys():
            items_popularity[item] += month_item_pop[item]
    for item in items_popularity.keys():
        items_popularity[item] /= month_count
    return items_popularity
def predict_all_ingredient_popularities(all_month_ingredient_popularities:list[dict], month_count:int):
    ingredient_popularity = {}
    for i in range(len(all_month_ingredient_popularities)):
        for item in all_month_ingredient_popularities[i].keys():
            ingredient_popularity[item] = 0
    for month_item_pop in all_month_ingredient_popularities:
        for item in month_item_pop.keys():
            ingredient_popularity[item] += month_item_pop[item]
    for item in ingredient_popularity.keys():
        ingredient_popularity[item] /= month_count
    #Data looks sus, check tomorrow
    return ingredient_popularity

            