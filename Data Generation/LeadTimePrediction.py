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
    'OrderDate': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],
    'DeliveryDate': [],
    'OrderQuantity_units': [random.randint(10, 100) for _ in range(num_rows)],  # Assuming order quantity is in units
    'TransportationMode': [random.choice(['Air', 'Sea', 'Land']) for _ in range(num_rows)],
    'SupplierLocation': [fake.country() for _ in range(num_rows)],
    'OrderUrgency': [random.randint(1, 5) for _ in range(num_rows)],
    'OrderType': [random.choice(['Regular', 'Express']) for _ in range(num_rows)]
}

# Calculate delivery date based on order date and order urgency
for i in range(num_rows):
    order_date = data['OrderDate'][i]
    order_urgency = data['OrderUrgency'][i]
    delivery_date = order_date + pd.DateOffset(days=order_urgency)
    data['DeliveryDate'].append(delivery_date)

# Create DataFrame from the generated data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "LeadTimePrediction_data.csv")
df.to_csv(csv_file_path, index=False)

print("CSV file saved to desktop:", csv_file_path)
