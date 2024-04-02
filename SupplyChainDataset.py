import pandas as pd
from faker import Faker
import random
import os
from uuid import uuid4

# Initialize Faker for generating fake data
fake = Faker()

# Define the number of rows to generate
num_rows = 50000

# Generate a single set of ProductIDs using UUID
product_ids = [str(uuid4()) for _ in range(50)]

def generate_demand_forecasting_data(product_ids):
    brand_categories = {
        'Sony': 'Electronics',
        'Nike': 'Apparel',
        'Adidas': 'Apparel',
        'Apple': 'Electronics'
    }
    data = {
        'ProductID': product_ids * (num_rows // 50),
        'Date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],
        'SalesVolume': [random.randint(100, 500) for _ in range(num_rows)],
        'Price': [round(random.uniform(5.99, 20.99), 2) for _ in range(num_rows)],
        'Promotion': [random.choice([0, 1]) for _ in range(num_rows)],
        'Category': [],
        'Brand': [],
        'SeasonalityFactor': [random.choice([0, 1]) for _ in range(num_rows)],
        'CompetitorPresence': [random.choice([0, 1]) for _ in range(num_rows)],
        'WeatherCondition': [random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']) for _ in range(num_rows)]
    }
    for _ in range(num_rows):
        brand = random.choice(list(brand_categories.keys()))
        data['Brand'].append(brand)
        data['Category'].append(brand_categories[brand])
    return pd.DataFrame(data)

def generate_inventory_optimization_data(product_ids):
    data = {
        'ProductID': product_ids * (num_rows // 50),
        'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)],
        'LeadTime_days': [random.randint(1, 10) for _ in range(num_rows)],
        'DemandForecast_units': [random.randint(10, 100) for _ in range(num_rows)],
        'EOQ_units': [random.randint(100, 500) for _ in range(num_rows)],
        'UnitCost': [round(random.uniform(5.99, 20.99), 2) for _ in range(num_rows)],
        'ReorderPoint_units': [],
        'ReorderQuantity_units': []
    }
    for i in range(num_rows // 50):
        lead_time = data['LeadTime_days'][i]
        demand_forecast = data['DemandForecast_units'][i]
        eoq = data['EOQ_units'][i]
        reorder_point = demand_forecast * lead_time
        reorder_quantity = eoq
        data['ReorderPoint_units'].append(reorder_point)
        data['ReorderQuantity_units'].append(reorder_quantity)
    return pd.DataFrame(data)

def generate_lead_time_prediction_data(product_ids):
    data = {
        'ProductID': product_ids * (num_rows // 50),
        'SupplierID': [random.randint(1, 100) for _ in range(num_rows)],  
        'OrderDate': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],
        'DeliveryDate': [],
        'OrderQuantity_units': [random.randint(10, 100) for _ in range(num_rows)], 
        'TransportationMode': [random.choice(['Air', 'Sea', 'Land']) for _ in range(num_rows)],
        'SupplierLocation': [fake.country() for _ in range(num_rows)],
        'OrderUrgency': [random.randint(1, 5) for _ in range(num_rows)],
        'OrderType': [random.choice(['Regular', 'Express']) for _ in range(num_rows)]
    }
    for i in range(num_rows):
        order_date = data['OrderDate'][i]
        order_urgency = data['OrderUrgency'][i]
        delivery_date = order_date + pd.DateOffset(days=order_urgency)
        data['DeliveryDate'].append(delivery_date)
    return pd.DataFrame(data)

def generate_risk_management_data(product_ids):
    data = {
        'ProductID': product_ids * (num_rows // 50),
        'SupplierID': [random.randint(1, 100) for _ in range(num_rows)],  
        'GeopoliticalRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
        'NaturalDisasterRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
        'MarketVolatilityRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
        'SupplierReliability': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
        'OrderLeadTime_days': [random.randint(1, 10) for _ in range(num_rows)],  
        'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)],  
    }
    return pd.DataFrame(data)

def save_to_csv(df, file_name):
    csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", file_name)
    df.to_csv(csv_file_path, index=False)
    print("CSV file saved to desktop:", csv_file_path)

# Generate data and save to CSV for each scenario
df_demand_forecasting = generate_demand_forecasting_data(product_ids)
df_inventory_optimization = generate_inventory_optimization_data(product_ids)
df_lead_time_prediction = generate_lead_time_prediction_data(product_ids)
df_risk_management = generate_risk_management_data(product_ids)

save_to_csv(df_demand_forecasting, "DemandForecasting_data.csv")
save_to_csv(df_inventory_optimization, "InventoryOptimization_data.csv")
save_to_csv(df_lead_time_prediction, "LeadTimePrediction_data.csv")
save_to_csv(df_risk_management, "RiskManagement_data.csv")