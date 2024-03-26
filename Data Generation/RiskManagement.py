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
    'SupplierID': [random.randint(1, 100) for _ in range(num_rows)],  # Assuming 100 suppliers
    'ProductID': [random.randint(1001, 1050) for _ in range(num_rows)],
    'GeopoliticalRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
    'NaturalDisasterRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
    'MarketVolatilityRisk': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
    'SupplierReliability': [random.choice(['Low', 'Medium', 'High']) for _ in range(num_rows)],
    'OrderLeadTime_days': [random.randint(1, 10) for _ in range(num_rows)],  # Assuming lead time in days
    'InventoryLevel': [random.randint(10, 1000) for _ in range(num_rows)],  # Assuming inventory levels in units
}

# Create DataFrame from the generated data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "RiskManagement_data.csv")
df.to_csv(csv_file_path, index=False)

print("CSV file saved to desktop:", csv_file_path)
