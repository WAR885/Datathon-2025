def calculate_monthly_earnings(data:list)->float:
    '''Calculates total earnings for each month'''
    total_each_month = 0
    for item_data in data:
        total_each_month += item_data["amount"]
    return total_each_month
def calculate_yearly_earnings(all_months_data:list)->list:
    total_yearly = []
    for month_data in all_months_data:
        total_yearly.append(calculate_monthly_earnings(month_data[0]))
    return total_yearly
def calculate_total_item_popularities(all_month_item_popularities:list[dict]):
    items_popularity = {}
    for i in range(len(all_month_item_popularities)):
        for item in all_month_item_popularities[i].keys():
            items_popularity[item] = 0
    for month_item_pop in all_month_item_popularities:
        for item in month_item_pop.keys():
            items_popularity[item] += month_item_pop[item]
    return items_popularity
def calculate_total_ingredient_popularities(all_month_ingredient_popularities:list[dict]):
    ingredient_popularity = {}
    for i in range(len(all_month_ingredient_popularities)):
        for item in all_month_ingredient_popularities[i].keys():
            ingredient_popularity[item] = 0
    for month_item_pop in all_month_ingredient_popularities:
        for item in month_item_pop.keys():
            ingredient_popularity[item] += month_item_pop[item]
    #Data looks sus, check tomorrow
    return ingredient_popularity