import pandas as pd
from faker import Faker
import random
import os

# Initialize Faker for generating fake data
fake = Faker()

# Define the number of rows to generate
num_rows = 50000

# Generate synthetic data for each column
data = {
    'ProductID': [random.randint(1001, 1050) for _ in range(num_rows)],
    'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)],  # Assuming inventory levels in units
    'LeadTime_days': [random.randint(1, 10) for _ in range(num_rows)],  # Assuming lead time in days
    'DemandForecast_units': [random.randint(10, 100) for _ in range(num_rows)],  # Assuming demand forecast in units
    'EOQ_units': [random.randint(100, 500) for _ in range(num_rows)],  # Assuming Economic Order Quantity (EOQ) in units
    'UnitCost': [round(random.uniform(5.99, 20.99), 2) for _ in range(num_rows)],  # Assuming unit cost in currency
    'ReorderPoint_units': [],
    'ReorderQuantity_units': []
}

# Calculate reorder point and reorder quantity based on lead time, demand forecast, and EOQ
for i in range(num_rows):
    lead_time = data['LeadTime_days'][i]
    demand_forecast = data['DemandForecast_units'][i]
    eoq = data['EOQ_units'][i]
    reorder_point = demand_forecast * lead_time
    reorder_quantity = eoq
    data['ReorderPoint_units'].append(reorder_point)
    data['ReorderQuantity_units'].append(reorder_quantity)

# Create DataFrame from the generated data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "InventoryOptimization_data.csv")
df.to_csv(csv_file_path, index=False)

print("CSV file saved to desktop:", csv_file_path)
