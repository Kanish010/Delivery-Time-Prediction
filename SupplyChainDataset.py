import pandas as pd
from faker import Faker
import random
import os
import uuid

class DataGenerator:
    def __init__(self, num_rows=5000):
        self.num_rows = num_rows
        self.fake = Faker()

    def generate_demand_data(self):
        brand_categories = {
            'Sony': 'Electronics',
            'Nike': 'Apparel',
            'Adidas': 'Apparel',
            'Apple': 'Electronics'
        }

        data = {
            'ProductID': [str(uuid.uuid4()) for _ in range(self.num_rows)],
            'Date': [self.fake.date_between(start_date='-5y', end_date='today') for _ in range(self.num_rows)],
            'SalesVolume': [random.randint(100, 500) for _ in range(self.num_rows)],
            'Price': [round(random.uniform(5.99, 20.99), 2) for _ in range(self.num_rows)],
            'Promotion': [random.choice([0, 1]) for _ in range(self.num_rows)],
            'Category': [],
            'Brand': [],
            'SeasonalityFactor': [random.choice(['Spring', 'Summer', 'Fall', 'Winter']) for _ in range(self.num_rows)],
            'CompetitorPresence': [random.choice([0, 100]) for _ in range(self.num_rows)],
            'WeatherCondition': [random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']) for _ in range(self.num_rows)]
        }

        for _ in range(self.num_rows):
            brand = random.choice(list(brand_categories.keys()))
            data['Brand'].append(brand)
            data['Category'].append(brand_categories[brand])

        df = pd.DataFrame(data)
        return df

    def generate_inventory_data(self):
        data = {
            'InventoryLevel': [random.randint(10, 1000) for _ in range(self.num_rows)],  
            'LeadTime_days': [random.randint(1, 10) for _ in range(self.num_rows)],  
            'DemandForecast_units': [random.randint(10, 100) for _ in range(self.num_rows)],  
            'EOQ_units': [random.randint(100, 500) for _ in range(self.num_rows)],  
            'UnitCost': [round(random.uniform(5.99, 20.99), 2) for _ in range(self.num_rows)],  
            'ReorderPoint_units': [],
            'ReorderQuantity_units': []
        }

        for i in range(self.num_rows):
            lead_time = data['LeadTime_days'][i]
            demand_forecast = data['DemandForecast_units'][i]
            eoq = data['EOQ_units'][i]
            reorder_point = demand_forecast * lead_time
            reorder_quantity = eoq
            data['ReorderPoint_units'].append(reorder_point)
            data['ReorderQuantity_units'].append(reorder_quantity)

        df = pd.DataFrame(data)
        return df

    def generate_supplier_data(self):
        data = {
            'SupplierID': [str(uuid.uuid4()) for _ in range(self.num_rows)],  
            'GeopoliticalRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(self.num_rows)],
            'NaturalDisasterRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(self.num_rows)],
            'MarketVolatilityRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(self.num_rows)],
            'SupplierReliability': [random.choice(['Low', 'Medium', 'High']) for _ in range(self.num_rows)],
            'OrderLeadTime_days': [random.randint(1, 10) for _ in range(self.num_rows)],  
            'InventoryLevel': [random.randint(10, 1000) for _ in range(self.num_rows)],  
        }

        df = pd.DataFrame(data)
        return df

    def generate_lead_time_prediction_data(self):
        data = {
            'OrderDate': [self.fake.date_between(start_date='-5y', end_date='today') for _ in range(self.num_rows)],
            'DeliveryDate': [],
            'OrderQuantity_units': [random.randint(10, 100) for _ in range(self.num_rows)],
            'TransportationMode': [random.choice(['Air', 'Sea', 'Land']) for _ in range(self.num_rows)],
            'SupplierLocation': [self.fake.country() for _ in range(self.num_rows)],
            'OrderUrgency': [random.randint(1, 5) for _ in range(self.num_rows)],
            'OrderType': [random.choice(['Regular', 'Express']) for _ in range(self.num_rows)]
        }

        for i in range(self.num_rows):
            order_date = data['OrderDate'][i]
            order_urgency = data['OrderUrgency'][i]
            delivery_date = order_date + pd.DateOffset(days=order_urgency)
            data['DeliveryDate'].append(delivery_date)

        df = pd.DataFrame(data)
        return df

    def save_to_csv(self, df, filename):
        csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved to desktop: {csv_file_path}")


if __name__ == "__main__":
    generator = DataGenerator()

    # Generate and save Demand Forecasting data
    demand_df = generator.generate_demand_data()
    generator.save_to_csv(demand_df, "DemandForecasting_data.csv")

    # Generate and save Inventory Optimization data
    inventory_df = generator.generate_inventory_data()
    generator.save_to_csv(inventory_df, "InventoryOptimization_data.csv")

    # Generate and save Risk Management data
    supplier_df = generator.generate_supplier_data()
    generator.save_to_csv(supplier_df, "RiskManagement_data.csv")

    # Generate and save Lead Time Prediction data
    lead_time_df = generator.generate_lead_time_prediction_data()
    generator.save_to_csv(lead_time_df, "LeadTimePrediction_data.csv")
