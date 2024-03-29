import pandas as pd
from faker import Faker
import random
import os
import uuid

# Initialize Faker for generating fake data
fake = Faker()

# Define the number of rows to generate
num_rows = 500000

# Define categories for each brand
brand_categories = {
    'Sony': 'Electronics',
    'Nike': 'Apparel',
    'Adidas': 'Apparel',
    'Apple': 'Electronics'
}

# Generate synthetic data for each column
data = {
    'ProductID': [str(uuid.uuid4()) for _ in range(num_rows)],  # Generate unique ProductIDs using UUID
    'Date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(num_rows)],
    'SalesVolume': [random.randint(100, 500) for _ in range(num_rows)],
    'Price': [round(random.uniform(5.99, 99.99), 2) for _ in range(num_rows)],
    'Promotion': [random.choice([0, 1]) for _ in range(num_rows)],
    'Category': [],
    'Brand': [],
    'SeasonalityFactor': [random.choice([0, 1]) for _ in range(num_rows)],
    'CompetitorPresence': [random.choice([0, 1]) for _ in range(num_rows)],
    'WeatherCondition': [random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']) for _ in range(num_rows)],
    'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)],  # Inventory optimization
    'LeadTime_days': [random.randint(1, 10) for _ in range(num_rows)],  # Lead time prediction
    'DemandForecast_units': [random.randint(10, 100) for _ in range(num_rows)],  # Demand forecasting
    'EOQ_units': [random.randint(100, 500) for _ in range(num_rows)],  # Inventory optimization
    'UnitCost': [round(random.uniform(5.99, 20.99), 2) for _ in range(num_rows)],  # Inventory optimization
    'SupplierID': [random.randint(1, 100) for _ in range(num_rows)],  # Lead time prediction / Risk management
    'OrderDate': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],  # Lead time prediction
    'DeliveryDate': [],  # Lead time prediction
    'OrderQuantity_units': [random.randint(10, 100) for _ in range(num_rows)],  # Lead time prediction
    'TransportationMode': [random.choice(['Air', 'Sea', 'Land']) for _ in range(num_rows)],  # Lead time prediction
    'SupplierLocation': [fake.country() for _ in range(num_rows)],  # Lead time prediction
    'OrderUrgency': [random.randint(1, 5) for _ in range(num_rows)],  # Lead time prediction
    'OrderType': [random.choice(['Regular', 'Express']) for _ in range(num_rows)],  # Lead time prediction
    'GeopoliticalRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],  # Risk management
    'NaturalDisasterRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],  # Risk management
    'MarketVolatilityRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],  # Risk management
    'SupplierReliability': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],  # Risk management
    'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)]  # Risk management
}

# Populate the 'Category' and 'Brand' columns randomly
for _ in range(num_rows):
    brand = random.choice(list(brand_categories.keys()))
    data['Brand'].append(brand)
    data['Category'].append(brand_categories[brand])

# Calculate delivery date based on order date and order urgency
for i in range(num_rows):
    order_date = data['OrderDate'][i]
    order_urgency = data['OrderUrgency'][i]
    delivery_date = order_date + pd.DateOffset(days=order_urgency)
    data['DeliveryDate'].append(delivery_date)

# Create DataFrame from the generated data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "SupplyChain_data.csv")
df.to_csv(csv_file_path, index=False)

print("CSV file saved to desktop:", csv_file_path)
