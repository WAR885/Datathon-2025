import heapq
from display_earnings import *
from ingredients_processing import *
from sale_processing import *
from shipment_processing import *
from calculate_total import *
from ingredient_popularity import *
from estimate_future_values import *
class overall_insights:
    
    
    def __init__(self):
        self.sales_data = []
        self.sale_file_names = ['mai-shen-yun-main\May_Data_Matrix (1).xlsx','mai-shen-yun-main\June_Data_Matrix.xlsx',
                    'mai-shen-yun-main\July_Data_Matrix (1).xlsx','mai-shen-yun-main\August_Data_Matrix (1).xlsx',
                    'mai-shen-yun-main\September_Data_Matrix.xlsx','mai-shen-yun-main\October_Data_Matrix_20251103_214000.xlsx',]
        for file in self.sale_file_names:
            self.sales_data.append(process_sale_data(file))
        self.shipment_data = process_shipment_data("mai-shen-yun-main\MSY Data - Shipment.csv")
        self.ingredient_data = process_ingredient_data("mai-shen-yun-main\MSY Data - Ingredient.csv")
        self.yearly_earnings = calculate_yearly_earnings(self.sales_data)
        self.item_pops = []
        self.ingredient_pops = []
        for i in range(len(self.sales_data)):
            self.item_pops.append(get_monthly_item_popularity(self.sales_data[i][1]))
            self.ingredient_pops.append(get_monthly_ingredient_popularity(self.sales_data[i][1],self.ingredient_data))
        graph_earnings(calculate_yearly_earnings(self.sales_data))

        self.total_pop_items = calculate_total_item_popularities(self.item_pops)
        self.total_pop_ingredients = calculate_total_ingredient_popularities(self.ingredient_pops)

        self.projected_earnings = predict_next_monthly_earnings(6,self.yearly_earnings)
        self.projected_pop_items = predict_all_item_popularities(self.item_pops,6)
        self.projected_pop_ingredients = predict_all_ingredient_popularities(self.ingredient_pops,6)
