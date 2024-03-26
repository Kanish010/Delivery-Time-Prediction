import pandas as pd
from faker import Faker
import random
import os

# Initialize Faker for generating fake data
fake = Faker()

# Define the number of rows to generate
num_rows = 50000

# Define categories for each brand
brand_categories = {
    'Sony': 'Electronics',
    'Nike': 'Apparel',
    'Adidas': 'Apparel',
    'Apple': 'Electronics'
}

# Generate synthetic data for each column
data = {
    'ProductID': [random.randint(1001, 1050) for _ in range(num_rows)],
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

# Populate the 'Category' and 'Brand' columns randomly
for _ in range(num_rows):
    brand = random.choice(list(brand_categories.keys()))
    data['Brand'].append(brand)
    data['Category'].append(brand_categories[brand])

# Create DataFrame from the generated data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "DemandForecasting_data.csv")
df.to_csv(csv_file_path, index=False)

print("CSV file saved to desktop:", csv_file_path)
