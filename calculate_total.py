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